from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

cst_load_balancing = CloudServiceTypeResource()
cst_load_balancing.name = 'LoadBalancing'
cst_load_balancing.provider = 'google_cloud'
cst_load_balancing.group = 'NetworkService'
cst_load_balancing.service_code = 'netservice'
cst_load_balancing.is_primary = True
cst_load_balancing.is_major = True
cst_load_balancing.labels = ['Networking']
cst_load_balancing.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Load_Balancing.svg',
}

cst_load_balancing._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Name', 'data.name'),
        TextDyField.data_source('Number of Subnet', 'data.subnetwork_data.total_number'),
        TextDyField.data_source('Maximum transmission unit', 'data.mtu'),
        TextDyField.data_source('Mode', 'data.subnet_creation_mode'),
        EnumDyField.data_source('Global Dynamic Routing', 'data.global_dynamic_route', default_state={
            'safe': ['On'],
            'warning': ['Off'],
        }),
        TextDyField.data_source('Firewall Rules', 'data.firewall_data.total_number'),
        DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
    ],

    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='description', key='data.description'),
        SearchField.set(name='firewall', key='data.firewall_data.firewall'),
        SearchField.set(name='route', key='data.route_data.route'),
        SearchField.set(name='subnetwork', key='data.subnetwork_data.subnets'),
        SearchField.set(name='Creation Time', key='data.creation_timestamp', data_type='datetime'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_load_balancing}),
]
