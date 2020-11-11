from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, ListDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_instance_group = CloudServiceTypeResource()
cst_instance_group.name = 'Disk'
cst_instance_group.provider = 'google_cloud'
cst_instance_group.group = 'ComputeEngine'
cst_instance_group.labels = ['Compute']
cst_instance_group.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Compute_Engine.svg',
    'spaceone:is_major': 'false',
}

cst_instance_group._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('ID', 'data.id'),
        TextDyField.data_source('Zone', 'data.zone'),
        TextDyField.data_source('Source Image', 'data.source_image_display'),
        EnumDyField.data_source('Disk Type', 'data.disk_type',
                                default_outline_badge=['local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard']),
        ListDyField.data_source('In Used By', 'data.in_used_by',
                                default_badge={'type': 'outline', 'delimiter': '<br>'}),
        ListDyField.data_source('Snapshot Schedule', 'data.snapshot_schedule_display',
                                default_badge={'type': 'outline', 'delimiter': '<br>'}),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Status', key='data.status'),
        SearchField.set(name='Disk Type', key='data.disk_type'),
        SearchField.set(name='Project', key='data.project'),
        SearchField.set(name='Zone', key='data.zone'),
        SearchField.set(name='Region', key='region_code'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_instance_group}),
]
