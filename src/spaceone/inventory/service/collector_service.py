import time
import logging
import concurrent.futures
from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.core.service import *


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            # set google cloud service manager
            # 'CloudSQLManager',
            # 'InstanceGroupManager',
            # 'InstanceTemplateManager',
            'MachineImageManager',
            'DiskManager',
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE
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
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        secret_data = params['secret_data']

        start_time = time.time()
        resource_regions = []
        collected_region_code = []

        # TODO: Thread per cloud services
        # with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
        #     print("[ EXECUTOR START ]")
        #     future_executors = []
        #     for execute_manager in self.execute_managers:
        #         print(f'@@@ {execute_manager} @@@')
        #         _manager = self.locator.get_manager(execute_manager)
        #         future_executors.append(executor.submit(_manager.collect_resources, **params))
        #
        #     for future in concurrent.futures.as_completed(future_executors):
        #         for result in future.result():
        #             collected_region = self.get_region_from_result(result.get('resource', {}))
        #
        #             if collected_region is not None and \
        #                     collected_region.get('resource', {}).get('region_code') not in collected_region_code:
        #                 resource_regions.append(collected_region)
        #                 collected_region_code.append(collected_region.get('resource', {}).get('region_code'))
        #
        #             yield result
        #
        # print(f'TOTAL TIME : {time.time() - start_time} Seconds')
        # for resource_region in resource_regions:
        #     yield resource_region

        for manager in self.execute_managers:
            _manager = self.locator.get_manager(manager)

            for resource in _manager.collect_resources(params):
                yield resource.to_primitive()
