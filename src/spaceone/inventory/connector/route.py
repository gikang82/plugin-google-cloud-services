import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.model.vpc_network.data import *
from spaceone.inventory.error import *
from pprint import pprint

__all__ = ['RouteConnector']
_LOGGER = logging.getLogger(__name__)


class RouteConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_routes(self, **query):
        query.update({'project': self.project_id})
        result = self.client.routes().list(**query).execute()
        return result.get('items', [])

    def list_instance(self, **query):
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