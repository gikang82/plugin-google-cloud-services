import time
import logging
import json

from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.connector.cloud_sql import CloudSQLConnector
from spaceone.inventory.model.cloud_sql.data import *
from spaceone.inventory.model.cloud_sql.cloud_service import *
from spaceone.inventory.model.cloud_sql.cloud_service_type import CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class CloudSQLManager(GoogleCloudManager):
    connector_name = 'CloudSQLConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug('** Cloud SQL START **')
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
            CloudServiceResponse/ErrorResourceResponse
        """

        collected_cloud_services = []
        error_responses = []
        instance_name = ""

        try:
            cloud_sql_conn: CloudSQLConnector = self.locator.get_connector(self.connector_name, **params)
            instances = cloud_sql_conn.list_instances()

            for instance in instances:
                instance_name = instance['name']
                project = instance.get('project', '')
                # Get Databases
                databases = cloud_sql_conn.list_databases(instance_name)

                # Get Users
                users = cloud_sql_conn.list_users(instance_name)
                stackdriver = self.get_stackdriver(project, instance_name)
                instance.update({
                    'stackdriver': stackdriver,
                    'display_state': self._get_display_state(instance),
                    'databases': [Database(database, strict=False) for database in databases],
                    'users': [User(user, strict=False) for user in users],
                })
                # No labels!!
                instance_data = Instance(instance, strict=False)
                instance_resource = InstanceResource({
                    'data': instance_data,
                    'region_code': instance['region'],
                    'name': instance_name,
                    'reference': ReferenceModel(instance_data.reference())
                })

                self.set_region_code(instance['region'])
                collected_cloud_services.append(InstanceResponse({'resource': instance_resource}))
        except Exception as e:
            _LOGGER.error(f'[collect_cloud_service] => {e}')
            # Database Instance name is key(= instance_id)
            error_response = self.generate_resource_error_response(e, 'CloudSQL', 'Instance', instance_name)
            error_response.append(error_response)

        _LOGGER.debug(f'** Cloud SQL Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services, error_responses

    @staticmethod
    def get_stackdriver(project, name):
        return {
            'type': 'cloudsql.googleapis.com',
            'identifier': 'database_id',
            'filters': [{
                'key': 'resource.label.database_id',
                'value': f'{project}:{name}' if project != '' else f'{name}'
            }]
        }

    @staticmethod
    def _get_display_state(instance):
        activation_policy = instance.get('settings', {}).get('activationPolicy', 'UNKNOWN')

        if activation_policy in ['ALWAYS']:
            return 'RUNNING'
        elif activation_policy in ['NEVER']:
            return 'STOPPED'
        elif activation_policy in ['ON_DEMAND']:
            return 'ON-DEMAND'
        else:
            return 'UNKNOWN'
