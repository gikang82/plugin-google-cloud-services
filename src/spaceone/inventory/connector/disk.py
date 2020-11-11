import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *

__all__ = ['DiskConnector']
_LOGGER = logging.getLogger(__name__)


class DiskConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_disks(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.disks().list(**query).execute()
        return result.get('items', [])

    def list_resource_policies(self, region, **query):
        query.update({'region': region})
        query = self.generate_query(**query)
        result = self.client.resourcePolicies().list(**query).execute()
        return result.get('items', [])
