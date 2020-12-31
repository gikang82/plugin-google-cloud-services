import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *
from pprint import pprint

__all__ = ['StorageConnector']
_LOGGER = logging.getLogger(__name__)


class StorageConnector(GoogleCloudConnector):
    google_client_service = 'storage'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_buckets(self, **query):
        query.update({
            'project': self.project_id,
            'projection': 'full',
            'alt': 'json'
        })
        result = {}
        try:
            result = self.client.buckets().list(**query).execute()
        except Exception as e:
            print(e)
            pass
        return result.get('items', [])

    def list_iam_policy(self, bucket_name, **query):
        query.update({"bucket": bucket_name})
        result = {}
        try:
            result = self.client.buckets().getIamPolicy(**query).execute()
        except Exception as e:
            print(e)
            # Not Authorized
            result = {'error_flag': 'na'}
        return result

    def list_objects(self, bucket_name, **query):
        query.update({"bucket": bucket_name})
        result = {}
        try:
            result = self.client.objects().list(**query).execute()
        except Exception as e:
            print(e)
        return result.get('items', [])
