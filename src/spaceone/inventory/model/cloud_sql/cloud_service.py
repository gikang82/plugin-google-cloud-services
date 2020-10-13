from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.cloud_sql.data import Instance
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
INSTANCE
'''
# TAB - Instance
sql_meta_autoscaling = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
])

cloud_sql_meta = CloudServiceMeta.set_layouts([sql_meta_autoscaling, ])


class CloudSQLResource(CloudServiceResource):
    cloud_service_group = StringType(default='CloudSQL')


class InstanceResource(CloudSQLResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(Instance)
    _metadata = ModelType(CloudServiceMeta, default=cloud_sql_meta, serialized_name='metadata')


class InstanceResponse(CloudServiceResponse):
    resource = PolyModelType(InstanceResource)
