import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *


__all__ = ['CloudSQLConnector']
_LOGGER = logging.getLogger(__name__)


class CloudSQLConnector(GoogleCloudConnector):

    google_client_service = 'sqladmin'
    version = 'v1beta4'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instances(self, **query):
        query = self.generate_query(**query)
        result = self.client.instances().list(**query).execute()
        return result.get('items', [])

    def list_databases(self, instance_name, **query):
        query.update({'instance': instance_name})
        query = self.generate_query(**query)
        result = {}
        try:
            result = self.client.databases().list(**query).execute()
        except Exception as e:
            print(e)
            pass
        return result.get('items', [])

    def list_users(self, instance_name, **query):
        query.update({'instance': instance_name})
        query = self.generate_query(**query)
        result = {}
        try:
            result = self.client.users().list(**query).execute()
        except Exception as e:
            print(e)
            pass
        return result.get('items', [])

    def list_backup_runs(self, instance_name, **query):
        query.update({'instance': instance_name})
        query = self.generate_query(**query)
        result = {}
        try:
            result = self.client.backup_runs().list(**query).execute()
        except Exception as e:
            print(e)
            pass
        return result.get('items', [])
