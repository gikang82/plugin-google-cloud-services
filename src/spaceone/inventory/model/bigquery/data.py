from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, UnionType, MultiType


class Labels(Model):
    key = StringType()
    value = StringType()


class View(Model):
    use_legacy_sql = BooleanType(deserialize_from='useLegacySql', serialize_when_none=False)


class Range(Model):
    start = StringType(serialize_when_none=False)
    end = StringType(serialize_when_none=False)
    interval = StringType(serialize_when_none=False)


class TimePartitioning(Model):
    type = StringType()
    expiration_ms = StringType(deserialize_from='expirationMs', serialize_when_none=False)
    field = StringType(serialize_when_none=False)
    require_partition_filter = StringType(deserialize_from='requirePartitionFilter', serialize_when_none=False)


class RangePartitioning(Model):
    field = StringType()
    range = ModelType(Range, serialize_when_none=False)


class TableReference(Model):
    project_id = StringType(deserialize_from='projectId', serialize_when_none=False)
    dataset_id = StringType(deserialize_from='datasetId', serialize_when_none=False)
    table_id = StringType(deserialize_from='tableId', serialize_when_none=False)

class Clustering(Model):
    fields = ListType(StringType(), serialize_when_none=False)


class HivePartitioningOptions(Model):
    mode = StringType()
    source_uri_prefix = StringType(deserialize_from='sourceUriPrefix', serialize_when_none=False)
    require_partition_filter = BooleanType(deserialize_from='requirePartitionFilter', serialize_when_none=False)
    fields = ListType(StringType(), serialize_when_none=False)


class TableSchemaRef(Model):
    table_id = StringType()
    name = StringType()
    type = StringType()
    mode = StringType()


class TableSchema(Model):
    name = StringType()
    type = StringType()
    mode = StringType()


class ProjectReference(Model):
    project_id = StringType()


class JobReference(Model):
    project_id = StringType(deserialize_from='projectId')
    job_id = StringType(deserialize_from='jobId')
    location = StringType(serialize_when_none=False)


class ErrorProto(Model):
    reason = StringType(serialize_when_none=False)
    location = StringType(serialize_when_none=False)
    debug_info = StringType(deserialize_from='debugInfo')
    message = StringType(serialize_when_none=False)


class ReservationUsage(Model):
    name = StringType(serialize_when_none=False)
    slot_ms = StringType(deserialize_from='slotMs', serialize_when_none=False)


class StatisticQuery(Model):
    total_partitions_processed = StringType(deserialize_from='totalPartitionsProcessed', serialize_when_none=False)
    total_bytes_processed = StringType(deserialize_from='totalBytesProcessed', serialize_when_none=False)
    total_bytes_processed_accuracy = StringType(deserialize_from='totalBytesProcessedAccuracy', serialize_when_none=False)
    total_bytes_billed = StringType(deserialize_from='totalBytesBilled', serialize_when_none=False)
    cache_hit = BooleanType(deserialize_from='cacheHit', serialize_when_none=False)
    statement_type = StringType(deserialize_from='statementType', serialize_when_none=False)



class JobStatistics(Model):
    query = ModelType(StatisticQuery)
    creation_time = DateTimeType(deserialize_from='creationTime', serialize_when_none=False)
    start_time = DateTimeType(deserialize_from='startTime', serialize_when_none=False)
    end_time = DateTimeType(deserialize_from='endTime', serialize_when_none=False)
    total_bytes_processed = StringType(deserialize_from='totalBytesProcessed', serialize_when_none=False)
    completion_ratio = FloatType(deserialize_from='completionRatio', serialize_when_none=False)
    quota_deferments = ListType(StringType(), deserialize_from='quotaDeferments', serialize_when_none=False)
    total_Slot_ms = StringType(deserialize_from='totalSlotMs', serialize_when_none=False)
    reservation_usages = ListType(ModelType(ReservationUsage), deserialize_from='ReservationUsage', serialize_when_none=False)
    reservation_id = StringType(deserialize_from='reservation_id', serialize_when_none=False)
    num_child_jobs = StringType(deserialize_from='numChildJobs', serialize_when_none=False)
    parent_job_id = StringType(deserialize_from='parentJobId', serialize_when_none=False)



class JobConfigurationQuery(Model):
    query = StringType(serialize_when_none=False)
    query_display = StringType(serialize_when_none=False)
    destinationTable = ModelType(TableReference, serialize_when_none=False, deserialize_from='destinationTable')
    priority = StringType(deserialize_from='preserveNulls', serialize_when_none=False)
    preserve_nulls = BooleanType(deserialize_from='preserveNulls', serialize_when_none=False)
    allow_large_results = BooleanType(deserialize_from='allowLargeResults', serialize_when_none=False)
    use_query_cache = BooleanType(deserialize_from='useQueryCache', serialize_when_none=False)
    flatten_results = BooleanType(deserialize_from='flattenResults', serialize_when_none=False)
    use_legacy_sql = BooleanType(deserialize_from='useLegacySql', serialize_when_none=False)
    parameter_mode = StringType(deserialize_from='parameterMode', serialize_when_none=False)
    maximum_billing_tier = IntType(deserialize_from='maximumBillingTier', serialize_when_none=False)
    maximum_bytes_billed = StringType(deserialize_from='maximumBytesBilled', serialize_when_none=False)
    create_disposition = StringType(deserialize_from='createDisposition', serialize_when_none=False)
    write_disposition = StringType(deserialize_from='writeDisposition', serialize_when_none=False)


class JobConfiguration(Model):
    job_type = StringType(deserialize_from='jobType', serialize_when_none=False)
    query = ModelType(JobConfigurationQuery, serialize_when_none=False)
    dry_run = BooleanType(deserialize_from='dryRun', serialize_when_none=False)
    job_timeout_ms = StringType(deserialize_from='jobTimeoutMs', serialize_when_none=False)
    labels = ListType(ModelType(Labels), default=[])


class JobStatus(Model):
    state = StringType(serialize_when_none=False)
    error_result = ModelType(ErrorProto, deserialize_from='errorResult', serialize_when_none=False)
    errors = ListType(ModelType(ErrorProto), serialize_when_none=False)


class Job(Model):
    id = StringType()
    kind = StringType()
    state = StringType()
    job_reference = ModelType(JobReference, deserialize_from='jobReference', serialize_when_none=False)
    error_result = ModelType(ErrorProto, deserialize_from='errorResult', serialize_when_none=False)
    statistics = ModelType(JobStatistics, serialize_when_none=False)
    configuration = ModelType(JobConfiguration, serialize_when_none=False)
    status = ModelType(JobStatus)
    user_email = StringType()

class Table(Model):
    id = StringType()
    kind = StringType()
    table_reference = ModelType(TableReference, deserialize_from='tableReference', serialize_when_none=False)
    friendly_name = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    range_partitioning = ModelType(RangePartitioning, deserialize_from='rangePartitioning', serialize_when_none=False)
    labels = ListType(ModelType(Labels), default=[])
    view = ModelType(View, serialize_when_none=False)
    num_rows = StringType(deserialize_from='numRows', serialize_when_none=False)
    schema = ListType(ModelType(TableSchema), default=[])
    creation_time = DateTimeType(deserialize_from='creationTime', serialize_when_none=False)
    expiration_time = DateTimeType(deserialize_from='expirationTime', serialize_when_none=False)
    last_modified_time = DateTimeType(deserialize_from='lastModifiedTime', serialize_when_none=False)


class DatasetReference(Model):
    dataset_id = StringType(deserialize_from='datasetId', serialize_when_none=False)
    project_id = StringType(deserialize_from='projectId', serialize_when_none=False)


class ProjectModel(Model):
    id = StringType()
    kind = StringType()
    numeric_id = StringType(deserialize_from='numericId')
    project_reference = ModelType(ProjectReference, deserialize_from='projectReference', serialize_when_none=False)
    friendly_name = StringType(deserialize_from='friendlyName', serialize_when_none=False)


class Access(Model):
    role = StringType(deserialize_from='role', serialize_when_none=False)
    special_group = StringType(deserialize_from='specialGroup', serialize_when_none=False)
    user_by_email = StringType(deserialize_from='userByEmail', serialize_when_none=False)


class BigQueryWorkSpace(Model):
    id = StringType()
    name = StringType()
    project = StringType()
    region = StringType()
    matching_projects = ListType(ModelType(ProjectModel), default=[])
    dataset_reference = ModelType(DatasetReference, deserialize_from='datasetReference', serialize_when_none=False)
    friendly_name = StringType(deserialize_from='friendlyName', serialize_when_none=False)
    tables = ListType(ModelType(Table), default=[])
    table_schemas = ListType(ModelType(TableSchemaRef), default=[])
    jobs = ListType(ModelType(Job), default=[])
    access = ListType(ModelType(Access), default=[])
    labels = ListType(ModelType(Labels), default=[])
    etags = StringType(serialize_when_none=False)
    location = StringType()
    visible_on_console = BooleanType()
    default_partition_expiration_ms_display = StringType(serialize_when_none=False)
    default_table_expiration_ms_display = StringType(serialize_when_none=False)
    default_table_expiration_ms = StringType(deserialize_from='defaultTableExpirationMs',serialize_when_none=False)
    default_partition_expiration_ms = StringType(deserialize_from='defaultPartitionExpirationMs', serialize_when_none=False)

    self_link = StringType(deserialize_from='selfLink')
    creation_time = DateTimeType(deserialize_from='creationTime')
    last_modified_time = DateTimeType(deserialize_from='lastModifiedTime')

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/bigquery?project={self.project}&p={self.dataset_reference.project_id}&page=dataset&d={self.dataset_reference.dataset_id}"
        }
