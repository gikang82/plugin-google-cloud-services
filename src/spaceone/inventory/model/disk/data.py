from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType


class Labels(Model):
    key = StringType()
    value = StringType()


class Disk(Model):
    project = StringType()
    id = StringType()
    name = StringType()
    zone = StringType()
    disk_type = StringType(choices=('local-ssd', 'pd-balanced', 'pd-ssd', 'pd-standard'), serialize_when_none=False)
    read_iops = FloatType(serialize_when_none=False)
    write_iops = FloatType(serialize_when_none=False)
    read_throughput = FloatType(serialize_when_none=False)
    write_throughput = FloatType(serialize_when_none=False)
    in_used_by = ListType(StringType(), default=[])
    source_image_display = StringType(serialize_when_none=False)
    source_image_id = StringType(deserialize_from='sourceImageId', serialize_when_none=False)
    source_image = StringType(deserialize_from='sourceImage', serialize_when_none=False)
    status = StringType(choices=('INVALID', 'CREATING', 'READY', 'DELETING', 'UPLOADING'))
    encryption = StringType(choices=('Google managed', 'Customer managed, Customer supplied'))
    size = FloatType()
    size_display = StringType()
    region = StringType()
    fingerprint = StringType(deserialize_from='labelFingerprint')
    snapshot_schedule = ListType(StringType(), default=[])
    self_link = StringType(deserialize_from='selfLink')
    labels = ListType(ModelType(Labels), default=[])
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')
    last_attach_timestamp = DateTimeType(deserialize_from='lastAttachTimestamp', serialize_when_none=False)
    last_detach_timestamp = DateTimeType(deserialize_from='lastDetachTimestamp', serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/compute/disksDetail/zones/{self.zone}/disks/{self.name}?project={self.project}"
        }
