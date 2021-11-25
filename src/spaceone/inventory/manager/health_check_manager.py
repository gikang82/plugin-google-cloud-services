import time
import logging

from spaceone.inventory.connector import HealthCheckConnector
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.health_check.data import *
from spaceone.inventory.model.health_check.cloud_service import *
from spaceone.inventory.model.health_check.cloud_service_type import CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)

class HealthCheckManager(GoogleCloudManager):
    connector_name = 'HealthCheckConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'** HealthCheck Start **')
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
            CloudServiceResponse
        """
        health_check_conn: HealthCheckConnector = self.locator.get_connector(self.connector_name, **params)
        collected_cloud_services = []
        for health_check in health_check_conn.list_health_checks():
            # No labels!!
            _LOGGER.debug(f'health_check => {health_check}')
            health_check_data = HealthCheck(health_check, strict=False)
            _LOGGER.debug(f'health_check_data => {health_check_data}')
            try:
                health_check_resource = HealthCheckResource({
                    'data': health_check_data,
                    'region_code': 'hardcoded',
                    'name': health_check_data['name'],
                    'reference': ReferenceModel(health_check_data.reference())
                })
            except Exception as e:
                _LOGGER.error(f'test => {e}')
            _LOGGER.debug(f'health_check_resource => {health_check_resource}')
            collected_cloud_services.append(HealthCheckResponse({'resource': health_check_resource}))

        _LOGGER.debug(f'** HealthCheck Finished {time.time() - start_time} Seconds **')
        _LOGGER.debug(f'collected_cloud_services : {collected_cloud_services}')
        return collected_cloud_services

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


