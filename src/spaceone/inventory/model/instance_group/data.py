from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType


class InstanceTemplate(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')


class NamePort(Model):
    name = StringType()
    port = IntType()


class Instance(Model):
    instance = StringType()
    status = StringType(choices=('PROVISIONING', 'STAGING', 'RUNNING', 'STOPPING', 'SUSPENDING',
                                 'SUSPENDED', 'REPAIRING', 'TERMINATED'))
    name_ports = ListType(ModelType(NamePort), deserialize_from='namePorts')


class InstanceGroup(Model):
    id = StringType()
    kind = StringType()
    name = StringType()
    description = StringType()
    network = StringType()
    fingerprint = StringType()
    zone = StringType()
    self_link = StringType()
    size = IntType()
    region = StringType()
    subnetwork = StringType()
    project = StringType()
    instance_counts = IntType()
    template = ModelType(InstanceTemplate)
    instances = ListType(ModelType())
    name_ports = ListType(ModelType(NamePort), deserialize_from='namePorts')
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/compute/instanceGroups/details/{self.zone}/{self.name}?authuser=1&project={self.project}"
        }


class InstanceGroupManager(Model):
    id = StringType()
    name = StringType()
    instance_template = ModelType(InstanceTemplate)
    instance_group = ModelType(InstanceGroup)


