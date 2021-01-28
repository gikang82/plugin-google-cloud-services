from spaceone.inventory.libs.manager import GoogleCloudManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.bigquery.data import *
from spaceone.inventory.model.bigquery.cloud_service import *
from spaceone.inventory.connector.big_query import BigQueryConnector
from spaceone.inventory.model.bigquery.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
from pprint import pprint
import time


class BigQueryManager(GoogleCloudManager):
    connector_name = 'BigQueryConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Big Query START **")
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

        collected_cloud_services = []
        secret_data = params['secret_data']
        project_id = secret_data['project_id']
        big_query_conn: BigQueryConnector = self.locator.get_connector(self.connector_name, **params)

        data_sets = big_query_conn.list_dataset()
        projects = big_query_conn.list_projects()
        jobs = big_query_conn.list_job()

        '''
        class BigQuery(Model):
        # id = StringType()
        # name = StringType()
        #project = StringType()
        #region = StringType()
        #dataset_reference = ModelType(DatasetReference, deserialize_from='datasetReference', serialize_when_none=False)
        #friendly_name = StringType(deserialize_from='friendlyName', serialize_when_none=False)
        
        #tables = ListType(ModelType(Table), default=[])
        #table_schemas = ListType(ModelType(TableSchemaRef), default=[])
        
        jobs = ListType(ModelType(Job), default=[])
        
        #projects = ListType(ModelType(Project), default=[])
        #access = ListType(ModelType(Access), default=[])
        #labels = ListType(ModelType(Labels), default=[])
        #self_link = StringType()
        #etags = StringType()
        #location = StringType()
        #visible_on_console = BooleanType()
        #default_partition_expiration_ms = DateTimeType(deserialize_from='defaultPartitionExpirationMs')
        #default_table_expiration_ms = DateTimeType(deserialize_from='defaultTableExpirationMs')
        #creation_time = DateTimeType(deserialize_from='creationTime')
        #last_modified_time = DateTimeType(deserialize_from='lastModifiedTime')
        '''

        for data_set in data_sets:
            data_refer = data_set.get('datasetReference', {})
            data_set_id = data_refer.get('datasetId')
            dataset_project_id = data_refer.get('projectId')

            bq_dataset = big_query_conn.get_dataset(data_set_id)
            bq_dt_tables = big_query_conn.list_tables(data_set_id)
            update_bq_dt_tables, table_schemas = self._get_table_list_with_schema(big_query_conn, bq_dt_tables)
            matched_projects = self._get_matching_project(dataset_project_id, projects)
            matched_jobs = self._get_matching_jobs(update_bq_dt_tables, jobs)

            creation_time = bq_dataset.get('creationTime')
            if creation_time:
                bq_dataset.update({'creationTime': datetime.fromtimestamp(int(creation_time) / 1000)})

            last_modified_time = bq_dataset.get('lastModifiedTime')
            if last_modified_time:
                bq_dataset.update({'lastModifiedTime': datetime.fromtimestamp(int(last_modified_time) / 1000)})

            region = self.get_region(bq_dataset.get('location', ''))

            exp_partition_ms = bq_dataset.get('defaultPartitionExpirationMs')
            exp_table_ms = bq_dataset.get('defaultTableExpirationMs')

            if exp_partition_ms:
                bq_dataset.update({'default_partition_expiration_ms_display': self.get_ms_display(exp_partition_ms)})

            if exp_table_ms:
                bq_dataset.update({'default_table_expiration_ms_display': self.get_ms_display(exp_table_ms)})

            labels = self.convert_labels_format(bq_dataset.get('labels', {}))
            bq_dataset.update({
                'name': data_set_id,
                'project': project_id,
                'tables': update_bq_dt_tables,
                'table_schemas': table_schemas,
                'region': region,
                'visible_on_console': self.get_visible_on_console(data_set_id),
                'jobs': matched_jobs,
                'matching_projects': matched_projects,
                'labels': labels
            })

            big_query_data = BigQueryWorkSpace(bq_dataset, strict=False)
            big_query_work_space_resource = SQLWorkSpaceResource({
                'tags': labels,
                'data': big_query_data,
                'region_code': region,
                'reference': ReferenceModel(big_query_data.reference())
            })

            self.set_region_code(region)
            collected_cloud_services.append(SQLWorkSpaceResponse({'resource': big_query_work_space_resource}))

        print(f'** Big Query Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services

    def get_region(self, location):
        matched_info = self.match_region_info(location)
        return matched_info.get('region_code') if matched_info else 'global'

    def get_ms_display(self, mills):
        display = ''
        _mills = int(mills) if isinstance(mills,str) else mills
        d, h, m, s = self.convertMillis(_mills)
        arr = [d, h, m, s]
        word_single = ['Day', 'Hour', 'Minute', 'Second']
        word_plural = ['Days', 'Hours', 'Minutes', 'Seconds']
        for idx, val in enumerate(arr):
            if val > 0:
                if int(val) == 1:
                    display = display + f'{int(val)} {word_single[idx]} '
                else:
                    display = display + f'{int(val)} {word_plural[idx]} '

        return display

    @staticmethod
    def _get_matching_project(project_id, projects):
        _projects = []
        for project in projects:
            if project_id == project.get('id'):
                _projects.append(ProjectModel(project, strict=False))
        return _projects

    @staticmethod
    def get_visible_on_console(dataset_id):
        return False if dataset_id.startswith('_') else True

    @staticmethod
    def _get_table_list_with_schema(big_conn: BigQueryConnector, bq_dt_tables):
        update_bq_dt_tables = []
        table_schemas = []

        for bq_dt_table in bq_dt_tables:
            table_ref = bq_dt_table.get('tableReference')
            table_single = big_conn.get_tables(table_ref.get('datasetId'), table_ref.get('tableId'))

            if table_single is not None:
                creationTime = table_single.get('creationTime')
                if creationTime:
                    table_single.update({'creationTime': datetime.fromtimestamp(int(creationTime) / 1000)})

                expirationTime = table_single.get('expirationTime')
                if expirationTime:
                    table_single.update({'expirationTime': datetime.fromtimestamp(int(expirationTime) / 1000)})

                lastModifiedTime = table_single.get('lastModifiedTime')
                if lastModifiedTime:
                    table_single.update({'lastModifiedTime': datetime.fromtimestamp(int(lastModifiedTime) / 1000)})

                fields = table_single.get('schema', {}).get('fields', [])
                table_single.update({'schema': fields})

                update_bq_dt_tables.append(table_single)

                for single_schema in fields:
                    single_schema.update({'table_id': table_ref.get('tableId')})
                    table_schemas.append(single_schema)

        return update_bq_dt_tables, table_schemas

    @staticmethod
    def _get_matching_jobs(tables, jobs):
        matched_jobs = []
        for table in tables:
            table_reference = table.get('tableReference', {})
            for job in jobs:
                stat = job.get('statistics', {})
                conf = job.get('configuration', {})
                refer_tables = stat.get('query', {}).get('referencedTables', [])
                if table_reference in refer_tables:

                    creationTime = datetime.fromtimestamp(int(stat.get('creationTime')) / 1000)
                    startTime = datetime.fromtimestamp(int(stat.get('startTime')) / 1000)
                    endTime = datetime.fromtimestamp(int(stat.get('endTime')) / 1000)

                    _query = conf.get('query', {})
                    query = _query.get('query', '')
                    query_display = f'{query[:200]} ...' if len(query) > 200 else query

                    _query.update({'query_display': query_display})
                    conf.update({'query': _query})
                    stat.update({
                        'creationTime': creationTime,
                        'startTime': startTime,
                        'endTime': endTime
                    })
                    job.update({'statistics': stat,
                                'configuration': conf
                                })
                    matched_jobs.append(Job(job, strict=False))

        return matched_jobs
