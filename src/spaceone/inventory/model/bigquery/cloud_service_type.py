from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_sql_workspace = CloudServiceTypeResource()
cst_sql_workspace.name = 'SQLWorkspace'
cst_sql_workspace.provider = 'google_cloud'
cst_sql_workspace.group = 'BigQuery'
cst_sql_workspace.service_code = 'BigQuery'
cst_sql_workspace.is_primary = True
cst_sql_workspace.is_major = True
cst_sql_workspace.labels = ['Analytics']
cst_sql_workspace.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Big_Query.svg',
}

cst_sql_workspace._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Location', 'data.location'),
        TextDyField.data_source('Default Partition Expires', 'data.default_partition_expiration_ms_display'),
        TextDyField.data_source('Default Table Expires', 'data.default_table_expiration_ms_display'),
        EnumDyField.data_source('Visible on Console', 'data.visible_on_console', default_badge={
            'indigo.500': ['true'], 'coral.600': ['false']
        }),
        DateTimeDyField.data_source('Creation Time', 'data.creation_time'),
        DateTimeDyField.data_source('Last Modified Time', 'data.last_modified_time'),
    ],

    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Location', key='data.location'),
        SearchField.set(name='Creation Time', key='data.creation_time', data_type='datetime'),
        SearchField.set(name='Last Modified Time', key='data.last_modified_time', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_sql_workspace}),
]
