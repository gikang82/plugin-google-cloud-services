import logging
from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.model.vpc_network.data import *
from spaceone.inventory.error import *
from pprint import pprint
__all__ = ['LoadBalancingConnector']
_LOGGER = logging.getLogger(__name__)


class LoadBalancingConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_url_maps(self, **query):
        url_map_list = []
        query.update({'project': self.project_id})
        request = self.client.urlMaps().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, url_scoped_list in response['items'].items():
                if 'urlMaps' in url_scoped_list:
                    url_map_list.extend(url_scoped_list.get('urlMaps'))
            request = self.client.urlMaps().aggregatedList_next(previous_request=request, previous_response=response)
        return url_map_list

    def list_back_end_services(self, **query):
        backend_svc_list = []
        query.update({'project': self.project_id})
        request = self.client.backendServices().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, url_scoped_list in response['items'].items():
                if 'backendServices' in url_scoped_list:
                    backend_svc_list.extend(url_scoped_list.get('backendServices'))
            request = self.client.backendServices().aggregatedList_next(previous_request=request,
                                                                        previous_response=response)
        return backend_svc_list

    def list_target_pools(self, **query):
        target_pool_list = []
        query.update({'project': self.project_id})
        request = self.client.targetPools().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, pool_scoped_list in response['items'].items():
                if 'targetPools' in pool_scoped_list:
                    target_pool_list.extend(pool_scoped_list.get('targetPools'))
            request = self.client.targetPools().aggregatedList_next(previous_request=request,
                                                                    previous_response=response)
        return target_pool_list

    def list_forwarding_rules(self, **query):
        forwarding_rule_list = []
        query.update({'project': self.project_id})
        request = self.client.forwardingRules().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, forwarding_scoped_list in response['items'].items():
                if 'forwardingRules' in forwarding_scoped_list:
                    forwarding_rule_list.extend(forwarding_scoped_list.get('forwardingRules'))
            request = self.client.forwardingRules().aggregatedList_next(previous_request=request,
                                                                        previous_response=response)
        return forwarding_rule_list

    def list_tcp_proxies(self, **query):
        tcp_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetTcpProxies().list(**query)
        while request is not None:
            response = request.execute()
            for tcp_proxy in response.get('items', []):
                tcp_proxy_list.append(tcp_proxy)
            request = self.client.targetTcpProxies().list_next(previous_request=request, previous_response=response)
        return tcp_proxy_list

    def list_ssl_proxies(self, **query):
        ssl_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetSslProxies().list(**query)
        while request is not None:
            response = request.execute()
            for ssl_proxy in response.get('items', []):
                ssl_proxy_list.append(ssl_proxy)
            request = self.client.targetSslProxies().list_next(previous_request=request, previous_response=response)
        return ssl_proxy_list

    def list_grpc_proxies(self, **query):
        grpc_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetGrpcProxies().list(**query)
        while request is not None:
            response = request.execute()
            for grpc_proxy in response.get('items', []):
                grpc_proxy_list.append(grpc_proxy)
            request = self.client.targetGrpcProxies().list_next(previous_request=request, previous_response=response)
        return grpc_proxy_list

    def list_back_end_buckets(self, **query):
        bucket_bucket_list = []
        query.update({'project': self.project_id})
        request = self.client.backendBuckets().list(**query)
        while request is not None:
            response = request.execute()
            for backend_bucket in response.get('items', []):
                bucket_bucket_list.append(backend_bucket)
            request = self.client.backendBuckets().list_next(previous_request=request, previous_response=response)
        return bucket_bucket_list

    def list_target_http_proxies(self, **query):
        http_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetHttpProxies().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, forwarding_scoped_list in response['items'].items():
                if 'targetHttpProxies' in forwarding_scoped_list:
                    http_proxy_list.extend(forwarding_scoped_list.get('targetHttpProxies'))
            request = self.client.targetHttpProxies().aggregatedList_next(previous_request=request,
                                                                          previous_response=response)
        return http_proxy_list

    def list_target_https_proxies(self, **query):
        https_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetHttpsProxies().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, forwarding_scoped_list in response['items'].items():
                if 'targetHttpsProxies' in forwarding_scoped_list:
                    https_proxy_list.extend(forwarding_scoped_list.get('targetHttpsProxies'))
            request = self.client.targetHttpsProxies().aggregatedList_next(previous_request=request,
                                                                           previous_response=response)
        return https_proxy_list

    def list_ssl_certificates(self, **query):
        ssl_certificate_list = []
        query.update({'project': self.project_id})
        request = self.client.sslCertificates().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, forwarding_scoped_list in response['items'].items():
                if 'sslCertificates' in forwarding_scoped_list:
                    ssl_certificate_list.extend(forwarding_scoped_list.get('sslCertificates'))
            request = self.client.sslCertificates().aggregatedList_next(previous_request=request,
                                                                        previous_response=response)
        return ssl_certificate_list

    def list_backend_https_proxies(self, **query):
        https_proxy_list = []
        query.update({'project': self.project_id})
        request = self.client.targetHttpsProxies().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, forwarding_scoped_list in response['items'].items():
                if 'targetHttpsProxies' in forwarding_scoped_list:
                    https_proxy_list.extend(forwarding_scoped_list.get('targetHttpsProxies'))
            request = self.client.targetHttpsProxies().aggregatedList_next(previous_request=request,
                                                                           previous_response=response)
        return https_proxy_list