import time
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.load_balancing.data import *
from spaceone.inventory.model.load_balancing.cloud_service import *
from spaceone.inventory.connector.load_balancing import LoadBalancingConnector
from spaceone.inventory.model.load_balancing.cloud_service_type import CLOUD_SERVICE_TYPES
from pprint import pprint


class LoadBalancingManager(GoogleCloudManager):
    connector_name = 'LoadBalancingConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Load Balancing START **")
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
        load_bal_conn: LoadBalancingConnector = self.locator.get_connector(self.connector_name, **params)

        region = 'global'
        project_id = secret_data.get('project_id')

        target_pools = load_bal_conn.list_target_pools()
        url_maps = load_bal_conn.list_url_maps()
        forwarding_rules = load_bal_conn.list_forwarding_rules()
        backend_services = load_bal_conn.list_back_end_services()
        backend_buckets = load_bal_conn.list_back_end_buckets()
        ssl_certificates = load_bal_conn.list_ssl_certificates()

        # proxies
        grpc_proxies = load_bal_conn.list_grpc_proxies()
        http_proxies = load_bal_conn.list_target_http_proxies()
        https_proxies = load_bal_conn.list_target_https_proxies()

        all_proxies = self.get_all_proxy_list(grpc_proxies, http_proxies, https_proxies, forwarding_rules)





        load_balances = self.get_load_balancer_infos(url_maps,
                                                     backend_services,
                                                     target_pools,
                                                     forwarding_rules,
                                                     all_proxies,
                                                     project_id)

        for load_balance in load_balances:
            identifier = load_balance.get('identifier')




            load_balance_data = LoadBalancing(load_balance, strict=False)
            # route_resource = LoadBalancingResource({
            #     'region_code': region,
            #     'data': load_balance_data,
            #     'reference': ReferenceModel(load_balance_data.reference())
            # })
            #
            # self.set_region_code(region)
            # collected_cloud_services.append(LoadBalancingResponse({'resource': route_resource}))


        print(f'** Load Balancing Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services

    def get_load_balancer_infos(self, url_maps, backend_services, target_pools, forwarding_rules, project):
        load_balance_infos = []
        load_balance_infos.extend(self.get_load_balancer_from_url_maps(url_maps, backend_services, project))
        load_balance_infos.extend(self.get_load_balancer_from_target_pools(target_pools, forwarding_rules, project))

        return load_balance_infos

    def get_all_proxy_list(self, grpc_proxies, http_proxies, https_proxies, forwarding_rules):
        proxy_list = []
        all_resources = [{'type': 'grpc',
                          'source': grpc_proxies},
                         {'type': 'http',
                          'source': http_proxies},
                         {'type': 'https',
                          'source': https_proxies}]

        for resource in all_resources:
            for proxy in resource.get('source', []):
                proxy_type = resource.get('type')
                proxy_key: str = 'grpc_proxy' if proxy_type == 'grpc' else 'http_proxy' if proxy_type == 'http' else 'https_proxy '
                proxy_vo = {
                    'type': proxy_type,
                     proxy_key: proxy
                }

                proxy_list.append(TargetProxy(proxy_vo))


        return proxy_list

    def get_load_balancer_from_url_maps(self, url_maps, backend_services, project):
        load_balancer_list = []

        for url_map in url_maps:
            url_map_single_vo = {}
            region = self._get_matched_last_target('region', url_map) if url_map.get('region') else 'global'
            url_map_single_vo.update({
                'project': project,
                'region': region,
                'id': url_map.get('id'),
                'name': url_map.get('name'),
                'self_link': self._get_self_link(project, region, url_map.get('name')),
                'identifier': url_map.get('selfLink'),
                'creation_timestamp': url_map.get('creationTimestamp')
            })

            identifier = url_map.get('defaultService')
            lb_info_from_be = self._get_lb_info_from_selected_items(identifier, 'selfLink', backend_services)

            if lb_info_from_be:
                url_map_single_vo.update({
                    'protocol': self._get_list_from_str(lb_info_from_be.get('protocol')),
                    'scheme': lb_info_from_be.get('loadBalancingScheme'),
                    'port_range': self._get_list_from_str(lb_info_from_be.get('port')),
                    'network_tier': lb_info_from_be.get('networkTier')
                })

            load_balancer_list.append(url_map_single_vo)

        return load_balancer_list

    def get_load_balancer_from_target_pools(self, target_pools, forwarding_rules, project):
        load_balancer_list = []

        for target_pool in target_pools:
            target_pool_single_vo = {}
            region = self._get_matched_last_target('region', target_pool) if target_pool.get('region') else 'global'

            target_pool_single_vo.update({
                'project': project,
                'region': region,
                'id': target_pool.get('id'),
                'name': target_pool.get('name'),
                'identifier': target_pool.get('selfLink'),
                'self_link': self._get_self_link(project, region, target_pool.get('name')),
                'creation_timestamp': target_pool.get('creationTimestamp')
            })

            target_link = target_pool.get('selfLink')
            lb_info = self._get_lb_info_from_selected_items(target_link, 'target', forwarding_rules)

            if lb_info:
                target_pool_single_vo.update({
                    'protocol': self._get_list_from_str(lb_info.get('IPProtocol')),
                    'port_range': self._get_list_from_str(lb_info.get('portRange')),
                    'scheme': lb_info.get('loadBalancingScheme'),
                    'network_tier': lb_info.get('networkTier')
                })

            load_balancer_list.append(target_pool_single_vo)

        return load_balancer_list

    @staticmethod
    def _get_matched_last_target(key, source):
        a = source.get(key, '')
        return a[a.rfind('/') + 1:]

    @staticmethod
    def _get_self_link(project, region, name):
        return f'https://www.googleapis.com/compute/v1/projects/{project}/regions/{region}/load_balancing/{name}'

    @staticmethod
    def _get_zone_from_target(key, source):
        a = source.get(key, '')
        return a[a.find('zones') + 6:a.find('/instances')]

    @staticmethod
    def _get_list_from_str(target_str):
        switching_target = None
        if isinstance(target_str, int):
            switching_target = target_str
        else:
            port_range = target_str.split('-')
            switching_target = port_range[0] if len(port_range) > 1 and port_range[0] == port_range[1] else target_str\

        return switching_target if isinstance(switching_target, list) else [switching_target]



    @staticmethod
    def _get_lb_info_from_selected_items(identifier, key, selected_items):
        matched_lb_vo = None
        for selected_item in selected_items:
            if selected_item.get(key, '') == identifier:
                matched_lb_vo = selected_item
                break
        return matched_lb_vo
