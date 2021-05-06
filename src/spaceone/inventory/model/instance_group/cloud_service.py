from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.instance_group.data import InstanceGroup
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, DateTimeDyField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, ListDynamicLayout, \
    TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
INSTANCE
'''
# TAB - Instance Group
instance_group_item = ItemDynamicLayout.set_fields('Instance Group', fields=[
    TextDyField.data_source('Resource ID', 'data.id'),
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('Type', 'data.instance_group_type',
                            default_outline_badge=['STATELESS', 'STATEFUL', 'UNMANAGED']),
    TextDyField.data_source('Project', 'data.project'),
    TextDyField.data_source('Region', 'data.display_location.region'),
    TextDyField.data_source('Zone', 'data.display_location.zone'),
    TextDyField.data_source('Network', 'data.network'),
    TextDyField.data_source('Subnet', 'data.subnetwork'),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Instance Counts', 'data.instance_counts'),
    TextDyField.data_source('Min Replicas', 'data.auto_scaler.autoscaling_policy.min_num_replicas'),
    TextDyField.data_source('Max Replicas', 'data.auto_scaler.autoscaling_policy.max_num_replicas'),
    TextDyField.data_source('Recommended Size', 'data.auto_scaler.recommended_size'),
    TextDyField.data_source('Self Link', 'data.self_link'),
    DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
])

instance_template_item = ItemDynamicLayout.set_fields('Instance Template', fields=[
    TextDyField.data_source('Resource ID', 'data.template.id'),
    TextDyField.data_source('Name', 'data.template.name'),
    TextDyField.data_source('Description', 'data.template.description'),
    TextDyField.data_source('Self Link', 'data.template.self_link'),
    DateTimeDyField.data_source('Creation Time', 'data.creation_timestamp'),
])

instance_group_layout = ListDynamicLayout.set_layouts('Instance Group',
                                                      layouts=[instance_group_item, instance_template_item])

autoscaler = ItemDynamicLayout.set_fields('Auto Scaler', fields=[
    TextDyField.data_source('Resource ID', 'data.auto_scaler.id'),
    TextDyField.data_source('Name', 'data.auto_scaler.name'),
    TextDyField.data_source('Description', 'data.auto_scaler.description'),
    EnumDyField.data_source('Status', 'data.auto_scaler.status', default_state={
        'safe': ['ACTIVE'],
        'warning': ['PENDING', 'DELETING'],
        'alert': ['ERROR']
    }),
    ListDyField.data_source('Status Detail Message', 'data.auto_scaler.status_details',
                            options={'sub_key': 'message'}),
    TextDyField.data_source('Self Link', 'data.auto_scaler.self_link'),
    DateTimeDyField.data_source('Creation Time', 'data.auto_scaler.creation_timestamp'),
])

autoscaling_policy = ItemDynamicLayout.set_fields('Auto Scaling Policy', fields=[
    EnumDyField.data_source('Mode', 'data.auto_scaler.autoscaling_policy.mode', default_badge={
        'indigo.500': ['ON'], 'coral.600': ['OFF']
    }),
    TextDyField.data_source('Minimum Replica Counts', 'data.auto_scaler.autoscaling_policy.min_num_replicas'),
    TextDyField.data_source('Maximum Replica Counts', 'data.auto_scaler.autoscaling_policy.max_num_replicas'),
    TextDyField.data_source('Cool Down Period (Seconds)', 'data.auto_scaler.autoscaling_policy.cool_down_period_sec'),
    TextDyField.data_source('CPU Utilization',
                            'data.auto_scaler.autoscaling_policy.cpu_utilization.utilization_target'),
    TextDyField.data_source('Load Balancing Utilization',
                            'data.auto_scaler.autoscaling_policy.loadbalancing_utilization.utilization_target'),
])

autoscaling_layout = ListDynamicLayout.set_layouts('Auto Scaler',
                                                   layouts=[autoscaler, autoscaling_policy])

autohealing_layout = TableDynamicLayout.set_fields('AutoHealing', root_path='data.instance_group_manager.auto_healing_policies', fields=[
    TextDyField.data_source('Health Check', 'health_check'),
    TextDyField.data_source('Initial Delay (Seconds)', 'initial_delay_sec'),
])

instance_layout = TableDynamicLayout.set_fields('Instance', root_path='data.instances', fields=[
    TextDyField.data_source('Name', 'name'),
    EnumDyField.data_source('Status', 'status', default_state={
        'safe': ['RUNNING'],
        'warning': ['STAGING', 'PROVISIONING', 'REPAIRING', 'STOPPING', 'SUSPENDING'],
        'disable': ['TERMINATED'],
        'alert': ['SUSPENDED']
    }),
    TextDyField.data_source('Self Link', 'instance'),
    ListDyField.data_source('Ports (Name)', 'name_ports',
                            default_badge={'type': 'outline', 'sub_key': 'name', 'delimiter': '<br>'}),
    ListDyField.data_source('Ports', 'name_ports',
                            default_badge={'type': 'outline', 'sub_key': 'port', 'delimiter': '<br>'}),
])


instance_group_meta = CloudServiceMeta.set_layouts([instance_group_layout, instance_layout,
                                                    autoscaling_layout, autohealing_layout])


class ComputeEngineResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeEngine')


class InstanceGroupResource(ComputeEngineResource):
    cloud_service_type = StringType(default='InstanceGroup')
    data = ModelType(InstanceGroup)
    _metadata = ModelType(CloudServiceMeta, default=instance_group_meta, serialized_name='metadata')


class InstanceGroupResponse(CloudServiceResponse):
    resource = PolyModelType(InstanceGroupResource)
