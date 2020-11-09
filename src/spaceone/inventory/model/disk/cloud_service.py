from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.disk.data import Disk
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
INSTANCE
'''

disk_properties_meta = ItemDynamicLayout.set_fields('Instance', fields=[
    TextDyField.data_source('ID', 'data.id'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('Disk Type', 'data.type',
                            default_outline_badge=['local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard']),
    TextDyField.data_source('Size', 'data.size_display'),
    TextDyField.data_source('Zone', 'data.zone'),
    ListDyField.data_source('In Used By', 'data.in_used_by',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
    ListDyField.data_source('Snapshot Schedule', 'data.snapshot_schedule',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
    EnumDyField.data_source('Encryption Type', 'encryption', default_badge={
        'primary': ['Google managed'], 'indigo.500': ['Customer managed'], 'coral.600': ['Customer supplied']
    }),
    TextDyField.data_source('Source Image', 'data.source_image_display'),
    DateTimeDyField.data_source('Last Attach Time', 'data.lastAttachTimestamp'),
    DateTimeDyField.data_source('Last Detach Time', 'data.lastDetachTimestamp'),
    DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
])

# TAB - Instance Group
disk_performance_meta = ItemDynamicLayout.set_fields('Estimated Performance', fields=[
    TextDyField.data_source('Read IOPS', 'tags.read_iops'),
    TextDyField.data_source('Write IOPS', 'tags.write_iops'),
    TextDyField.data_source('Read Throughput(MB/s)', 'tags.read_throughput'),
    TextDyField.data_source('Write Throughput(MB/s)', 'tags.write_throughput'),
])

meta_disk_template = ListDynamicLayout.set_layouts('Disks', layouts=[disk_properties_meta, disk_performance_meta])

it_meta_labels = TableDynamicLayout.set_fields('Labels', root_path='data.labels', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

disk_meta = CloudServiceMeta.set_layouts([meta_disk_template, it_meta_labels])


class ComputeEngineResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeEngine')


class DiskResource(ComputeEngineResource):
    cloud_service_type = StringType(default='StorageDisk')
    data = ModelType(Disk)
    _metadata = ModelType(CloudServiceMeta, default=disk_meta, serialized_name='metadata')


class DiskResponse(CloudServiceResponse):
    resource = PolyModelType(DiskResource)