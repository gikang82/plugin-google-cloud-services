import time
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.vpc_network.data import *
from ipaddress import ip_address, IPv4Address
from spaceone.inventory.model.vpc_network.cloud_service import *
from spaceone.inventory.connector.vpc_network import VPCNetworkConnector
from spaceone.inventory.model.vpc_network.cloud_service_type import CLOUD_SERVICE_TYPES
from pprint import pprint


class VPCNetworkManager(GoogleCloudManager):
    connector_name = 'VPCNetworkConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** VPC Network START **")
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
        vpc_conn: VPCNetworkConnector = self.locator.get_connector(self.connector_name, **params)

        # Get lists that relate with snapshots through Google Cloud API
        networks = vpc_conn.list_networks()
        firewalls = vpc_conn.list_firewall()
        subnets = vpc_conn.list_subnetworks()
        routes = vpc_conn.list_routes()
        regional_address = vpc_conn.list_regional_addresses()

        for network in networks:

            network_identifier = network.get('selfLink')
            matched_firewall = self._get_matched_firewalls(network_identifier, firewalls)
            matched_route = self.get_matched_route(network_identifier, routes)
            matched_subnets = self._get_matched_subnets(network_identifier, subnets)
            region = self.match_region_info('global')
            peerings = self.get_peering(network)

            network.update({
                'mode': 'Auto' if network.get('autoCreateSubnetworks') else 'Custom',
                'project': secret_data['project_id'],
                'global_dynamic_route': self._get_global_dynamic_route(network, 'not_mode'),
                'dynamic_routing_mode': self._get_global_dynamic_route(network, 'mode'),
                'subnet_creation_mode': 'Auto' if network.get('autoCreateSubnetworks') else 'Custom',
                'ip_address_data': self.get_internal_ip_address_in_use(network, regional_address),
                'peerings': peerings,
                'route_data': {
                    'total_number': len(matched_route),
                    'route': matched_route
                },
                'firewall_data': {
                    'total_number': len(matched_firewall),
                    'firewall': matched_firewall
                },
                'subnetwork_data': {
                    'total_number': len(matched_subnets),
                    'subnets': matched_subnets
                },
            })

            # No labels
            _name = network.get('name', '')
            vpc_data = VPCNetwork(network, strict=False)
            vpc_resource = VPCNetworkResource({
                'name': _name,
                'region_code': region.get('region_code'),
                'data': vpc_data,
                'reference': ReferenceModel(vpc_data.reference())
            })

            self.set_region_code('global')
            collected_cloud_services.append(VPCNetworkResponse({'resource': vpc_resource}))

        print(f'** VPC Network Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services

    def get_internal_ip_address_in_use(self, network, regional_address):
        all_Internal_addresses = []
        for ip_address in regional_address:
            ip_type = ip_address.get('addressType', '')
            subnetwork = ip_address.get('subnetwork', '')

            if ip_type == 'INTERNAL' and subnetwork in network.get('subnetworks', []):
                simple_region = ip_address.get('region')
                users = ip_address.get('users')
                ip_address.update({
                    'subnet_name': network.get('name'),
                    'ip_version_display': self._valid_ip_address(ip_address.get('address')),
                    'region': simple_region[simple_region.rfind('/') + 1:] if simple_region else 'global',
                    'used_by': self._get_parse_users(users) if users else ['None'],
                    'is_ephemeral': 'Static'
                })

                all_Internal_addresses.append(IPAddress(ip_address, strict=False))

        return all_Internal_addresses

    def get_peering(self, network):
        updated_peering = []
        for peer in network.get('peerings', []):
            peer_network = peer.get('network')[peer.get('network').find('/projects/') + 10:]

            ex_custom = 'None'
            if peer.get('exportCustomRoutes') and peer.get('importCustomRoutes'):
                ex_custom = 'Import & Export custom routes'
            elif peer.get('exportCustomRoutes'):
                ex_custom = 'Export custom routes'
            elif peer.get('importCustomRoutes'):
                ex_custom = 'Import custom routes'

            ex_route = 'None'
            if peer.get('exportSubnetRoutesWithPublicIp') and peer.get('importSubnetRoutesWithPublicIp'):
                ex_route = 'Import & Export subnet routes with public IP'
            elif peer.get('exportSubnetRoutesWithPublicIp'):
                ex_route = 'Export subnet routes with public IP'
            elif peer.get('importSubnetRoutesWithPublicIp'):
                ex_route = 'Import subnet routes with public IP'

            display = {
                'your_network': self._get_matched_last_target('selfLink', network),
                'peered_network': self._get_matched_last_target('network', peer),
                'project_id': peer_network[:peer_network.find('/')],
                'state_display': peer.get('state').capitalize(),
                'ex_custom_route': ex_custom,
                'ex_route_public_ip_display': ex_route
            }
            peer.update({
                'display': display
            })
            updated_peering.append(peer)
        return updated_peering

    def get_matched_route(self, network, routes):
        route_vos = []

        for route in routes:
            if network == route.get('network', ''):
                next_hop = ''
                if 'nextHopInstance' in route:
                    target = self._get_matched_last_target('nextHopInstance', route).capitalize()
                    zone = self._get_zone_from_target('nextHopInstance', route)
                    next_hop = f'Instance {target} (zone  {zone})'

                elif 'nextHopIp' in route:
                    target = self._get_matched_last_target('nextHopIp', route).capitalize()
                    next_hop = f'IP address lie within {target}'

                elif 'nextHopNetwork' in route:
                    target = self._get_matched_last_target('nextHopNetwork', route)
                    next_hop = f'Virtual network {target}'

                elif 'nextHopGateway' in route:
                    target = self._get_matched_last_target('nextHopGateway', route).capitalize()
                    next_hop = f'{target} internet gateway'

                elif 'nextHopIlb' in route:
                    target = self._get_matched_last_target('nextHopIlb', route).capitalize()
                    next_hop = f' Loadbalancer on {target}'

                elif 'nextHopPeering' in route:
                    target = self._get_matched_last_target('nextHopPeering', route).capitalize()
                    next_hop = f'Peering : {target}'

                route.update({
                    'next_hop': next_hop,
                })
                route_vos.append(route)
        return route_vos

    @staticmethod
    def _get_matched_last_target(key, source):
        a = source.get(key, '')
        return a[a.rfind('/') + 1:]

    @staticmethod
    def _get_zone_from_target(key, source):
        a = source.get(key, '')
        return a[a.find('zones') + 6:a.find('/instances')]

    @staticmethod
    def _get_matched_subnets(network, subnets):
        matched_subnet = []
        for subnet in subnets:
            if network == subnet.get('network', ''):
                log_config = subnet.get('logConfig', {})
                r_ref = subnet.get('region')
                subnet.update({
                    'region': r_ref[r_ref.rfind('/') + 1:],
                    'google_access': 'On' if subnet.get('privateIpGoogleAccess') else 'Off',
                    'flow_log': 'On' if log_config.get('enable') else 'Off'
                })
                matched_subnet.append(subnet)
        return matched_subnet

    @staticmethod
    def _get_matched_firewalls(network, firewalls):
        firewall_vos = []

        for firewall in firewalls:
            if network == firewall.get('network', ''):
                target_tag = firewall.get('targetTags', [])
                filter_range = ', '.join(firewall.get('sourceRanges', ''))
                log_config = firewall.get('log_config', {})

                protocol_port = []
                flag = 'allowed' if 'allowed' in firewall else 'denied'
                for allowed in firewall.get(flag, []):
                    ip_protocol = allowed.get('IPProtocol', '')

                    for port in allowed.get('ports', []):
                        protocol_port.append(f'{ip_protocol}: {port}')

                display = {
                    'type_display': 'Ingress' if firewall.get('direction') == 'INGRESS' else 'Egress',
                    'target_display': ['Apply to all'] if not target_tag else target_tag,
                    'filter': f'IP ranges: {filter_range}',
                    'protocols_port': protocol_port,
                    'action': 'Allow' if 'allowed' in firewall else 'Deny',
                    'logs': 'On' if log_config.get('enable') else 'Off'
                }

                firewall.update({
                    'display': display
                })

                firewall_vos.append(firewall)
        return firewall_vos

    @staticmethod
    def _valid_ip_address(ip):
        try:
            return "IPv4" if type(ip_address(ip)) is IPv4Address else "IPv6"
        except ValueError:
            return "Invalid"

    @staticmethod
    def _get_global_dynamic_route(network, flag):
        routing_config = network.get('routingConfig', {})
        if flag == 'mode':
            return 'Regional' if routing_config == 'REGIONAL' else 'Global'
        else:
            return 'Off' if routing_config == 'REGIONAL' else 'On'

    @staticmethod
    def _get_parse_users(users):
        parsed_used_by = []
        for user in users:
            zone = user[user.find('zones') + 6:user.find('/instances')]
            instance = user[user.rfind('/') + 1:]
            used = f'VM instance {instance} (Zone: {zone})'
            parsed_used_by.append(used)

        return parsed_used_by
