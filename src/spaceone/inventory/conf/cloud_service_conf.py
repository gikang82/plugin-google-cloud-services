MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
FILTER_FORMAT = []
CLOUD_SERVICE_GROUP_MAP = {
    'SQLWorkspace': 'BigQueryManager',
    'CloudSQL': 'CloudSQLManager',
    'Disk': 'DiskManager',
    'ExternalIPAddress': 'ExternalIPAddressManager',
    'Firewall': 'FirewallManager',
    'InstanceGroup': 'InstanceGroupManager',
    'InstanceTemplate': 'InstanceTemplateManager',
    'LoadBalancing': 'LoadBalancingManager',
    'MachineImage': 'MachineImageManager',
    'Route': 'RouteManager',
    'Snapshot': 'SnapshotManager',
    'Bucket': 'StorageManager',
    'VPCNetwork': 'VPCNetworkManager'
}

