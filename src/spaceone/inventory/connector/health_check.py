import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *

__all__ = ['HealthCheckConnector']
_LOGGER = logging.getLogger(__name__)


class HealthCheckConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_health_checks(self, **query):
        health_checks_list = []
        query.update({'project': self.project_id})
        _LOGGER.debug(f'start query health check resources : {self.project_id}')
        request = self.client.healthChecks().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            _LOGGER.debug(f'healthChecks().aggregatedList : {response}')
            for key, _health_check_list in response['items'].items():
                if 'healthChecks' in _health_check_list:
                    health_checks_list.extend(_health_check_list.get('healthChecks'))
            request = self.client.healthChecks().aggregatedList_next(previous_request=request, previous_response=response)

        _LOGGER.debug(f'list_health_checks results : {health_checks_list}')
        return health_checks_list

