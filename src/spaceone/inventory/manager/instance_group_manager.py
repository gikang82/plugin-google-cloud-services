from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.instance_group import InstanceGroupConnector
from spaceone.inventory.model.instance_group.data import *
from spaceone.inventory.model.instance_group.cloud_service import *
from spaceone.inventory.model.instance_group.cloud_service_type import CLOUD_SERVICE_TYPES


class InstanceGroupManager(GoogleCloudManager):
    connector_name = 'InstanceGroupConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
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

        for zone in params.get('zones', []):
            print(f"====== ZONE: {zone} ======")

            # Get Instance Groups
            instance_groups = instance_group_conn.list_instance_groups(zone)

            if instance_groups:
                # Get Instance Group Managers
                instance_group_managers = instance_group_conn.list_instance_group_managers(zone)

                # Get Auto Scalers
                autoscalers = instance_group_conn.list_autoscalers(zone)

            for instance_group in instance_groups:
                instance_group.update({
                    'region': self.generate_region_from_zone(zone),
                    'project': secret_data['project_id']
                })

                instance_group_self_link = instance_group['selfLink']

                match_instance_group_manager = self.match_instance_group_manager(instance_group_managers,
                                                                                 instance_group_self_link)

                if match_instance_group_manager:
                    instance_group.update({
                        'instance_group_manager': InstanceGroupManagers(match_instance_group_manager, strict=False)
                    })

                    match_auto_scaler = self.match_auto_scaler(autoscalers, match_instance_group_manager)
                    if match_auto_scaler:
                        instance_group.update({'auto_scaler': AutoScaler(match_auto_scaler, strict=False)})

                    instances = instance_group_conn.list_instances(zone, match_instance_group_manager['name'])
                    instance_group.update({
                        'instances': instances,
                        'instance_counts': len(instances)
                    })

                    match_instance_template = \
                        self.match_instance_template(instance_templates,
                                                     match_instance_group_manager['instanceTemplate'])
                    if match_instance_template:
                        instance_group.update({'template': InstanceTemplate(match_instance_template, strict=False)})

                instance_group_data = InstanceGroup(instance_group, strict=False)
                instance_group_resource = InstanceGroupResource({
                    'data': instance_group_data,
                    'region_code': instance_group['region'],
                    'reference': ReferenceModel(instance_group_data.reference())
                })

                self.set_region_code(instance_group['region'])
                yield InstanceGroupResponse({'resource': instance_group_resource})

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
                if match_auto_scaler_name == auto_scaler['name']:
                    return auto_scaler

        return None


