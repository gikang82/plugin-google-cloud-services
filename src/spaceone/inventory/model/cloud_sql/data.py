from schematics import Model
from schematics.types import ModelType, ListType, StringType, BooleanType, IntType, DateTimeType


class ServerCACert(Model):
    kind = StringType()
    cert_serial_number = StringType(deserialize_from="certSerialNumber")
    cert = StringType()
    common_name = StringType(deserialize_from="commonName")
    sha1_fingerprint = StringType(deserialize_from="sha1Fingerprint")
    instance = StringType()
    create_time = DateTimeType(deserialize_from="createTime")
    expiration_time = DateTimeType(deserialize_from="expirationTime")


class BackupRetentionSettings(Model):
    retention_unit = StringType(deserialize_from="retentionUnit")
    retained_backups = IntType(deserialize_from="retainedBackups")


class BackupConfiguration(Model):
    start_time = StringType()
    kind = StringType()
    location = StringType()
    backup_retention_settings = ModelType(BackupRetentionSettings, deserialize_from="backupRetentionSettings")
    enabled = BooleanType()
    transaction_log_retention_days = IntType(deserialize_from="transactionLogRetentionDays")


class MaintenanceWindow(Model):
    kind = StringType()
    hour = IntType()
    day = IntType()


class IPConfiguration(Model):
    authorized_networks = ListType(StringType, deserialize_from="authorizedNetworks")
    ipv4_enabled = BooleanType()


class LocationPreference(Model):
    zone = StringType()
    kind = StringType()


class InstanceSetting(Model):
    authorize_gae_applications = ListType(StringType, deserialize_from="authorizedGaeApplications")
    tier = StringType()
    kind = StringType()
    availability_type = StringType(deserialize_from="availabilityType")
    pricing_plan = StringType(deserialize_from="pricingPlan")
    replication_type = StringType(deserialize_from="replicationType")
    activation_policy = StringType(deserialize_from="activationPolicy")
    ip_configuration = ModelType(IPConfiguration, deserialize_from="ipConfiguration")
    location_preference = ModelType(LocationPreference, deserialize_from="locationPreference")
    data_disk_type = StringType(deserialize_from="dataDiskType")
    maintenance_window = ModelType(MaintenanceWindow, deserialize_from="maintenanceWindow")
    backup_configuration = ModelType(BackupConfiguration, deserialize_from="backupConfiguration")
    collation = StringType()
    settings_version = StringType(deserialize_from="settingsVersion")
    storage_auto_resize_limit = StringType(deserialize_from="storageAutoResizeLimit")
    storage_auto_resize = BooleanType(deserialize_from="storageAutoResize")
    data_disk_size_gb = StringType(deserialize_from="dataDiskSizeGb")


class IPAddress(Model):
    type = StringType(deserialize_from="type")
    ip_address = StringType(deserialize_from="ipAddress")


class Instance(Model):
    name = StringType()
    kind = StringType()
    state = StringType(choices=('SQL_INSTANCE_STATE_UNSPECIFIED', 'RUNNABLE', 'SUSPENDED', 'PENDING_DELETE',
                                'PENDING_CREATE', 'MAINTENANCE', 'FAILED'))
    region = StringType()
    gce_zone = StringType(deserialize_from="gceZone")
    database_version = StringType(deserialize_from="databaseVersion")
    settings = ModelType(InstanceSetting)
    etag = StringType()
    ip_addresses = ListType(ModelType(IPAddress), deserialize_from="ipAddresses")
    server_ca_cert = ModelType(ServerCACert, deserialize_from="serverCaCert")
    instance_type = StringType(deserialize_from="instanceType")
    project = StringType()
    service_account_email_address = StringType(deserialize_from="serviceAccountEmailAddress")
    backend_type = StringType(deserialize_from="backendType")
    self_link = StringType(deserialize_from="selfLink")
    connection_name = StringType(deserialize_from="connectionName")

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/sql/instances/{self.name}/overview?authuser=1&project={self.project}"
        }
