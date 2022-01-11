# plugin-google-cloud-services

![Google Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/google_cloud/Google_Cloud.svg)
**Plugin to collect Google Cloud Services**

> SpaceONE's [plugin-google-cloud-services](https://github.com/spaceone-dev/plugin-google-cloud-services) is a convenient tool to 
get cloud service data from Google Cloud platform. 


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/google-cloud-services)


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
    * [Networking](#networking)
        * [VPC Network](#vpc-network)
        * [Route](#route)
        * [External IP Address](#external-ip-address)
        * [Firewall](#firewall)
        * [LoadBalancing](#loadbalancing)
    * [Cloud SQL](#cloud-sql)
        * [Instance](#instance)
    * [Storage](#storage)
        * [Buckets](#Bucket)
    * [BigQuery](#bigquery)
        * [SQLWorkspace](#SQLWorkspace)
    

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

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
    
- ##### Instance Template
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instanceGroupManagers.list
        - compute.machineTypes.list
        - compute.disks.list
        - compute.instanceTemplates.list
      
    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        
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
  
    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
     
- #### Machine Images
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.machineImages.list
        - compute.machineTypes.list
        - compute.disks.list
        - compute.images.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        
- #### Disk
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.disks.list
        - compute.resourcePolicies.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        
- #### Snapshot
    - Scopes
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.snapshots.list
        - compute.resourcePolicies.list
        - compute.disks.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
     

#### [Networking](https://cloud.google.com/compute/docs/apis)

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
        
    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        
- #### Route
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.routes.list
        - compute.instances.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        
- #### External IP Address
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.forwardingRules.list
        - compute.addresses.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}

- #### Firewall
    - Scopes 
        - https://www.googleapis.com/auth/compute
        - https://www.googleapis.com/auth/cloud-platform
        
    - IAM
        - compute.instances.list
        - compute.firewalls.list

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}

- #### LoadBalancing
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

    - Service Endpoint
        - https://compute.googleapis.com/compute/v1/projects/{project}/aggregated/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/global/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/zone/{zone}/{resource_name}
        - https://compute.googleapis.com/compute/v1/projects/{project}/regions/{region}/{resource_name}
        

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

    - Service Endpoint
        - https://sqladmin.googleapis.com/v1/projects/{project}/{resources}
        - https://sqladmin.googleapis.com/v1/projects/{project}/instances/{instance}/{resources}



#### [Storage](https://cloud.google.com/storage/docs/apis)
- #### Bucket
    - IAM
        - storage.buckets.get
        - storage.objects.list
        - storage.objects.getIamPolicy

    - Service Endpoint
        - https://storage.googleapis.com/storage/v1/b/{resource}

            
#### [BigQuery](https://cloud.google.com/bigquery/docs/reference)
- #### SQLWorkspace
    - IAM
        - bigquery.datasets.get
        - bigquery.tables.get
        - bigquery.tables.list
        - bigquery.jobs.list
        - resourcemanager.projects.get

    - Service Endpoint
        - https://bigquery.googleapis.com/bigquery/v2/projects/{projectId}/{resource}

---
## Options

### Cloud Service Type : Specify what to collect

If cloud_service_types is added to the list elements in options, only the specified cloud service type is collected.
By default, if cloud_service_types is not specified in options, all services are collected.

The cloud_service_types items that can be specified are as follows.

<pre>
<code>
{
    "cloud_service_types": [
    'SQLWorkspace',
    'CloudSQL',
    'Disk',
    'ExternalIPAddress',
    'Firewall',
    'InstanceGroup',
    'InstanceTemplate',
    'LoadBalancing',
    'MachineImage',
    'Route',
    'Snapshot',
    'Bucket',
    'VPCNetwork''
    ]
}
</code>
</pre>

How to update plugin information using spacectl is as follows.
First, create a yaml file to set options.

<pre>
<code>
> cat update_collector.yaml
---
collector_id: collector-xxxxxxx
options:
  cloud_service_types:
    - CloudSQL
    - VPCNetwork
</code>
</pre>

Update plugin through spacectl command with the created yaml file.

<pre><code>
> spacectl exec update_plugin inventory.Collector -f update_collector.yaml
</code></pre>


