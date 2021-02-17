import logging

from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.error import *

__all__ = ['SnapshotConnector']
_LOGGER = logging.getLogger(__name__)


class SnapshotConnector(GoogleCloudConnector):
    google_client_service = 'compute'
    version = 'v1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def list_snapshot(self, **query):
        query = self.generate_query(**query)
        result = self.client.snapshots().list(**query).execute()
        return result.get('items', [])

    def list_resource_policies(self, **query):
        resource_policies = {}
        query = self.generate_query(**query)
        result = self.client.resourcePolicies().aggregatedList(**query).execute()
        all_results = result.get('items', {})
        for region in all_results.keys():
            if 'resourcePolicies' in all_results.get(region):
                for single_policy in all_results.get(region).get('resourcePolicies', []):
                    resource_policies[single_policy.get('selfLink')] = single_policy
        return resource_policies

    def list_all_disks_for_snapshots(self, **query):
        disk_with_schedule = {}
        query = self.generate_query(**query)
        result = self.client.disks().aggregatedList(**query).execute()
        all_results = result.get('items', {})
        for zone in all_results.keys():
            if 'disks' in all_results.get(zone):
                for disk in all_results.get(zone).get('disks', []):
                    if 'resourcePolicies' in disk:
                        zone_name_only = self._get_zone(disk.get('zone'))
                        disk_name = disk.get('name')
                        disk_with_schedule.update({
                            f'{disk_name}-{zone_name_only}': disk.get('resourcePolicies')
                        })
        return disk_with_schedule

    @staticmethod
    def _get_zone(zone: str):
        a = zone
        return a[a.rfind('zones/')+6:]