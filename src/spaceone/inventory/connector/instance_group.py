import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *


__all__ = ['InstanceGroupConnector']
_LOGGER = logging.getLogger(__name__)


class InstanceGroupConnector(GoogleCloudConnector):

    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instance_groups(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.instanceGroups().list(**query).execute()
        return result.get('items', [])

    def list_instance_group_managers(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.instanceGroupManagers().list(**query).execute()
        return result.get('items', [])

    def list_instances(self, zone, instance_group, **query):
        query.update({'zone': zone, 'instanceGroup': instance_group})
        query = self.generate_query(**query)
        result = self.client.instanceGroups().listInstances(**query).execute()
        return result.get('items', [])

    def list_autoscalers(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.autoscalers().list(**query).execute()
        return result.get('items', [])

    def list_instance_templates(self, **query):
        query = self.generate_query(**query)
        result = self.client.instanceTemplates().list(**query).execute()
        return result.get('items', [])
