import time
import logging
import json
import concurrent.futures

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.core.service import *
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        # set google cloud service manager
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []
            for execute_manager in self.execute_managers:

                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))
        #
            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for result in future.result():
                        yield result.to_primitive()
                except Exception as e:
                    _LOGGER.error(f'failed to yield result => {e}')

                    if type(e) is dict:
                        error_resource_response = ErrorResourceResponse(
                            {'message': json.dumps(e), 'resource': {'resource_type': 'inventory.Error'}}
                        )
                        _LOGGER.error(f'error response => {error_resource_response.to_primitive()}')
                    else:
                        error_resource_response = ErrorResourceResponse(
                            {'message': str(e), 'resource': {'resource_type': 'inventory.Error'}}
                        )
                        _LOGGER.error(f'error response => {error_resource_response.to_primitive()}')

                    yield error_resource_response.to_primitive()

        _LOGGER.debug(f'TOTAL TIME : {time.time() - start_time} Seconds')

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
            _LOGGER.error(f'failed to _set_regions_zones {e}')
