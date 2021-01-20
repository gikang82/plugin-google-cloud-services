# plugin-google-cloud-services

![Google Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Google_Cloud.svg)
**Plugin to collect Google Cloud Services**

[plugin-google-cloud-services](https://github.com/spaceone-dev/plugin-google-cloud-services) is a convenient tool to 
get cloud service data from Google Cloud platform.

Find it also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/google-cloud-servi)

> Latest stable version : 1.1.2

Please contact us if you need any further information. 
<support@spaceone.dev>

---

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data 
Please, set authentication privilege for followings:
 
#### Compute Engine

- Compute VM(Instance)
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.zones.list
        - compute.regions.list
        - compute.instances.list
        - compute.machineTypes.list
        - compute.urlMaps.list
        - compute.backendServices.list
        - compute.disks.list
        - compute.diskTypes.list
        - compute.autoscalers.list
        - compute.images.list
        - compute.subnetworks.list
        - compute.regionUrlMaps.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list
    
- Instance Template
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.zones.list
        - compute.regions.list
        - compute.instances.list
        - compute.machineTypes.list
        - compute.urlMaps.list
        - compute.backendServices.list
        - compute.disks.list
        - compute.diskTypes.list
        - compute.autoscalers.list
        - compute.images.list
        - compute.subnetworks.list
        - compute.regionUrlMaps.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list
        
- Instance Group
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.zones.list
        - compute.regions.list
        - compute.instances.list
        - compute.machineTypes.list
        - compute.urlMaps.list
        - compute.backendServices.list
        - compute.disks.list
        - compute.diskTypes.list
        - compute.autoscalers.list
        - compute.images.list
        - compute.subnetworks.list
        - compute.regionUrlMaps.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list        
- Machine Images
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.zones.list
        - compute.regions.list
        - compute.instances.list
        - compute.machineTypes.list
        - compute.urlMaps.list
        - compute.backendServices.list
        - compute.disks.list
        - compute.diskTypes.list
        - compute.autoscalers.list
        - compute.images.list
        - compute.subnetworks.list
        - compute.regionUrlMaps.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list  
- Disk
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.disks.list
        - compute.resourcePolicies.list
  
- Snapshot
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.zones.list
        - compute.regions.list
        - compute.instances.list
        - compute.machineTypes.list
        - compute.urlMaps.list
        - compute.backendServices.list
        - compute.disks.list
        - compute.diskTypes.list
        - compute.autoscalers.list
        - compute.images.list
        - compute.subnetworks.list
        - compute.regionUrlMaps.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list  

#### VPC
- VPC Network

- Route

- External IP Address
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.forwardingRules.list
        - compute.addresses.list

- Firewall
- Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.forwardingRules.list
        - compute.addresses.list
#### Network Service
- Load Balancing

#### Cloud SQL
- Instance
    - Scopes 
        - https://www.googleapis.com/auth/cloud-platform
        - https://www.googleapis.com/auth/sqlservice.admin
        
    - IAM
        - sqladmin.instances.list
        - sqladmin.databases.list
        - sqladmin.users.list
        - sqladmin.backup_runs.list

#### Storage
- Bucket






