from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, FloatType


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
    self_link = StringType(deserialize_from='selfLink', serialize_when_none=False)
    load_balancing_scheme = StringType(choices=['EXTERNAL','INTERNAL','INTERNAL_MANAGED','INTERNAL_SELF_MANAGED'], serialize_when_none=False)
    subnetwork = StringType()
    network = StringType()
    back_service = StringType()
    service_label = StringType()
    service_name = StringType()
    network_tier = StringType(choices=('Premium', 'Standard'))
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp', serialize_when_none=False)


class LogConfig(Model):
    enable = BooleanType(serialize_when_none=False)
    sample_rate = IntType(deserialize_from='sampleRate', serialize_when_none=False)


class BackendServiceBackend(Model):
    description = StringType()
    group = StringType()
    balancing_mode = StringType(deserialize_from='balancingMode', choices=['RATE', 'UTILIZATION', 'CONNECTION'])
    max_utilization = FloatType(deserialize_from='maxUtilization', serialize_when_none=False)
    max_rate = IntType(deserialize_from='maxRate', serialize_when_none=False)
    max_rate_per_instance = FloatType(deserialize_from='maxRatePerInstance', serialize_when_none=False)
    max_rate_per_endpoint = FloatType(deserialize_from='maxRatePerEndpoint', serialize_when_none=False)
    max_connections = IntType(deserialize_from='maxConnections', serialize_when_none=False)
    max_connections_per_instance = IntType(deserialize_from='maxConnectionsPerInstance', serialize_when_none=False)
    max_connections_per_endpoint = IntType(deserialize_from='maxConnectionsPerEndpoint', serialize_when_none=False)
    capacity_scaler = FloatType(deserialize_from='capacityScaler', serialize_when_none=False)
    failover = BooleanType

class FailOverPolicy(Model):
    disable_connection_drain_on_failover = BooleanType(deserialize_from='disableConnectionDrainOnFailover', serialize_when_none=False)
    drop_traffic_if_unhealthy = BooleanType(deserialize_from='dropTrafficIfUnhealthy', serialize_when_none=False)
    failover_ratio = FloatType(deserialize_from='failoverRatio', serialize_when_none=False)

class ConnectionDraining(Model):
    draining_timeout_sec = IntType(deserialize_from='drainingTimeoutSec', serialize_when_none=False)

class BackendService(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    region = StringType()
    backends = ListType(ModelType(BackendServiceBackend), default=[], serialize_when_none=False)
    health_checks = ListType(StringType(), default=[], deserialize_from='healthChecks', serialize_when_none=False)
    timeout_sec = IntType(deserialize_from='timeoutSec', serialize_when_none=False)
    port = IntType(serialize_when_none=False)
    protocol = StringType(choices=['HTTP', 'HTTPS', 'HTTP2', 'TCP', 'SSL', 'UDP' 'GRPC'])
    fingerprint = StringType()
    port_name = StringType(deserialize_from='portName', serialize_when_none=False)
    enable_cdn = BooleanType(deserialize_from='enableCDN', serialize_when_none=False)
    sessionAffinity = StringType(deserialize_from='sessionAffinity',
                                 choices=['NONE', 'CLIENT_IP', 'CLIENT_IP_PROTO','CLIENT_IP_PORT_PROTO',
                                          'INTERNAL_MANAGED', 'INTERNAL_SELF_MANAGED', 'GENERATED_COOKIE',
                                          'HEADER_FIELD', 'HTTP_COOKIE'],
                                 serialize_when_none=False)
    affinity_cookie_ttl_sec = IntType(deserialize_from='affinityCookieTtlSec', serialize_when_none=False)
    failover_policy = ModelType(FailOverPolicy, serialize_when_none=False)
    load_balancing_scheme = StringType(deserialize_from='loadBalancingScheme',
                                 choices=['EXTERNAL','INTERNAL','INTERNAL_MANAGED','INTERNAL_SELF_MANAGED'],
                                 serialize_when_none=False)
    log_config = ModelType(LogConfig, serialize_when_none=False)
    connection_draining = ModelType(ConnectionDraining, serialize_when_none=False)
    self_link = StringType(deserialize_from='selfLink')
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')

class CDNPolicy(Model):
    signed_url_key_names = ListType(StringType(), default=[],
                                       deserialize_from='signedUrlKeyNames',
                                       serialize_when_none=False)
    signed_url_cache_max_age_sec = StringType(deserialize_from='signedUrlCacheMaxAgeSec')

    bucket_name = StringType(deserialize_from='bucketName')
    bucket_name = StringType(deserialize_from='bucketName')


class BackEndBucket(Model):
    id = StringType()
    name = StringType()
    bucket_name = StringType(deserialize_from='bucketName')
    description = StringType()
    self_link = StringType(deserialize_from='selfLink')
    cdn_policy = ModelType(CDNPolicy, serialize_when_none=False)
    enable_cdn = BooleanType(deserialize_from='enableCDN', serialize_when_none=False)
    custom_response_headers = ListType(StringType(), default=[],
                                       deserialize_from='customResponseHeaders',
                                       serialize_when_none=False)
    creation_timestamp = DateTimeType(deserialize_from='creationTimestamp')

class Certificate(Model):
    name = StringType()
    description = StringType()
    domain = StringType()
    type = StringType()
    status = StringType()
    in_used_by = StringType()


class TargetPools(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    region = StringType(serialize_when_none=False)
    healthChecks = ListType(StringType(), deserialize_from='healthChecks', default=[])
    instances = ListType(StringType(), default=[])
    session_affinity = StringType(deserialize_from='sessionAffinity',serialize_when_none=False)
    failover_ratio = FloatType(deserialize_from='failoverRatio',serialize_when_none=False)
    backup_pool = StringType(deserialize_from='backupPool',serialize_when_none=False)
    self_link = StringType(deserialize_from='selfLink')
    kind = StringType(serialize_when_none=False)


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
    session_affinity = StringType(serialize_when_none=False)
    connection_draining_timeout = StringType(serialize_when_none=False)
    logging = StringType(serialize_when_none=False)
    region = StringType(serialize_when_none=False)
    endpoint_protocol = StringType(serialize_when_none=False)
    name_port = StringType(serialize_when_none=False)
    time_out = StringType(serialize_when_none=False)
    cloud_cdn = StringType(serialize_when_none=False)
    traffic_policy = StringType(serialize_when_none=False)
    Health_check = ListType(StringType(), default=[])


class Frontend(Model):
    name = StringType()
    ip_port = StringType()
    protocols = StringType(choices=('HTTP', 'TCP', 'UDP', 'HTTPS'))
    certificate = StringType()
    network_tier = StringType(choices=('Premium', 'Standard'))


class HostAndPathRule(Model):
    host = StringType()
    path = StringType()
    back_end = StringType()


class LoadBalancing(Model):
    id = StringType()
    name = StringType()
    description = StringType()
    project = StringType()
    region = StringType()
    lb_type = StringType()
    #type = StringType(choices=('HTTP', 'TCP', 'UDP', 'HTTP(S)'))
    protocols = ListType(StringType(), default=[])
    source_link = StringType(deserialize_from='identifier', serialize_when_none=False)
    self_link = StringType(default="")
    host_and_paths = ListType(ModelType(HostAndPathRule), serialize_when_none=False)
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