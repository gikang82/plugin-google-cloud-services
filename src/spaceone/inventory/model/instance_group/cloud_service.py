from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.instance_group.data import InstanceGroup
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
INSTANCE
'''
# TAB - Instance Group
instance_group_meta = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Instance Counts', 'data.instance_counts'),
    TextDyField.data_source('Template', 'data.template.name'),
    TextDyField.data_source('Autoscaling', 'data.auto_scaler.name'),
    TextDyField.data_source('Zone', 'data.zone'),
    DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
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
