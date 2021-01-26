from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.instance_group import InstanceGroupConnector
from spaceone.inventory.model.instance_group.data import *
from spaceone.inventory.model.instance_group.cloud_service import *
from spaceone.inventory.model.instance_group.cloud_service_type import CLOUD_SERVICE_TYPES
import time

class InstanceGroupManager(GoogleCloudManager):
    connector_name = 'InstanceGroupConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Instance Group START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        instance_group_conn: InstanceGroupConnector = self.locator.get_connector(self.connector_name, **params)

        # Get Instance Templates
        instance_templates = instance_group_conn.list_instance_templates()

        collected_cloud_services = []

        # Collect Zonal Instance Groups
        for zone in params.get('zones', []):
            if instance_groups := instance_group_conn.list_instance_groups(zone):
                # Get Instance Group Managers
                instance_group_managers = instance_group_conn.list_instance_group_managers(zone)

                # Get Auto Scalers
                autoscalers = instance_group_conn.list_autoscalers(zone)

                for instance_group in instance_groups:
                    instance_group.update({
                        'project': secret_data['project_id']
                    })

                    if match_instance_group_manager := \
                            self.match_instance_group_manager(instance_group_managers, instance_group['selfLink']):
                        # Managed
                        match_instance_group_manager.update({
                            'statefulPolicy': {
                                'preservedState': {'disks': self._get_stateful_policy(match_instance_group_manager)}}
                        })

                        instance_group.update({
                            'instance_group_type': self.get_instance_group_type(match_instance_group_manager),
                            'instance_group_manager': InstanceGroupManagers(match_instance_group_manager, strict=False)
                        })

                        if match_auto_scaler := self.match_auto_scaler(autoscalers, match_instance_group_manager):
                            instance_group.update({
                                'auto_scaler': AutoScaler(match_auto_scaler, strict=False),
                                'autoscaling_display':
                                    self._get_autoscaling_display(match_auto_scaler.get('autoscalingPolicy', {}))
                            })

                        match_instance_template = \
                            self.match_instance_template(instance_templates,
                                                         match_instance_group_manager['instanceTemplate'])

                        if match_instance_template:
                            instance_group.update({'template': InstanceTemplate(match_instance_template, strict=False)})

                    else:
                        # Unmanaged
                        instance_group.update({'instance_group_type': 'UNMANAGED'})

                    region = self.generate_region_from_zone_self_link(instance_group['zone'])

                    instances = instance_group_conn.list_instances(zone, instance_group['name'])
                    instance_group.update({
                        'instances': instances,
                        'instance_counts': len(instances)
                    })
                    # No labels
                    instance_group_data = InstanceGroup(instance_group, strict=False)
                    instance_group_resource = InstanceGroupResource({
                        'data': instance_group_data,
                        'region_code': region,
                        'reference': ReferenceModel(instance_group_data.reference())
                    })

                    self.set_region_code(region)
                    collected_cloud_services.append(InstanceGroupResponse({'resource': instance_group_resource}))

        # Collect Regional Instance Groups
        for region in params.get('regions', []):
            if instance_groups := instance_group_conn.list_region_instance_groups(region):
                # Get Instance Group Managers
                instance_group_managers = instance_group_conn.list_region_instance_group_managers(region)

                # Get Auto Scalers
                autoscalers = instance_group_conn.list_region_autoscalers(region)

                for instance_group in instance_groups:
                    instance_group.update({
                        'project': secret_data['project_id']
                    })

                    if match_instance_group_manager := \
                            self.match_instance_group_manager(instance_group_managers, instance_group['selfLink']):
                        # Managed
                        match_instance_group_manager.update({
                            'statefulPolicy': {
                                'preservedState': {'disks': self._get_stateful_policy(match_instance_group_manager)}}
                        })

                        instance_group.update({
                            'instance_group_type': self.get_instance_group_type(match_instance_group_manager),
                            'instance_group_manager': InstanceGroupManagers(match_instance_group_manager, strict=False)
                        })

                        if match_auto_scaler := self.match_auto_scaler(autoscalers, match_instance_group_manager):
                            instance_group.update({
                                'auto_scaler': AutoScaler(match_auto_scaler, strict=False),
                                'autoscaling_display':
                                    self._get_autoscaling_display(match_auto_scaler.get('autoscalingPolicy', {}))
                            })

                        match_instance_template = \
                            self.match_instance_template(instance_templates,
                                                         match_instance_group_manager['instanceTemplate'])

                        if match_instance_template:
                            instance_group.update({'template': InstanceTemplate(match_instance_template, strict=False)})

                    else:
                        # Unmanaged
                        instance_group.update({'instance_group_type': 'UNMANAGED'})

                    instances = instance_group_conn.list_region_instances(region, instance_group['name'])
                    instance_group.update({
                        'instances': instances,
                        'instance_counts': len(instances)
                    })

                    instance_group_data = InstanceGroup(instance_group, strict=False)
                    instance_group_resource = InstanceGroupResource({
                        'data': instance_group_data,
                        'region_code': region,
                        'reference': ReferenceModel(instance_group_data.reference())
                    })

                    self.set_region_code(region)
                    collected_cloud_services.append(InstanceGroupResponse({'resource': instance_group_resource}))

        print(f'** Instance Group Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services

    @staticmethod
    def match_instance_template(instance_templates, instance_template_self_link):
        for instance_template in instance_templates:
            if instance_template['selfLink'] == instance_template_self_link:
                return instance_template

        return None

    @staticmethod
    def match_instance_group_manager(instance_group_managers, instance_group_name):
        for instance_group_manager in instance_group_managers:
            if instance_group_manager['instanceGroup'] == instance_group_name:
                return instance_group_manager

        return None

    @staticmethod
    def match_auto_scaler(auto_scalers, instance_group_manager):
        match_auto_scaler_name = instance_group_manager.get('status', {}).get('autoscaler')

        if match_auto_scaler_name:
            for auto_scaler in auto_scalers:
                if match_auto_scaler_name == auto_scaler['selfLink']:
                    return auto_scaler

        return None

    @staticmethod
    def _get_stateful_policy(match_instance_group_manager):
        disks_vos = []
        stateful_policy = match_instance_group_manager.get('statefulPolicy')
        if stateful_policy:
            preserved_state = stateful_policy.get('preservedState')
            if preserved_state:
                for key, val in preserved_state.get('disks', {}).items():
                    disks_vos.append({'key': key, 'value': val})

        return disks_vos

    @staticmethod
    def get_instance_group_type(instance_group_manager):
        if instance_group_manager.get('status', {}).get('stateful', {}).get('hasStatefulConfig'):
            return 'STATEFUL'
        else:
            return 'STATELESS'

    def _get_autoscaling_display(self, autoscaling_policy):
        display_string = f'{autoscaling_policy.get("mode")}: Target '

        policy_display_list = []

        if 'cpuUtilization' in autoscaling_policy:
            policy_display_list.append(f'CPU utilization {(autoscaling_policy.get("cpuUtilization", {}).get("utilizationTarget")) * 100}%')

        if 'loadBalancingUtilization' in autoscaling_policy:
            policy_display_list.append(f'LB capacity fraction {(autoscaling_policy.get("loadBalancingUtilization", {}).get("utilizationTarget")) * 100}%')

        for custom_metric in autoscaling_policy.get('customMetricUtilizations', []):
            policy_display_list.append(
                f'{self._get_custom_metric_target_name(custom_metric.get("metric", ""))} {custom_metric.get("utilizationTarget", "")}{self._get_custom_metric_target_type(custom_metric.get("utilizationTargetType"))}')

        if policy_display_list:
            policy_join_str = ', '.join(policy_display_list)
            return f'{display_string}{policy_join_str}'
        else:
            return ''

    @staticmethod
    def _get_custom_metric_target_name(util_target):
        try:
            target_name = util_target.split('/')[-1]
            return target_name
        except Exception as e:
            return ''

    @staticmethod
    def _get_custom_metric_target_type(util_target_type):
        if util_target_type == 'GAUGE':
            return ''
        elif util_target_type == 'DELTA_PER_SECOND':
            return '/s'
        elif util_target_type == 'DELTA_PER_MINUTE':
            return '/m'
        else:
            return ''
