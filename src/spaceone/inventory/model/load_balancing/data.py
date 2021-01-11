from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType, DictType, UnionType, MultiType


class Labels(Model):
    key = StringType()
    value = StringType()


class TargetGRPCProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    self_link = StringType()
    self_link_with_id = StringType(deserialize_from='selfLinkWithId', serialize_when_none=False)
    url_map = StringType()
    region = StringType()
    validate_for_proxyless = BooleanType(deserialize_from='validateForProxyless', serialize_when_none=False)
    finger_print = StringType(deserialize_from='fingerprint', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetHttpProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    self_link = StringType()
    url_map = StringType()
    region = StringType()
    proxy_bind = BooleanType(deserialize_from='proxyBind', serialize_when_none=False)
    finger_print = StringType(deserialize_from='fingerprint', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetHttpsProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    self_link = StringType()
    ssl_certificates = ListType(StringType, default=[])
    quic_override = StringType(choices=['NONE', 'ENABLE', 'DISABLE'], serialize_when_none=False)
    url_map = StringType()
    region = StringType()
    authorization_policy = StringType(serialize_when_none=False)
    proxy_bind = BooleanType(deserialize_from='proxyBind', serialize_when_none=False)
    finger_print = StringType(deserialize_from='fingerprint', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetProxy(Model):
    name = StringType()
    type = StringType()
    description = StringType()
    grpc_proxy = ModelType(TargetGRPCProxy, serialize_when_none=False)
    http_proxy = ModelType(TargetHttpProxy, serialize_when_none=False)
    https_proxy = ModelType(TargetHttpsProxy, serialize_when_none=False)
    target_resource = StringType()
    in_used_by = StringType()



class ForwardingRule(Model):
    name = StringType()
    description = StringType()
    type = StringType(choices=['Global', 'Regional'])
    region = StringType()
    address = StringType()
    protocol = StringType()
    target = StringType(choices=['tcp', 'udp', 'http', 'https'])


class BackendService(Model):
    name = StringType()
    description = StringType()
    type = StringType()
    region = StringType()
    in_used_by = StringType()


class BackEndBucket(Model):
    name = StringType()
    description = StringType()
    bucket = StringType()
    in_used_by = StringType()


class Certificate(Model):
    name = StringType()
    description = StringType()
    domain = StringType()
    type = StringType()
    status = StringType()
    in_used_by = StringType()


class TargetPools(Model):
    name = StringType()
    region = StringType()
    number_of_instance = IntType(default=0)
    health_check = StringType()
    in_used_by = StringType()


class LoadBalancing(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    project = StringType()
    region = StringType()
    type = StringType(choices=('HTTP', 'TCP', 'UDP'))
    dns = StringType(default="")
    port = ListType(IntType())
    protocol = ListType(StringType())
    identifier = StringType(default='')
    scheme = StringType(choices=('EXTERNAL', 'INTERNAL'))
    network_tier = StringType(choices=('STANDARD', 'PREMIUM'))
    self_link = StringType(default="")
    forwarding_rules = ListType(ModelType(ForwardingRule), default=[])
    target_proxies = ListType(ModelType(TargetProxy), default=[])
    backend_services = ListType(ModelType(BackendService), default=[])
    backend_buckets = ListType(ModelType(BackEndBucket), default=[])

    # certificates = ListType(ModelType(TargetPools), default=[])

    target_pools = ListType(ModelType(TargetPools), default=[])
    labels = ListType(ModelType(Labels), default=[])
    tags = ListType(ModelType(Labels), default=[])
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')

    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/net-services/loadbalancing/details/{self.protocol}/{self.name}?project={self.project}"
        }