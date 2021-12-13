import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector

__all__ = ['InstanceTemplateConnector']
_LOGGER = logging.getLogger(__name__)


class InstanceTemplateConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_machine_types(self, **query):
        machine_type_list = []
        query.update({'project': self.project_id})
        request = self.client.machineTypes().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, machine_type in response['items'].items():
                if 'machineTypes' in machine_type:
                    machine_type_list.extend(machine_type.get('machineTypes'))
            request = self.client.machineTypes().aggregatedList_next(previous_request=request,
                                                                     previous_response=response)

        return machine_type_list


    def list_disks(self, **query):
        disk_list = []
        query.update({'project': self.project_id})
        request = self.client.instanceGroupManagers().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, _disk in response['items'].items():
                if 'disks' in _disk:
                    disk_list.extend(_disk.get('disks'))
            request = self.client.instanceGroupManagers().aggregatedList_next(previous_request=request,
                                                                              previous_response=response)

        return disk_list

    def list_instance_templates(self, **query):
        instance_template_list = []
        query.update({'project': self.project_id})
        request = self.client.instanceTemplates().list(**query)
        while request is not None:
            response = request.execute()
            for template in response.get('items', []):
                instance_template_list.append(template)
            request = self.client.instanceTemplates().list_next(previous_request=request,
                                                                previous_response=response)

        return instance_template_list

    def list_instance_group_managers(self, **query):
        instance_group_manager_list = []
        query.update({'project': self.project_id})
        request = self.client.instanceGroupManagers().aggregatedList(**query)
        while request is not None:
            response = request.execute()
            for key, _instance_group_manager_list in response['items'].items():
                if 'instanceGroupManagers' in _instance_group_manager_list:
                    instance_group_manager_list.extend(_instance_group_manager_list.get('instanceGroupManagers'))
            request = self.client.instanceGroupManagers().aggregatedList_next(previous_request=request,
                                                                              previous_response=response)

        return instance_group_manager_list