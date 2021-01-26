# plugin-google-cloud-services

![Google Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Google_Cloud.svg)
**Plugin to collect Google Cloud Services**

> SpaceONE's [plugin-google-cloud-services](https://github.com/spaceone-dev/plugin-google-cloud-services) is a convenient tool to 
get cloud service data from Google Cloud platform. 


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/google-cloud-services)
> Latest stable version : 1.1.3

Please contact us if you need any further information. (<support@spaceone.dev>)

---

## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data 
Please, set authentication privilege for followings:

### Contents

* Table of Contents
    * [Compute Engine](#compute-engine)
        * [Compute VM (Instance)](#compute-vminstance)
        * [Instance Template](#instance-template)
        * [Instance Group](#instance-group)
        * [Machine Images](#machine-images)
        * [Disk](#disk)
        * [Snapshot](#snapshot)
    * [VPC](#vpc)
        * [VPC Network](#vpc-network)
        * [Route](#route)
        * [External IP Address](#external-ip-address)
        * [Firewall](#firewall)
    * [Network Service](#network-service)
        * [Load Balancing](#load-balancing)
    * [Cloud SQL](#cloud-sql)
        * [Instance](#instance)
    * [Storage](#storage)
        * [Buckets](#Bucket)
    

---
#### [Compute Engine](https://cloud.google.com/compute/docs/apis)

- ##### Compute VM(Instance)
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
    
- ##### Instance Template
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instanceGroupManagers.list
        - compute.machineTypes.list
        - compute.disks.list
        - compute.instanceTemplates.list
        
- ##### Instance Group
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instanceGroups.list
        - compute.instanceGroupManagers.list
        - compute.instances.list
        - compute.autoscalers.list
        - compute.instanceTemplates.list
     
- #### Machine Images
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.machineImages.list
        - compute.machineTypes.list
        - compute.disks.list
        - compute.images.list
    
- #### Disk
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.disks.list
        - compute.resourcePolicies.list
  
- #### Snapshot
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.snapshots.list
        - compute.resourcePolicies.list
        - compute.disks.list
     

#### [VPC](https://cloud.google.com/compute/docs/apis)

- #### VPC Network
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.forwardingRules.list
        - compute.networks.list
        - compute.addresses.list
        - compute.globalAddresses.list
        - compute.subnetworks.list
        - compute.firewalls.list
        - compute.routes.list
        
- #### Route
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.routes.list
        - compute.instances.list
        
- #### External IP Address
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.forwardingRules.list
        - compute.addresses.list

- #### Firewall
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.firewalls.list


#### [Network Service](https://cloud.google.com/compute/docs/apis)
- #### Load Balancing
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.urlMaps.list
        - compute.backendBuckets.list
        - compute.backendServices.list
        - compute.targetPools.list
        - compute.forwardingRules.list
        - compute.targetGrpcProxies.list
        - compute.targetHttpProxies.list
        - compute.targetHttpsProxies.list
        - compute.targetGrpcProxies.list
        - compute.healthChecks.list
        - compute.httpHealthChecks.list
        - compute.httpsHealthChecks.list
        - compute.autoscalers.list
        

#### [Cloud SQL](https://cloud.google.com/sql/docs/mysql/apis)
- #### Instance
    - Scopes 
        - https://www.googleapis.com/auth/cloud-platform
        - https://www.googleapis.com/auth/sqlservice.admin
        
    - IAM
        - sqladmin.instances.list
        - sqladmin.databases.list
        - sqladmin.users.list
        - sqladmin.backup_runs.list

#### [Storage](https://cloud.google.com/storage/docs/apis)
- #### Bucket
    - IAM
        - storage.buckets.get
        - storage.objects.list
        - storage.objects.getIamPolicy2,6
            




