from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_instance_group = CloudServiceTypeResource()
cst_instance_group.name = 'MachineImage'
cst_instance_group.provider = 'google_cloud'
cst_instance_group.group = 'ComputeEngine'
cst_instance_group.labels = ['Compute']
cst_instance_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Compute_Engine.svg',
    'spaceone:is_major': 'true',
}
# Basic table for
cst_instance_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Source Instance', 'data.machine.machine_display'),
        TextDyField.data_source('Machine Type', 'data.machine.machine_type'),
        ListDyField.data_source('Storage location', 'data.storage_locations',
                            default_badge={'type': 'outline', 'delimiter': '<br>'}),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Machine Type', key='data.machine.machine_type'),
        SearchField.set(name='Disk Type', key='data.disks.tags.disk_type'),
        SearchField.set(name='Core', key='data.machine.core'),
        SearchField.set(name='Memory', key='data.machine.memory'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_instance_group}),
]
