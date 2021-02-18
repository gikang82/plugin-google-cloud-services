import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *

__all__ = ['StorageConnector']
_LOGGER = logging.getLogger(__name__)


class StorageConnector(GoogleCloudConnector):
    google_client_service = 'storage'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_buckets(self, **query):
        bucket_list = []
        query.update({'project': self.project_id, 'projection': 'full', 'alt': 'json'})
        request = self.client.buckets().list(**query)
        try:
            while request is not None:
                response = request.execute()
                for template in response.get('items', []):
                    bucket_list.append(template)
                request = self.client.buckets().list_next(previous_request=request, previous_response=response)
        except Exception as e:
            print(f'Error occurred at buckets().list(**query) : skipped \n {e}')
            pass

        return bucket_list

    def list_iam_policy(self, bucket_name, **query):
        query.update({"bucket": bucket_name})
        try:
            result = self.client.buckets().getIamPolicy(**query).execute()
        except Exception as e:
            # Not Authorized
            result = {'error_flag': 'na'}
            print(f'Error occurred at buckets().getIamPolicy(**query) : skipped \n {e}')

        return result

    def list_objects(self, bucket_name, **query):
        objects_list = []
        query.update({"bucket": bucket_name})
        request = self.client.objects().list(**query)
        try:
            while request is not None:
                response = request.execute()
                for template in response.get('items', []):
                    objects_list.append(template)
                request = self.client.objects().list_next(previous_request=request, previous_response=response)
        except Exception as e:
            print(f'Error occurred at objects().list(**query) : skipped \n : {e}')
            print(e)

        return objects_list
