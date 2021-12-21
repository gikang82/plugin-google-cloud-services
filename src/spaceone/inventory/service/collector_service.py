import time
import logging
import json
import concurrent.futures

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.core.service import *
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)

@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        # set google cloud service manager
        self.execute_managers = []
        '''
        self.execute_managers = [
            'BigQueryManager',
            'CloudSQLManager',
            'InstanceGroupManager',
            'InstanceTemplateManager',
            'MachineImageManager',
            'DiskManager',
            'SnapshotManager',
            'StorageManager',
            'VPCNetworkManager',
            'ExternalIPAddressManager',
            'FirewallManager',
            'RouteManager',
            'LoadBalancingManager'
        ]
        '''

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})
        if secret_data != {}:
            google_manager = GoogleCloudManager()
            active = google_manager.verify({}, secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        _LOGGER.debug(f'EXECUTOR START: Google Cloud Service')
        # Get target manager to collect
        try:
            self.execute_managers = self._get_target_execute_manager(params.get('options', {}))
            _LOGGER.debug(f'[collect] execute_managers => {self.execute_managers}')
        except Exception as e:
            _LOGGER.error(f'[collect] failed to get target execute_managers => {e}', exc_info=True)
            error_resource_response = self.generate_error_response(e, '', 'inventory.Error')
            yield error_resource_response.to_primitive()

        # Execute manager
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []
            for execute_manager in self.execute_managers:

                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for result in future.result():
                        yield result.to_primitive()
                except Exception as e:
                    _LOGGER.error(f'[collect] failed to yield result => {e}', exc_info=True)
                    error_resource_response = self.generate_error_response(e, '', 'inventory.Error')
                    yield error_resource_response.to_primitive()

        _LOGGER.debug(f'TOTAL TIME : {time.time() - start_time} Seconds')

    def _get_target_execute_manager(self, options):
        if 'cloud_service_types' in options:
            execute_managers = self._match_execute_manager(options['cloud_service_types'])
        else:
            execute_managers = list(CLOUD_SERVICE_GROUP_MAP.values())

        return execute_managers

    @staticmethod
    def _match_execute_manager(cloud_service_types):
        target_cloud_service_types = []
        for cloud_service_type in cloud_service_types:
            if cloud_service_type in CLOUD_SERVICE_GROUP_MAP:
                target_cloud_service_types.append(CLOUD_SERVICE_GROUP_MAP[cloud_service_type])

        return target_cloud_service_types

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})

        return error_resource_response

# Not used function
    def _set_regions_zones(self, secret_data, params):
        result_regions = []
        result_zones = []
        query = {}
        try:
            connector: GoogleCloudConnector = self.locator.get_connector('GoogleCloudConnector', secret_data=secret_data)
            zones = connector.list_zones(**query)

            for zone in zones:
                result_zones.append(zone.get('name'))

                if region := zone.get('region'):
                    result_regions.append(region.split('/')[-1])

            params.update({'region': list(set(result_regions)), 'zone': result_zones})
        except Exception as e:
            _LOGGER.error(f'failed to _set_regions_zones {e}', exc_info=True)
