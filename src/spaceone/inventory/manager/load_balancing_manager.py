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
        load_balancers = []

        instance_groups = load_bal_conn.list_instance_groups()
        target_pools = load_bal_conn.list_target_pools()
        url_maps = load_bal_conn.list_url_maps()
        forwarding_rules = load_bal_conn.list_forwarding_rules()
        backend_services = load_bal_conn.list_back_end_services()

        backend_buckets = load_bal_conn.list_back_end_buckets()
        ssl_certificates = load_bal_conn.list_ssl_certificates()


        health_checks = load_bal_conn.list_health_checks()

        legacy_health_checks = []
        http_health_checks = load_bal_conn.list_http_health_checks()
        https_health_checks = load_bal_conn.list_https_health_checks()
        legacy_health_checks.extend(http_health_checks)
        legacy_health_checks.extend(https_health_checks)

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

        lbs_from_proxy = self.get_load_balacer_from_target_proxy(backend_services,
                                                                 selective_proxies,
                                                                 project_id)

        lbs_from_url_map = self.get_load_balancer_from_url_maps(url_maps, backend_services, backend_buckets, project_id)
        lbs_from_target_pool = self.get_load_balancer_from_target_pools(target_pools, project_id)

        load_balancers.extend(lbs_from_proxy)
        load_balancers.extend(lbs_from_url_map)
        load_balancers.extend(lbs_from_target_pool)

        for load_balancer in load_balancers:
            health_checks_vo = load_balancer.get('heath_check_vos', {})
            health_self_links = health_checks_vo.get('health_check_self_link_list', [])

            # Set Target Proxies
            if load_balancer.get('lb_type') != 'target_proxy':
                matched_target_proxies, matched_certificates = self.get_matched_target_proxies(load_balancer,
                                                                                               target_proxies,
                                                                                               ssl_certificates)
                load_balancer.update({'target_proxies': matched_target_proxies,
                                      'certificates': matched_certificates})

            # Set forwarding Rules to LoadBlancer
            matched_forwarding_rules = self.get_matched_forwarding_rules(load_balancer, forwarding_rules)
            load_balancer.update({'forwarding_rules': matched_forwarding_rules})

            # Set Health Check to LoadBlancer
            if len(health_self_links) > 0:
                filter_check_list = list(set(health_checks_vo.get('health_check_list', [])))
                filter_check_self_link_list = list(set(health_checks_vo.get('health_check_self_link_list', [])))
                matched_health_list = self._get_matched_health_checks(filter_check_self_link_list, health_checks)

                if len(matched_health_list) == len(filter_check_list):
                    load_balancer['heath_check_vos'].update({
                        'health_check_list': filter_check_list,
                        'health_check_self_link_list': filter_check_self_link_list,
                        'health_checks': matched_health_list
                    })
                else:
                    matched_health_legacy_list = self._get_matched_health_checks(filter_check_self_link_list,
                                                                                 legacy_health_checks)
                    matched_health_list.extend(matched_health_legacy_list)
                    load_balancer['heath_check_vos'].update({
                        'health_check_list': filter_check_list,
                        'health_check_self_link_list': filter_check_self_link_list,
                        'health_checks': matched_health_list
                    })

            # Set Front to LoadBlancer
            frontends = self.get_front_from_loadbalancer(load_balancer)
            if len(frontends) > 0:
                load_balancer.update({'frontends': frontends})




            load_balance_data = LoadBalancing(load_balancer, strict=False)
            npn = load_balancer.get('name')
            print('#########################')
            print(f'LOAD BALANCER: {npn}')
            print('#########################')
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
            health_check_list = self._get_health_checks_from_backend_svc(backend_svc_list)
            backend_bucktet_list = self._get_lb_info_from_selected_items(identifiers, 'selfLink', backend_buckets)
            host_and_path_rules = self.get_matched_host_and_path(url_map)

            url_map_single_vo.update({
                'lb_type': 'url_map',
                'project': project,
                'region': region,
                'id': url_map.get('id'),
                'description': url_map.get('description', ''),
                'name': url_map.get('name'),
                'self_link': self._get_self_link(project, region, url_map.get('name')),
                'identifier': url_map.get('selfLink'),
                'heath_check_vos': {
                    'health_check_list': self._get_matched_last_target_in_list(health_check_list),
                    'health_check_self_link_list': health_check_list,
                },
                'backend_services': backend_svc_list,
                'backend_buckets': backend_bucktet_list,
                'host_and_paths': host_and_path_rules,
                'creation_timestamp': url_map.get('creationTimestamp')
            })

            load_balancer_list.append(url_map_single_vo)

        return load_balancer_list

    def get_load_balancer_from_target_pools(self, target_pools, project):
        load_balancer_list = []

        for target_pool in target_pools:
            region = self._get_matched_last_target('region', target_pool) if target_pool.get('region') else 'global'
            health_checks = target_pool.get('healthChecks', [])
            target_pool_vo = {
                'lb_type': 'target_pool',
                'project': project,
                'region': region,
                'description': target_pool.get('description'),
                'id': target_pool.get('id'),
                'name': target_pool.get('name'),
                'heath_check_vos': {
                    'health_check_list': self._get_matched_last_target_in_list(health_checks),
                    'health_check_self_link_list': health_checks,
                },
                'identifier': target_pool.get('selfLink'),
                'self_link': self._get_self_link(project, region, target_pool.get('name')),
                'creation_timestamp': target_pool.get('creationTimestamp'),
                'target_pools': [TargetPools(target_pool, strict=False)]
            }

            load_balancer_list.append(target_pool_vo)

        return load_balancer_list

    def get_load_balacer_from_target_proxy(self, backends, selective_proxies, project):
        backend_proxies = []

        for ssl_tcp_proxy in selective_proxies:
            key = 'tcp_proxy' if 'tcp_proxy' in ssl_tcp_proxy else 'ssl_proxy'
            proxy_info = ssl_tcp_proxy.get(key, {})
            region = self._extract_region_from_proxy(proxy_info.get('selfLink'), project)
            for backend in backends:
                health_checks = backend.get('healthChecks', [])
                if backend.get('selfLink') == proxy_info.get('service', ''):
                    backend_proxy_vo = {
                        'lb_type': 'target_proxy',
                        'project': project,
                        'id': proxy_info.get('id'),
                        'region': region,
                        'name': proxy_info.get('name'),
                        'self_link': self._get_self_link(project, region, proxy_info.get('name')),
                        'heath_check_vos': {
                            'health_check_list': self._get_matched_last_target_in_list(health_checks),
                            'health_check_self_link_list': health_checks,
                        },
                        'identifier': proxy_info.get('selfLink'),
                        'creation_timestamp': proxy_info.get('creationTimestamp'),
                        'target_proxies': [ssl_tcp_proxy],
                        'backend_services': [backend]
                    }

                    backend_proxies.append(backend_proxy_vo)

        return backend_proxies

    def get_matched_forwarding_rules(self, loadbalancer, forwarding_rules):
        matched_forwarding_rules = []
        lb_type = loadbalancer.get('lb_type')

        # It's difficult to predict what's lb_type for forwarding_rules
        if lb_type == 'target_pool':
            for forwarding_rule in forwarding_rules:
                if loadbalancer.get('identifier') == forwarding_rule.get('target'):
                    matched_forwarding_rules.append(forwarding_rule)

        elif lb_type in ['url_map', 'target_proxy']:
            self_links = self._get_self_links_from_proxies(loadbalancer.get('target_proxies', []))
            for forwarding_rule in forwarding_rules:
                if forwarding_rule.get('target') in self_links:
                    matched_forwarding_rules.append(forwarding_rule)

        return matched_forwarding_rules

    def get_matched_target_proxies(self, lb, target_proxies, certs):
        matched_target_proxies = []
        matched_certificate = []
        for target_proxy in target_proxies:
            key = target_proxy.get('proxy_key')
            proxy_info = target_proxy.get(key, {})
            if 'urlMap' in proxy_info:
                if proxy_info.get('urlMap') == lb.get('identifier'):
                    if 'sslCertificates' in proxy_info:
                        matching_ones = self._get_matched_certificates(certs, proxy_info.get('sslCertificates', []))
                        matched_certificate.extend(matching_ones)
                    matched_target_proxies.append(target_proxy)

        return matched_target_proxies, matched_certificate

    def get_matched_host_and_path(self, target_item):

        host_and_path_rules = []

        if 'defaultService' in target_item:
            host_and_path_rules.append({
                'host': ['All unmatched (default)'],
                'path': ['All unmatched (default)'],
                'backend': self._get_matched_last_target('defaultService', target_item)
            })

        if 'hostRules' in target_item:
            host_rule_map = {}
            for host_rule in target_item.get('hostRules', []):
                host_rule_map[host_rule.get('pathMatcher')] = {'host': host_rule.get('hosts', [])}

            for path_matcher in target_item.get('pathMatchers', []):
                _name = path_matcher.get('name', '')
                default_service = path_matcher.get('defaultService')
                if default_service:
                    host_and_path_rules.append({
                        'host': host_rule_map.get(_name, {}).get('host'),
                        'path': ['/*'],
                        'backend': self._get_matched_last_target('defaultService', target_item)
                    })

                for path_rule in path_matcher.get('pathRules', []):
                    host_and_path_rules.append({
                        'host': host_rule_map.get(_name, {}).get('host'),
                        'path': path_rule.get('paths', []),
                        'backend': self._get_matched_last_target('service', path_rule)
                    })

        return host_and_path_rules

    def get_front_from_loadbalancer(self, loadbalancer):
        frontends = []

        proxies = loadbalancer.get('target_proxies', [])
        pools = loadbalancer.get('target_pools', [])

        for forwarding_rule in loadbalancer.get('forwarding_rules', []):

            target = forwarding_rule.get('target', '')
            ports = forwarding_rule.get('ports', [])
            region = 'global' if forwarding_rule.get('region') is None else forwarding_rule.get('region')
            _region = region[region.rfind('/') + 1:]

            if not proxies:
                print('!!!!!!!!!!!!!!!!!')
                for pool in pools:
                    if target == pool.get('self_link'):
                        front_single = {
                            'name': forwarding_rule.get('name'),
                            'protocols': forwarding_rule.get('IPProtocol').upper(),
                            'scope': 'Global' if region == 'global' else f'Regional ({_region})',
                            'region': _region,
                            'ip_address': forwarding_rule.get('IPAddress'),
                            'port': self._get_list_from_str(
                                forwarding_rule.get('portRange')) if not ports else self._get_list_from_str(ports),
                            'network_tier': forwarding_rule.get('networkTier').capitalize()
                        }
                        frontends.append(front_single)
            else:
                for proxy in proxies:
                    key = proxy.get('proxy_key', '')
                    proxy_vo = proxy.get(key)
                    if target == proxy_vo.get('selfLink'):
                        front_single = {
                            'name': forwarding_rule.get('name'),
                            'protocols': proxy.get('type').upper(),
                            'scope': 'Global' if region == 'global' else f'Regional ({_region})',
                            'region': _region,
                            'ip_address': forwarding_rule.get('IPAddress'),
                            'port': self._get_list_from_str(
                                forwarding_rule.get('portRange')) if not ports else self._get_list_from_str(ports),
                            'network_tier': forwarding_rule.get('networkTier').capitalize()
                        }

                        if 'sslCertificates' in proxy_vo:
                            front_single.update({'certificate': self._get_matched_last_target_in_list(proxy_vo.get('sslCertificates'))})

                        frontends.append(front_single)

        return frontends

    @staticmethod
    def _get_matched_certificates(certs, ssl_certificates):
        certificates = []
        for cert in certs:
            if cert.get('selfLink', '') in ssl_certificates:
                certificates.append(cert)
        return certificates

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
    def _get_self_links_from_proxies(target_proxies):
        self_link_list = []
        for proxy in target_proxies:
            key = proxy.get('proxy_key')
            self_link = proxy.get(key, {}).get('selfLink')
            if self_link:
                self_link_list.append(self_link)
        return self_link_list

    @staticmethod
    def _get_matched_last_target(key, source):
        a = source.get(key, '')
        return a[a.rfind('/') + 1:]

    @staticmethod
    def _get_matched_last_target_in_list(target_list):
        matched_links_vos = []
        for target_item in target_list:
            a = target_item
            matched_links_vos.append(a[a.rfind('/') + 1:])
        return matched_links_vos

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
            switching_target = port_range[0] if len(port_range) > 1 and port_range[0] == port_range[1] else target_str
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
        p_len = len(project) + 1
        p_key = f'{project}/'
        _region = self_link[self_link.find(p_key) + p_len:]
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

    @staticmethod
    def _get_matched_health_checks(self_link_list, health_checks):
        health_check_list = []
        for health_check in health_checks:
            if health_check.get('selfLink', '') in self_link_list:
                health_check_list.append(health_check)
        return health_check_list

    @staticmethod
    def _get_health_checks_from_backend_svc(backend_svcs):
        health_check_list = []
        for backend_svc in backend_svcs:
            if len(backend_svc.get('healthChecks', [])) > 0:
                health_check_list.extend(backend_svc.get('healthChecks'))
        return health_check_list
