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

        instance_groups = load_bal_conn.list_instance_groups()
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
        ssl_proxies = load_bal_conn.list_ssl_proxies()
        tcp_proxies = load_bal_conn.list_tcp_proxies()

        target_proxies, selective_proxies = self.get_all_proxy_list(grpc_proxies,
                                                                   http_proxies,
                                                                   https_proxies,
                                                                   ssl_proxies,
                                                                   tcp_proxies,
                                                                   forwarding_rules)

        # print('####################################')
        # print()
        # pprint(target_proxies)
        # print()

        loadbalancers = []

        lbs_from_proxy = self.get_load_balacer_from_target_proxy(backend_services,
                                                selective_proxies,
                                                project_id)
        loadbalancers.extend(lbs_from_proxy)

        lbs_from_url_map = self.get_load_balancer_from_url_maps(url_maps, backend_services, backend_buckets, project_id)

        loadbalancers.extend(lbs_from_url_map)
        lbs_from_target_pool =  self.get_load_balancer_from_target_pools(target_pools, project_id)

        loadbalancers.extend(lbs_from_target_pool)

        print()
        print('##################################')
        print(f'number of loadbalancer: {len(loadbalancers)}')
        print('##################################')
        print()

        for load_balancer in loadbalancers:
            # Set Target Proxies
            if load_balancer.get('lb_type') != 'target_proxy':
                matched_target_proxies = self.get_matched_target_proxies(load_balancer, target_proxies)
                load_balancer.update({'target_proxies': matched_target_proxies})

            # Set BackEnd Services and Backend Buckets
            if load_balancer.get('lb_type') != 'target_proxy':
                if load_balancer.get('lb_type') == 'target_pool':
                    print()



            load_balance_data = LoadBalancing(load_balancer, strict=False)
            print('LB:load_balancer')
            print('#####################')
            print()
            pprint(load_balance_data.to_primitive())
            print()
            print()



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

    def get_all_proxy_list(self, grpc_proxies, http_proxies, https_proxies, ssl_proxies, tcp_proxies, forwarding_rules):
        proxy_list = []
        proxy_list_relate_to_load_balancer = []

        all_resources = [{'type': 'grpc',
                          'source': grpc_proxies},
                         {'type': 'http',
                          'source': http_proxies},
                         {'type': 'https',
                          'source': https_proxies},
                         {'type': 'ssl',
                          'source': ssl_proxies},
                         {'type': 'tcp',
                          'source': tcp_proxies}
                         ]

        for resource in all_resources:
            for proxy in resource.get('source', []):

                proxy_type = resource.get('type')
                proxy_key: str = self._get_proxy_key(resource.get('type'))
                in_used_by, in_used_by_display = self._get_in_used_by_forwarding_rule(proxy, forwarding_rules)

                proxy_vo = {
                    proxy_key: proxy,
                    'proxy_key': proxy_key,
                    'type': proxy_type,
                    'name': proxy.get('name', ''),
                    'description': proxy.get('description', ''),
                    'target_resource': {},
                    'in_used_by': in_used_by,
                    'target_proxy_display': {
                        'name': proxy.get('name', ''),
                        'description': proxy.get('description', ''),
                        'type': f'{proxy_type.upper()} Proxy',
                        'target_resource': self._get_matched_last_target('urlMap', proxy),
                        'in_used_by_display': in_used_by_display
                    },
                }
                if proxy_type in ['ssl', 'tcp']:
                    proxy_list_relate_to_load_balancer.append(proxy_vo)
                proxy_list.append(proxy_vo)
                #     proxy_list_relate_to_load_balancer.append(TargetProxy(proxy_vo, strict=False))
                # proxy_list.append(TargetProxy(proxy_vo, strict=False))

        return proxy_list, proxy_list_relate_to_load_balancer

    def get_load_balancer_from_url_maps(self, url_maps, backend_services, backend_buckets, project):
        load_balancer_list = []

        for url_map in url_maps:
            region = self._get_matched_last_target('region', url_map) if url_map.get('region') else 'global'
            url_map_single_vo = {}
            identifiers = self._get_matched_services(url_map)
            backend_svc_list = self._get_lb_info_from_selected_items(identifiers, 'selfLink', backend_services)
            backend_bucktet_list = self._get_lb_info_from_selected_items(identifiers, 'selfLink', backend_buckets)
            url_map_single_vo.update({
                'lb_type': 'url_map',
                'project': project,
                'region': region,
                'id': url_map.get('id'),
                'name': url_map.get('name'),
                'self_link': self._get_self_link(project, region, url_map.get('name')),
                'identifier': url_map.get('selfLink'),
                'backend_services': backend_svc_list,
                'backend_buckets': backend_bucktet_list,
                'creation_timestamp': url_map.get('creationTimestamp')
            })

            load_balancer_list.append(url_map_single_vo)

        return load_balancer_list

    def get_load_balancer_from_target_pools(self, target_pools, project):
        load_balancer_list = []

        for target_pool in target_pools:
            region = self._get_matched_last_target('region', target_pool) if target_pool.get('region') else 'global'
            target_pool_vo = {
                'lb_type': 'target_pool',
                'project': project,
                'region': region,
                'description': target_pool.get('description'),
                'id': target_pool.get('id'),
                'name': target_pool.get('name'),
                'identifier': target_pool.get('selfLink'),
                'self_link': self._get_self_link(project, region, target_pool.get('name')),
                'creation_timestamp': target_pool.get('creationTimestamp'),
                'target_pools': [TargetPools(target_pool, strict=False)]
            }

            load_balancer_list.append(target_pool_vo)

        return load_balancer_list

    def get_matched_front_end(self, load_balancer, proxies, forwarding_rule):
        front_ends = []
        lb_type = load_balancer.get('lb_type')
        identity = load_balancer.get('identifier')

        for forwarding_rule in forwarding_rule:
            if lb_type == 'target_pool':
                if identity == forwarding_rule.get('target'):
                    region = self._get_matched_last_target('region', forwarding_rule)
                    front_ends.append({
                        'id': forwarding_rule.get('id'),
                        'name': forwarding_rule.get('name'),
                        'region': 'global' if region == '' else region,
                        'load_balancing_scheme': forwarding_rule.get('loadBalancingScheme'),
                        'network_tier': forwarding_rule.get('networkTier'),
                    })
            elif lb_type == 'url_map':
                pass
            else:
                pass

        return front_ends

    def get_matched_target_proxies(self, lb, target_proxies):
        matched_target_proxies = []
        for target_proxy in target_proxies:
            key = target_proxy.get('proxy_key')
            proxy_info = target_proxy.get(key, {})
            if 'urlMap' in proxy_info:
                if proxy_info.get('urlMap') == lb.get('identifier'):
                    matched_target_proxies.append(target_proxy)
        return matched_target_proxies

    @staticmethod
    def _get_matched_services(target_item):
        matching_item_self_links = []
        if 'defaultService' in target_item:
            matching_item_self_links.append(target_item.get('defaultService'))

        if 'pathMatchers' in target_item and isinstance(target_item.get('pathMatchers'), list):
            for path_matcher in target_item.get('pathMatchers'):
                if path_matcher.get('defaultService', '') not in matching_item_self_links:
                    matching_item_self_links.append(path_matcher.get('defaultService', ''))

                if 'pathRules' in path_matcher and isinstance(path_matcher.get('pathRules'), list):
                    for rule in path_matcher.get('pathRules'):
                        if rule.get('service') not in matching_item_self_links:
                            matching_item_self_links.append(rule.get('service'))

        return matching_item_self_links
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
    def _get_in_used_by_forwarding_rule(target_proxy, forwarding_rules):
        in_used_by = []
        in_used_by_display = []
        for forwarding_rule in forwarding_rules:
            if forwarding_rule.get('target') == target_proxy.get('selfLink'):
                in_used_by.append({
                    'id': forwarding_rule.get('id', ''),
                    'name': forwarding_rule.get('name', ''),
                    'self_link': forwarding_rule.get('selfLink', ''),
                })

                in_used_by_display.append(forwarding_rule.get('name', ''))

        return in_used_by, in_used_by_display

    def get_load_balacer_from_target_proxy(self, backends, selective_proxies, project):
        backend_proxies = []

        for ssl_tcp_proxy in selective_proxies:
            key = 'tcp_proxy' if 'tcp_proxy' in ssl_tcp_proxy else 'ssl_proxy'
            proxy_info = ssl_tcp_proxy.get(key, {})
            region = self._extract_region_from_proxy(proxy_info.get('selfLink'), project)
            for backend in backends:

                if backend.get('selfLink') == proxy_info.get('service', ''):
                    backend_proxy_vo = {
                        'lb_type': 'target_proxy',
                        'project': project,
                        'id': proxy_info.get('id'),
                        'region': region,
                        'name': proxy_info.get('name'),
                        'self_link': self._get_self_link(project, region, proxy_info.get('name')),
                        'identifier': proxy_info.get('selfLink'),
                        'creation_timestamp': proxy_info.get('creationTimestamp'),
                        'target_proxies': [ssl_tcp_proxy],
                        'backend_services': [backend]
                    }

                    backend_proxies.append(backend_proxy_vo)

        return backend_proxies

    @staticmethod
    def _get_matching_target_proxy(loadbalancer, all_proxies):
        target_proxies = []

        for proxy in all_proxies:
            proxy_key: str = 'grpc_proxy' if 'grpc_proxy' in proxy \
                else 'http_proxy' if 'http_proxy' in proxy else 'https_proxy'
            selected_px = proxy.get(proxy_key, {}).get('url_map', '')
            if selected_px == loadbalancer.get('identifier', ''):
                proxy['target_resource'].update({
                    'id': loadbalancer.get('id'),
                    'name': loadbalancer.get('name'),
                    'self_link': loadbalancer.get('identifier')
                })
                target_proxies.append(proxy)
        return target_proxies

    @staticmethod
    def _extract_region_from_proxy(self_link, project):
        p_len = len(project)+1
        p_key = f'{project}/'
        _region = self_link[self_link.find(p_key)+p_len:]
        return _region[:_region.find('/')]

    @staticmethod
    def _get_proxy_key(proxy_type):
        proxy_key = 'tcp_proxy'
        if proxy_type == 'grpc':
            proxy_key = 'grpc_proxy'
        elif proxy_type == 'http':
            proxy_key = 'http_proxy'
        elif proxy_type == 'https':
            proxy_key = 'https_proxy'
        elif proxy_type == 'ssl':
            proxy_key = 'ssl_proxy'
        return proxy_key

    @staticmethod
    def _get_lb_info_from_selected_items(identifier, key, selected_items):
        matched_lb_vo = []
        for selected_item in selected_items:
            if selected_item.get(key, '') in identifier:
                matched_lb_vo.append(selected_item)
        return matched_lb_vo

