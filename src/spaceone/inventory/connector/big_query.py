import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.model.bigquery.data import *
from spaceone.inventory.error import *
from pprint import pprint

__all__ = ['BigQueryConnector']
_LOGGER = logging.getLogger(__name__)


class BigQueryConnector(GoogleCloudConnector):
    google_client_service = 'bigquery'
    version = 'v2'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_dataset(self, **query):
        dataset_list = []
        query.update({'projectId': self.project_id, 'all': True})
        request = self.client.datasets().list(**query)
        while request is not None:
            try:
                response = request.execute()
                for dataset in response.get('datasets', []):
                    dataset_list.append(dataset)
                request = self.client.datasets().list_next(previous_request=request, previous_response=response)

            except Exception as e:
                request = None
                print(f'Error occurred at BigQueryConnector: datasets().list(**query) : skipped \n {e}')

        return dataset_list

    def get_dataset(self, dataset_id, **query):
        query.update({'projectId': self.project_id,
                      'datasetId': dataset_id})
        response = {}

        try:
            response = self.client.datasets().get(**query).execute()
        except Exception as e:
            print(f'Error occurred at BigQueryConnector: datasets().get(**query) : skipped \n {e}')


        return response

    def list_job(self, **query):
        job_list = []
        query.update({'projectId': self.project_id,
                      'allUsers': True,
                      'projection': 'full'})
        request = self.client.jobs().list(**query)
        while request is not None:
            try:
                response = request.execute()
                for job in response.get('jobs', []):
                    job_list.append(job)
                request = self.client.jobs().list_next(previous_request=request, previous_response=response)
            except Exception as e:
                request = None
                print(f'Error occurred at jobs().list(**query) : skipped \n {e}')
        return job_list

    def list_projects(self, **query):
        project_list = []
        request = self.client.projects().list(**query)

        while request is not None:
            try:
                response = request.execute()
                for project in response.get('projects', []):
                    project_list.append(project)
                request = self.client.projects().list_next(previous_request=request, previous_response=response)
            except Exception as e:
                request = None
                print(f'Error occurred at BigQueryConnector: projects().list(**query) : skipped \n {e}')

        return project_list

    def list_tables(self, dataset_id, **query):
        table_list = []

        query.update({'projectId': self.project_id,
                      'datasetId': dataset_id})

        request = self.client.tables().list(**query)
        while request is not None:
            try:
                response = request.execute()
                for table in response.get('tables', []):
                    table_list.append(table)
                request = self.client.tables().list_next(previous_request=request, previous_response=response)
            except Exception as e:
                request = None
                print(f'Error occurred at BigQueryConnector: tables().list(**query) : skipped \n {e}')

        return table_list

    def get_tables(self, dataset_id, table_id, **query):
        query.update({'projectId': self.project_id,
                      'datasetId': dataset_id,
                      'tableId': table_id})
        response = {}
        try:
            response = self.client.tables().get(**query).execute()
        except Exception as e:
            print(e)

        return response