from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.cloud_sql.data import *
from spaceone.inventory.model.cloud_sql.cloud_service import *
from spaceone.inventory.model.cloud_sql.cloud_service_type import CLOUD_SERVICE_TYPES


class CloudSQLManager(GoogleCloudManager):
    connector_name = 'CloudSQL'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        Response:
            CloudServiceResponse
        """

        cloud_sql_conn = self.locator.get_connector(self.connector_name, **params)

        for instance in cloud_sql_conn.list_instances():
            instance_data = Instance(instance, strict=False)

            instance_resource = InstanceResource({
                'data': instance_data,
                'region_code': instance['region'],
                'reference': ReferenceModel(instance_data.reference())
            })

            self.set_region_code(instance['region'])
            yield InstanceResponse({'resource': instance_resource})
