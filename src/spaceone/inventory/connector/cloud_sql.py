import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *


__all__ = ['CloudSQL']
_LOGGER = logging.getLogger(__name__)


class CloudSQL(GoogleCloudConnector):

    google_client_service = 'sqladmin'
    version = 'v1beta4'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_instances(self, **query):
        query = self.generate_query(**query)
        result = self.client.instances().list(**query).execute()
        return result.get('items', [])
