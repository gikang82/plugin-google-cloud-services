from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_instance_group = CloudServiceTypeResource()
cst_instance_group.name = 'InstanceTemplate'
cst_instance_group.provider = 'google_cloud'
cst_instance_group.group = 'ComputeEngine'
cst_instance_group.labels = ['Compute']
cst_instance_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Compute_Engine.svg',
    'spaceone:is_major': 'false',
}
# Basic table for
cst_instance_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Machine Type', 'data.machine.machine_display'),
        TextDyField.data_source('Image', 'data.image'),
        TextDyField.data_source('Disk Type', 'data.disk_display'),
        ListDyField.data_source('In Used By', 'data.in_used_by',
                                default_badge={'type': 'outline', 'delimiter': '<br>'}),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Machine Type', key='data.machine.machine_type'),
        SearchField.set(name='Image', key='data.image'),
        SearchField.set(name='Disk Type', key='data.disk_display'),
        SearchField.set(name='In Use By', key='data.in_used_by'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_instance_group}),
]
