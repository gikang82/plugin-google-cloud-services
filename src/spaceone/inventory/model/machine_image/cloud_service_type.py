from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, \
    ListDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_machine_image = CloudServiceTypeResource()
cst_machine_image.name = 'MachineImage'
cst_machine_image.provider = 'google_cloud'
cst_machine_image.group = 'ComputeEngine'
cst_machine_image.service_code = 'ComputeEngine'
cst_machine_image.labels = ['Compute']
cst_machine_image.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Compute_Engine.svg',
}
# Basic table for
cst_machine_image._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Source Instance', 'data.machine.source_image_from'),
        TextDyField.data_source('Machine Type', 'data.machine.machine_type'),
        ListDyField.data_source('Storage location', 'data.storage_locations',
                                default_badge={'type': 'outline', 'delimiter': '<br>'}),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),

        # is_optional
        TextDyField.data_source('ID', 'data.id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),

        TextDyField.data_source('Service accounts', 'data.service_account.email', options={
            'is_optional': True
        }),
        TextDyField.data_source('Total Storage Bytes', 'data.total_storage_bytes', options={
            'is_optional': True
        }),

    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Source Image', key='data.machine.source_image_from'),
        SearchField.set(name='Disk Type', key='data.disks.tags.disk_type'),
        SearchField.set(name='Core', key='data.machine.core'),
        SearchField.set(name='Memory', key='data.machine.memory'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_machine_image}),
]
