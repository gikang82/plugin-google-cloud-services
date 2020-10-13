import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *


__all__ = ['InstanceGroup']
_LOGGER = logging.getLogger(__name__)


class InstanceGroup(GoogleCloudConnector):

    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instance_groups(self, **query):
        query = self.generate_query(**query)
        result = self.client.instanceGroups().list(**query).execute()
        return result.get('items', [])

    def list_instance_group_managers(self, **query):
        query = self.generate_query(**query)
        result = self.client.instanceGroupManagers().list(**query).execute()
        return result.get('items', [])
