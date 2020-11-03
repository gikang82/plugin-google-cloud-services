import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *

__all__ = ['MachineImageConnector']
_LOGGER = logging.getLogger(__name__)


class MachineImageConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'beta'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_machine_images(self, **query):
        query = self.generate_query(**query)
        result = self.client.machineImages().list(**query).execute()
        return result.get('items', [])

    def list_machine_types(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.machineTypes().list(**query).execute()
        return result.get('items', [])

    def list_disks(self, zone, **query):
        query.update({'zone': zone})
        query = self.generate_query(**query)
        result = self.client.disks().list(**query).execute()
        return result.get('items', [])

    def list_public_images(self, **query) -> dict:
        public_images = {}
        public_image_list = [
            {'key': 'centos', 'value': 'centos-cloud'},
            {'key': 'coreos', 'value': 'coreos-cloud'},
            {'key': 'debian', 'value': 'debian-cloud'},
            {'key': 'google', 'value': 'google-containers'},
            {'key': 'opensuse', 'value': 'opensuse-cloud'},
            {'key': 'rhel', 'value': 'rhel-cloud'},
            {'key': 'suse', 'value': 'suse-cloud'},
            {'key': 'ubuntu', 'value': 'ubuntu-os-cloud'},
            {'key': 'windows', 'value': 'windows-cloud'}
        ]
        query = self.generate_query(**query)

        for public_image in public_image_list:

            query.update({'project': public_image.get('value'), 'orderBy': 'creationTimestamp desc'})
            response = self.client.images().list(**query).execute()
            image = response.get('items', [])
            public_images[public_image.get('key')] = image

        return public_images