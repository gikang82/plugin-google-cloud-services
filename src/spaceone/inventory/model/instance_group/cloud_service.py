from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.instance_group.data import InstanceGroup
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
INSTANCE
'''
# TAB - Instance
instance_group_meta = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('Name', 'data.auto_scaling_group_name'),
])

instance_group_meta = CloudServiceMeta.set_layouts([instance_group_meta, ])


class ComputeEngineResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeEngine')


class InstanceGroupResource(ComputeEngineResource):
    cloud_service_type = StringType(default='InstanceGroup')
    data = ModelType(InstanceGroup)
    _metadata = ModelType(CloudServiceMeta, default=instance_group_meta, serialized_name='metadata')


class InstanceGroupResponse(CloudServiceResponse):
    resource = PolyModelType(InstanceGroupResource)
