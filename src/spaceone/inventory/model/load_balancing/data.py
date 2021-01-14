from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType


class Labels(Model):
    key = StringType()
    value = StringType()


class TargetTCPProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType(default='')
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    region = StringType(default='global')
    service = StringType()
    proxy_header = StringType(choices=['NONE', 'PROXY_V1'], deserialize_from='proxyHeader', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)
    kind = StringType()


class TargetSSLProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType(default='')
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    region = StringType(default='global')
    service = StringType()
    ssl_certificates = StringType(deserialize_from='sslCertificates', serialize_when_none=False)
    proxy_header = StringType(choices=['NONE', 'PROXY_V1'], deserialize_from='proxyHeader', serialize_when_none=False)
    ssl_policy = StringType(deserialize_from='sslPolicy', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)
    kind = StringType()


class TargetGRPCProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType(default='')
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    kind = StringType()
    region = StringType(default='global')
    self_link_with_id = StringType(deserialize_from='selfLinkWithId', serialize_when_none=False)
    url_map = StringType(deserialize_from='urlMap', serialize_when_none=False)
    validate_for_proxyless = BooleanType(deserialize_from='validateForProxyless', serialize_when_none=False)
    finger_print = StringType(deserialize_from='fingerprint', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetHttpProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType(default='')
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    url_map = StringType(deserialize_from='urlMap', serialize_when_none=False)
    region = StringType(default='global')
    kind = StringType()
    proxy_bind = BooleanType(deserialize_from='proxyBind', serialize_when_none=False)
    finger_print = StringType(deserialize_from='fingerprint', serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetHttpsProxy(Model):
    id = StringType()
    name = StringType()
    description = StringType(default='')
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    url_map = StringType(deserialize_from='urlMap', serialize_when_none=False)
    ssl_certificates = ListType(StringType, default=[], deserialize_from='sslCertificates', serialize_when_none=False)
    quic_override = StringType(deserialize_from='quicOverride', choices=['NONE', 'ENABLE', 'DISABLE'], serialize_when_none=False)
    ssl_policy = StringType(deserialize_from='sslPolicy', serialize_when_none=False)
    region = StringType(default='global')
    proxy_bind = BooleanType(deserialize_from='proxyBind', serialize_when_none=False)
    http_filters = ListType(StringType, default=[], serialize_when_none=False)
    server_tls_policy = StringType(deserialize_from='serverTlsPolicy', serialize_when_none=False)
    authentication = StringType(serialize_when_none=False)
    authorization_policy = StringType(deserialize_from='authorizationPolicy', serialize_when_none=False)
    authorization = StringType(serialize_when_none=False)
    kind = StringType()
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class TargetProxyDisplay(Model):
    name = StringType()
    description = StringType()
    type = StringType()
    target_resource = StringType()
    in_used_by_display = ListType(StringType(), default=[])


class InUsedBy(Model):
    id = StringType()
    name = StringType()
    self_link = StringType()


class TargetProxy(Model):
    name = StringType()
    type = StringType()
    description = StringType()
    grpc_proxy = ModelType(TargetGRPCProxy, serialize_when_none=False)
    http_proxy = ModelType(TargetHttpProxy, serialize_when_none=False)
    https_proxy = ModelType(TargetHttpsProxy, serialize_when_none=False)
    tcp_proxy = ModelType(TargetTCPProxy, serialize_when_none=False)
    ssl_proxy = ModelType(TargetSSLProxy, serialize_when_none=False)
    target_resource = ModelType(InUsedBy, default={})
    target_proxy_display = ModelType(TargetProxyDisplay, serialize_when_none=False)
    in_used_by = ListType(ModelType(InUsedBy), default=[])


class ForwardingRule(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    ip_address = StringType(deserialize_from='IPAddress', serialize_when_none=False)
    ip_protocol = StringType(deserialize_from='IPProtocol', serialize_when_none=False)
    port_range = StringType(deserialize_from='portRange', serialize_when_none=False)
    ports = ListType(StringType(), default=[])
    region = StringType(default='global')
    ip_version = StringType(deserialize_from='ipVersion', serialize_when_none=False)
    fingerprint = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    target = StringType(serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


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


class HealthCheck(Model):
    protocol = StringType()
    port = StringType()
    proxy_protocol = StringType()
    Logs = StringType()
    interval = IntType()
    timeout = IntType()
    healthy_threshold = StringType()
    unhealthy_threshold = StringType()


class Backend(Model):
    name = StringType()
    type = StringType()
    scope = IntType(default=0)
    protocol = StringType()
    logging = StringType(choices=['On', 'Off'])
    sample_rate = IntType(default=0)
    health_check = ModelType(HealthCheck)


class Frontend(Model):
    name = StringType()
    scope = StringType(choices=('Regional', 'Global'))
    address = StringType()
    protocols = StringType(choices=('HTTP', 'TCP', 'UDP', 'HTTPS'))
    network_tier = StringType(choices=('Premium', 'Standard'))


class LoadBalancing(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    project = StringType()
    region = StringType()
    type = StringType(choices=('HTTP', 'TCP', 'UDP', 'HTTP(S)'))
    protocols = ListType(StringType(), default=[])
    source_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    self_link = StringType(default="")
    backends = ListType(ModelType(Backend), default=[])
    frontends = ListType(ModelType(Frontend), default=[])
    forwarding_rules = ListType(ModelType(ForwardingRule), default=[])
    target_proxies = ListType(ModelType(TargetProxy), default=[])
    backend_services = ListType(ModelType(BackendService), default=[])
    backend_buckets = ListType(ModelType(BackEndBucket), default=[])
    #certificates = ListType(ModelType(TargetPools), default=[])
    target_pools = ListType(ModelType(TargetPools), default=[])
    labels = ListType(ModelType(Labels), default=[])
    tags = ListType(ModelType(Labels), default=[])
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')
    def reference(self):
        return {
            "resource_id": self.self_link,
            "external_link": f"https://console.cloud.google.com/net-services/loadbalancing/details/{self.protocol}/{self.name}?project={self.project}"
        }