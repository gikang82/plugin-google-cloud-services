import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.model.vpc_network.data import *
from spaceone.inventory.error import *
from pprint import pprint

__all__ = ['VPCNetworkConnector']
_LOGGER = logging.getLogger(__name__)


class VPCNetworkConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instance_for_networks(self, **query):
        instance_list = []
        query.update({'project': self.project_id,
                      'includeAllScopes': False,
                      'maxResults': 500})

        request = self.client.instances().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for name, instances_scoped_list in response['items'].items():
                if 'instances' in instances_scoped_list:
                    instance_list.extend(instances_scoped_list.get('instances'))
            request = self.client.instances().aggregatedList_next(previous_request=request, previous_response=response)
        return instance_list

    def list_forwarding_rule(self, **query):
        forwarding_rule_list = []
        query.update({'project': self.project_id,
                      'includeAllScopes': False,
                      'maxResults': 500})

        request = self.client.forwardingRules().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for name, forwarding_rules_scoped_list in response['items'].items():
                if 'forwardingRules' in forwarding_rules_scoped_list:
                    forwarding_rule_list.extend(forwarding_rules_scoped_list.get('forwardingRules'))
            request = self.client.instances().aggregatedList_next(previous_request=request, previous_response=response)
        return forwarding_rule_list

    def list_networks(self, **query):
        query.update({'project': self.project_id })
        result = self.client.networks().list(**query).execute()
        return result.get('items', [])

    def list_regional_addresses(self, **query):
        query = self.generate_query(**query)
        result = self.client.addresses().aggregatedList(**query).execute()
        all_results = result.get('items', {})
        return all_results

    def list_global_addresses(self, **query):
        query = self.generate_query(**query)
        result = self.client.globalAddresses().list(**query).execute()
        return result.get('items', [])

    def list_subnetworks(self, **query):
        resource_policies = {}
        query = self.generate_query(**query)
        result = self.client.subnetworks().aggregatedList(**query).execute()
        all_results = result.get('items', {})
        for region in all_results.keys():
            if 'subnetworks' in all_results.get(region):
                resource_policies.update({
                    region: all_results.get(region).get('subnetworks', [])
                })
        return resource_policies

    def list_routes(self, **query):
        query.update({'project': self.project_id })
        result = self.client.routes().list(**query).execute()
        return result.get('items', [])

    def list_firewall(self, **query):
        query.update({'project': self.project_id })
        result = self.client.firewalls().list(**query).execute()
        return result.get('items', [])


