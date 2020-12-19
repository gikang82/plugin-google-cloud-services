
import time
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.external_ip_address.data import *
from ipaddress import ip_address, IPv4Address
from spaceone.inventory.model.external_ip_address.cloud_service import *
from spaceone.inventory.connector.external_ip_address import ExternalIPAddressConnector
from spaceone.inventory.model.external_ip_address.cloud_service_type import CLOUD_SERVICE_TYPES
from pprint import pprint


class ExternalIPAddressManager(GoogleCloudManager):
    connector_name = 'ExternalIPAddressConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** External IP Address START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        collected_cloud_services = []
        secret_data = params['secret_data']
        exp_conn: ExternalIPAddressConnector = self.locator.get_connector(self.connector_name, **params)
        regional_global_addresses = exp_conn.list_regional_addresses()
        compute_engine_vm_address = exp_conn.list_instance_for_networks()
        forwarding_rule_address = exp_conn.list_forwarding_rule()

        # Get lists that relate with snapshots through Google Cloud API
        all_external_ip_addresses = self.get_external_ip_addresses(regional_global_addresses,
                                                                   compute_engine_vm_address,
                                                                   forwarding_rule_address)

        for external_ip_juso in all_external_ip_addresses:
            region = external_ip_juso.get('region') if external_ip_juso.get('region') else 'global'
            external_ip_juso.update({'project': secret_data['project_id']})
            external_ip_juso_data = ExternalIpAddress(external_ip_juso, strict=False)
            external_ip_juso_resource = ExternalIpAddressResource({
                'region_code': region,
                'data': external_ip_juso_data,
                'reference': ReferenceModel(external_ip_juso_data.reference())
            })

            self.set_region_code(region)
            collected_cloud_services.append(ExternalIpAddressResponse({'resource': external_ip_juso_resource}))

        print(f'** External IP Address Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services


    def get_external_ip_addresses(self, regional_address, instances_over_region, forwarding_rules):

        all_ip_juso_vos = []
        all_ip_juso_only_check_dup = []

        for region in regional_address.keys():
            if 'addresses' in regional_address.get(region):
                for ip_juso in regional_address.get(region).get('addresses'):
                    if 'EXTERNAL' == ip_juso.get('addressType'):
                        simple_region = ip_juso.get('region')
                        users = ip_juso.get('users')
                        ip_juso.update({
                            'region': simple_region[simple_region.rfind('/')+1:] if simple_region else 'global',
                            'used_by': self._get_parse_users(users) if users else ['None'],
                            'ip_version_display': self._valid_ip_address(ip_juso.get('address')),
                            'is_ephemeral': 'Static'
                        })
                        all_ip_juso_only_check_dup.append(ip_juso.get('address'))
                        all_ip_juso_vos.append(ip_juso)

        for forwarding_rule in forwarding_rules:
            forwarding_ip_juso = forwarding_rule.get('IPAddress')
            if forwarding_rule.get('loadBalancingScheme') == 'EXTERNAL' and forwarding_ip_juso not in all_ip_juso_only_check_dup:
                rule_name = forwarding_rule.get('name')
                forwarding_rule.update({
                    'is_ephemeral': 'Ephemeral',
                    'ip_version_display': self._valid_ip_address(forwarding_ip_juso),
                    'address_type': forwarding_rule.get('loadBalancingScheme'),
                    'address': forwarding_ip_juso,
                    'region': self._get_region_from_forwarding_rule(forwarding_rule),
                    'status': 'IN_USE',
                    'users': [forwarding_rule.get('selfLink')],
                    'used_by': [f'Forwarding rule {rule_name}'],
                })
                all_ip_juso_only_check_dup.append(forwarding_ip_juso)
                all_ip_juso_vos.append(forwarding_rule)

        for instance in instances_over_region:
            network_interfaces = instance.get('networkInterfaces', [])
            zone = self._get_matched_last_target('zone', instance)
            region = zone[:-2]
            for network_interface in network_interfaces:
                external_ip_infos = network_interface.get('accessConfigs')
                for external_ip_info in external_ip_infos:
                    if 'natIP' in external_ip_info and external_ip_info.get('natIP') not in all_ip_juso_only_check_dup:
                        instance_name = instance.get('name')
                        external_ip = {
                            'address': external_ip_info.get('natIP'),
                            'region': region,
                            'address_type': 'EXTERNAL',
                            'is_ephemeral': 'Ephemeral',
                            'network_tier': external_ip_info.get('networkTier'),
                            'network_tier_display': self._get_network_tier_display(external_ip_info),
                            'status': 'IN_USE',
                            'ip_version_display': self._valid_ip_address(external_ip_info.get('natIP')),
                            'creation_timestamp': instance.get('creationTimestamp'),
                            'users': [instance.get('selfLink')],
                            'used_by': [f'Vm Instance {instance_name} ({zone})'],
                            'labels': [],
                        }
                        all_ip_juso_only_check_dup.append(external_ip_info.get('natIP'))
                        all_ip_juso_vos.append(external_ip)



        return all_ip_juso_vos

    @staticmethod
    def _valid_ip_address(ip):
        try:
            return "IPv4" if type(ip_address(ip)) is IPv4Address else "IPv6"
        except ValueError:
            return "Invalid"

    @staticmethod
    def _get_region_from_forwarding_rule(forwarding_rule):
        self_link = forwarding_rule.get('selfLink')
        parsed_link = self_link[self_link.find('projects/')+9:]
        return 'global' if parsed_link == '' else parsed_link[parsed_link.find('/')+1:parsed_link.find('/forwardingRules')]


    @staticmethod
    def _get_network_tier_display(external_ip_info):
        display_value = ''
        if external_ip_info.get('networkTier') is not None:
            display_value = external_ip_info.get('networkTier').capitalize()
        return display_value

    @staticmethod
    def _get_parse_users(users):
        parsed_used_by = []
        for user in users:
            zone = user[user.find('zones') + 6:user.find('/instances')]
            instance = user[user.rfind('/') + 1:]
            used = f'VM instance {instance} (Zone: {zone})'
            parsed_used_by.append(used)

        return parsed_used_by

    @staticmethod
    def _get_matched_last_target(key, source):
        a = source.get(key, '')
        return a[a.rfind('/') + 1:]