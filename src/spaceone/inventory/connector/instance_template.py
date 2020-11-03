import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *


__all__ = ['InstanceTemplateConnector']
_LOGGER = logging.getLogger(__name__)


class InstanceTemplateConnector(GoogleCloudConnector):

    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instance_group_managers(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.instanceGroupManagers().list(**query).execute()
        return result.get('items', [])

    def list_machine_types(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.machineTypes().list(**query).execute()
        return result.get('items', [])

    def list_disks(self, zone,  **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.disks().list(**query).execute()
        return result.get('items', [])

    def list_instance_templates(self, **query):
        query = self.generate_query(**query)
        result = self.client.instanceTemplates().list(**query).execute()
        return result.get('items', [])