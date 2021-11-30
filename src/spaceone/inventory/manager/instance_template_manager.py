import time
import logging
import json

from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.model.instance_template.data import *
from spaceone.inventory.model.instance_template.cloud_service import *
from spaceone.inventory.connector.instance_template import InstanceTemplateConnector
from spaceone.inventory.model.instance_template.cloud_service_type import CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class InstanceTemplateManager(GoogleCloudManager):
    connector_name = 'InstanceTemplateConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** Instance Template START **')
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
            CloudServiceResponse/ErrorResourceResponse
        """
        collected_cloud_services = []

        try:
            secret_data = params['secret_data']
            instance_template_conn: InstanceTemplateConnector = self.locator.get_connector(self.connector_name, **params)

            # Get Instance Templates
            instance_templates = instance_template_conn.list_instance_templates()
            instance_groups = instance_template_conn.list_instance_group_managers()
            machine_types = instance_template_conn.list_machine_types()

            for inst_template in instance_templates:
                properties = inst_template.get('properties', {})
                tags = properties.get('tags', {})

                in_used_by, matched_instance_group = self.match_instance_group(inst_template, instance_groups)
                disks = self.get_disks(properties)
                labels = self.convert_labels_format(properties.get('labels', {}))

                inst_template.update({
                    'project': secret_data['project_id'],
                    'in_used_by': in_used_by,
                    'ip_forward': properties.get('canIpForward', False),
                    'machine': MachineType(self._get_machine_type(properties, machine_types), strict=False),
                    'network_tags': tags.get('items', []),
                    'scheduling': self._get_scheduling(properties),
                    'disk_display': self._get_disk_type_display(disks, 'disk_type'),
                    'image': self._get_disk_type_display(disks, 'source_image_display'),
                    'instance_groups': matched_instance_group,
                    'network_interfaces': self.get_network_interface(properties),
                    'fingerprint': self._get_properties_item(properties, 'metadata', 'fingerprint'),
                    'labels': labels,
                    'disks': disks
                })

                svc_account = properties.get('serviceAccounts', [])
                if len(svc_account) > 0:
                    inst_template.update({'service_account': self._get_service_account(svc_account)})
                _name = inst_template.get('name', '')
                instance_template_data = InstanceTemplate(inst_template, strict=False)
                # labels -> tags
                default_region = 'global'

                instance_template_resource = InstanceTemplateResource({
                    'name': _name,
                    'tags': labels,
                    'data': instance_template_data,
                    'reference': ReferenceModel(instance_template_data.reference()),
                    'region_code': default_region
                })

                self.set_region_code(default_region)
                collected_cloud_services.append(InstanceTemplateResponse({'resource': instance_template_resource}))
        except Exception as e:
            _LOGGER.error(f'[collect_cloud_service] => {e}')

            if type(e) is dict:
                return [
                    ErrorResourceResponse({
                        'message': json.dumps(e),
                        'resource': {
                            'cloud_service_group': 'ComputeEngine',
                            'cloud_service_type': 'InstanceTemplate'
                        }
                    })
                ]
            else:
                return [
                    ErrorResourceResponse({
                        'message': str(e),
                        'resource': {
                            'cloud_service_group': 'ComputeEngine',
                            'cloud_service_type': 'InstanceTemplate'
                        }
                    })
                ]

        _LOGGER.debug(f'** Instance Template Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services

    def match_instance_group(self, instance_template, instance_group_managers: list):
        in_used_by = []
        instance_group_infos = []
        for instance_group in instance_group_managers:
            version_info = instance_group.get('versions', [])
            for version in version_info:
                template_self_link_source = instance_template.get('selfLink', '')
                template_self_link_target = version.get('instanceTemplate', '')
                if self._check_self_link_matched(template_self_link_source, '/projects/', 10,
                                                 template_self_link_target, '/projects/', 10, ):
                    in_used_by.append(instance_group.get('name', ''))
                    instance_group_infos.append(InstanceGroup(instance_group, strict=False))

        return in_used_by, instance_group_infos

    def get_disks(self, instance):
        disk_info = []
        for disk in instance.get('disks', []):
            _LOGGER.debug(f'get_disk => {disk}')
            init_param = disk.get('initializeParams', {})
            # initializeParams: {diskSizeGb: ""} can be Null
            if init_param.get('diskSizeGb') is not None:
                size = self._get_bytes(int(init_param.get('diskSizeGb')))
            else:
                size = 0
            disk_info.append(Disk({
                'device_index': disk.get('index'),
                'device': disk.get('deviceName'),
                'device_type': disk.get('type', ''),
                'device_mode': disk.get('mode', ''),
                'size': float(size),
                'tags': self.get_tags_info(disk)
            }, strict=False))
        return disk_info

    def get_tags_info(self, disk):
        init_param = disk.get('initializeParams', {})
        disk_size = float(init_param.get('diskSizeGb'))
        disk_type = init_param.get('diskType')
        sc_image = init_param.get('sourceImage', '')
        return {
            'disk_type': init_param.get('diskType'),
            'source_image': sc_image,
            'source_image_display': sc_image[sc_image.rfind('/')+1:],
            'auto_delete': disk.get('autoDelete'),
            'read_iops': self.get_iops_rate(disk_type, disk_size, 'read'),
            'write_iops': self.get_iops_rate(disk_type, disk_size, 'write'),
            'read_throughput': self.get_throughput_rate(disk_type, disk_size),
            'write_throughput': self.get_throughput_rate(disk_type, disk_size),
        }

    def get_network_interface(self, instance):
        network_interface_info = []
        for network_interface in instance.get('networkInterfaces', []):
            configs, tiers = self._get_access_configs_type_and_tier(network_interface.get('accessConfigs', []))
            network_interface_info.append({
                'idx_name': network_interface.get('name', ''),
                'network': network_interface.get('network', ''),
                'network_display': self._get_display_info(network_interface.get('network', '')),
                'configs': configs,
                'network_tier': tiers,
                'access_configs': network_interface.get('accessConfigs', []),
                'kind': network_interface.get('kind', [])
            })

        return network_interface_info

    def get_iops_rate(self, disk_type, disk_size, flag):
        const = self._get_iops_constant(disk_type, flag)
        return disk_size * const

    def get_throughput_rate(self, disk_type, disk_size):
        const = self._get_throughput_constant(disk_type)
        return disk_size * const

    @staticmethod
    def _get_machine_type(instance, machine_types):
        machine = None
        machine_type = instance.get('machineType', '')
        machine_vo = {'machine_type': machine_type}

        if machine_type != '':
            for item in machine_types:
                if item.get('name') == machine_type:
                    machine = item

        if machine:
            core = machine.get('guestCpus')
            memory = float(machine.get('memoryMb')) * 0.0009765625
            m_str = str(memory)
            display_memory = m_str if m_str[m_str.find('.'):] != '.0' else m_str[:m_str.find('.')]
            machine_vo.update({
                'machine_display': f'{machine_type} : {core} vCPUs {display_memory} GB RAM',
                'machine_detail': machine.get('description'),
                'core': core,
                'memory': memory
            })
        return machine_vo

    @staticmethod
    def _get_access_configs_type_and_tier(access_configs):
        configs = []
        tiers = []
        for access_config in access_configs:
            ac_name = access_config.get('name', '')
            ac_type = access_config.get('type', '')
            configs.append(f' {ac_name} : {ac_type}')
            tiers.append(access_config.get('networkTier', ''))
        return configs, tiers

    @staticmethod
    def _get_service_account(svc_account):
        service_account = svc_account[0]
        return {
            'email': service_account.get('email', ''),
            'scopes': service_account.get('scopes', [])
        }

    @staticmethod
    def _check_self_link_matched(source_self_link: str,
                                 source_context: str,
                                 source_idx: int,
                                 target_self_link: str,
                                 target_context: str,
                                 target_idx: int):

        return source_self_link[source_self_link.find(source_context) + source_idx:] == \
               target_self_link[target_self_link.find(target_context) + target_idx:]

    @staticmethod
    def _get_iops_constant(disk_type, flag):
        constant = 0.0
        if flag == 'read':
            if disk_type == 'pd-standard':
                constant = 0.75
            elif disk_type == 'pd-balanced':
                constant = 6.0
            elif disk_type == 'pd-ssd':
                constant = 30.0
        else:
            if disk_type == 'pd-standard':
                constant = 1.5
            elif disk_type == 'pd-balanced':
                constant = 6.0
            elif disk_type == 'pd-ssd':
                constant = 30.0
        return constant

    @staticmethod
    def _get_display_info(network):
        network_display = ''
        if network != '':
            network_display = network[network.rfind('/') + 1:]
        return network_display

    @staticmethod
    def _get_disk_type_display(disk, key):
        if len(disk) > 0:
            tag = disk[0].get('tags', {})
            disk_type = tag.get(key, '')
            return disk_type
        else:
            return ''

    @staticmethod
    def _get_bytes(number):
        return 1024 * 1024 * 1024 * number

    @staticmethod
    def _get_properties_item(properties: dict, item_key: str, key: str):
        item = properties.get(item_key)
        selected_prop_item = item.get(key) if item else ''
        return selected_prop_item

    @staticmethod
    def _get_scheduling(properties):
        scheduling = properties.get('scheduling', {})
        return {
            'on_host_maintenance': scheduling.get('onHostMaintenance', 'MIGRATE'),
            'automatic_restart': 'On' if scheduling.get('automaticRestart', False) == True else 'Off',
            'preemptibility': 'On' if scheduling.get('preemptible', False) == True else 'Off',
        }

    @staticmethod
    def _get_throughput_constant(disk_type):
        constant = 0.0
        if disk_type == 'pd-standard':
            constant = 0.12
        elif disk_type == 'pd-balanced':
            constant = 0.28
        elif disk_type == 'pd-ssd':
            constant = 0.48

        return constant
