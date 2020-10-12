from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, DateTimeDyField, SearchField, \
    EnumDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_instance = CloudServiceTypeResource()
cst_instance.name = 'Instance'
cst_instance.provider = 'google_cloud'
cst_instance.group = 'CloudSQL'
cst_instance.labels = ['Database']
cst_instance.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Cloud_SQL.svg',
    'spaceone:is_major': 'true',
}

cst_instance._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        EnumDyField.data_source('State', 'data.state', default_state={
            'safe': ['RUNNABLE'],
            'warning': ['PENDING_DELETE', 'PENDING_CREATE'],
            'alert': ['SUSPENDED', 'MAINTENANCE', 'FAILED'],
        }),
        TextDyField.data_source('Type', 'data.database_version'),
        TextDyField.data_source('Project', 'data.project'),
        ListDyField.data_source('Public IP Address', 'data.ip_addresses', default_badge={'type': 'outline',
                                                                                         'sub_key': 'ip_address',
                                                                                         'delimiter': '<br>'}),
        TextDyField.data_source('Location', 'data.gce_zone'),
        TextDyField.data_source('Data Disk Size (GB)', 'data.settings.data_disk_size_gb'),
    ],
    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='State', key='data.state'),
        SearchField.set(name='Type', key='data.database_version'),
        SearchField.set(name='Project', key='data.project'),
        SearchField.set(name='Region', key='data.region'),
        SearchField.set(name='Zone', key='data.gce_zone'),
        SearchField.set(name='Public IP Address', key='data.ip_addresses.ip_address'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_instance}),
]