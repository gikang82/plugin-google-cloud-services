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
        instance_list = []
        query.update({'project': self.project_id})
        request = self.client.instances().list(**query)
        while request is not None:
            response = request.execute()
            for instance in response.get('items', []):
                instance_list.append(instance)
            request = self.client.instances().list_next(previous_request=request, previous_response=response)

        return instance_list

    def list_databases(self, instance_name, **query):
        database_list = []
        query.update({'project': self.project_id,
                      'instance': instance_name})

        request = self.client.databases().list(**query)
        while request is not None:
            try:
                response = request.execute()
                for database in response.get('items', []):
                    database_list.append(database)
                request = self.client.instances().list_next(previous_request=request, previous_response=response)
            except Exception as e:
                request = None
                _LOGGER.error(f'Error occurred at CloudSQLConnector: databases().list(**query) : skipped \n {e}')

        return database_list

    def list_users(self, instance_name, **query):
        user_list = []
        query.update({'project': self.project_id, 'instance': instance_name})
        try:
            response = self.client.users().list(**query).execute()
            user_list = response.get('items', [])
        except Exception as e:
            _LOGGER.error(f'Error occurred at users().list(**query) : skipped \n {e}')

        return user_list

    def list_backup_runs(self, instance_name, **query):
        backup_runs_list = []
        query.update({'project': self.project_id, 'instance': instance_name})
        request = self.client.backup_runs().list(**query)

        while request is not None:
            try:
                response = request.execute()
                for backup in response.get('items', []):
                    backup_runs_list.append(backup)
                request = self.client.backup_runs().list_next(previous_request=request, previous_response=response)
            except Exception as e:
                request = None
                _LOGGER.error(f'Error occurred at CloudSQLConnector: backup_runs().list(**query) : skipped \n {e}')

        return backup_runs_list