from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse


class GoogleCloudManager(BaseManager):
    connector_name = None
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: GoogleCloudConnector = self.locator.get_connector('GoogleCloudConnector', secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        for cloud_service_type in self.collect_cloud_service_type():
            yield cloud_service_type

        # Add zone lists in params
        params.update({
            'zones': self.list_zones(params['secret_data'])
        })

        for cloud_service_response_schema in self.collect_cloud_service(params):
            yield cloud_service_response_schema

        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                yield RegionResponse({'resource': region})

    def list_zones(self, secret_data):
        query = {}

        if secret_data.get('region_name'):
            region_self_link = f'https://www.googleapis.com/compute/v1/projects/{secret_data["project_id"]}/regions/{secret_data.get("region_name")}'
            query.update({'filter': f'region="{region_self_link}"'})

        connector: GoogleCloudConnector = self.locator.get_connector('GoogleCloudConnector', secret_data=secret_data)
        zones = connector.list_zones(**query)
        return [zone.get('name') for zone in zones if zone.get('name')]

    def set_region_code(self, region):
        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    def generate_region_from_zone_self_link(self, zone_self_link):
        _split = zone_self_link.split('/')
        return self.generate_region_from_zone(_split[-1])

    @staticmethod
    def generate_region_from_zone(zone):
        return zone[:-2]


    @staticmethod
    def match_region_info(region_code):
        REGION_INFO = {
            'asia-east1': {'region_code': 'asia-east1',
                           'name': 'Changhua County, Taiwan, APAC',
                           'tags': {'latitude': '', 'longitude': ''}},
            'asia-east2': {'region_code': 'asia-east2',
                           'name': 'Hong Kong, APAC',
                           'tags': {'latitude': '', 'longitude': ''}},
            'asia-northeast1': {'region_code': 'asia-northeast1',
                                'name': 'Tokyo, Japan, APAC',
                                'tags': {'latitude': '', 'longitude': ''}},
            'asia-northeast2': {'region_code': 'asia-northeast2',
                                'name': 'Osaka, Japan, APAC',
                                'tags': {'latitude': '', 'longitude': ''}},
            'asia-northeast3': {'region_code': 'asia-northeast3',
                                'name': 'Seoul, South Korea, APAC',
                                'tags': {'latitude': '', 'longitude': ''}},
            'asia-south1': {'region_code': 'asia-south1',
                            'name': 'Mumbai, India APAC',
                            'tags': {'latitude': '', 'longitude': ''}},
            'asia-southeast1': {'region_code': 'asia-southeast1',
                                'name': 'Jurong West, Singapore, APAC',
                                'tags': {'latitude': '', 'longitude': ''}},
            'asia-southeast2': {'region_code': 'asia-southeast2',
                                'name': 'Jakarta, Indonesia, APAC',
                                'tags': {'latitude': '', 'longitude': ''}},
            'australia-southeast1': {'region_code': 'australia-southeast1',
                                     'name': 'Sydney, Australia, APAC',
                                     'tags': {'latitude': '', 'longitude': ''}},
            'europe-north1': {'region_code': 'europe-north1',
                              'name': 'Hamina, Finland, Europe',
                              'tags': {'latitude': '', 'longitude': ''}},
            'europe-west1': {'region_code': 'europe-west1',
                             'name': 'St. Ghislain, Belgium, Europe',
                             'tags': {'latitude': '', 'longitude': ''}},
            'europe-west2': {'region_code': 'europe-west2',
                             'name': 'London, England, Europe',
                             'tags': {'latitude': '', 'longitude': ''}},
            'europe-west3': {'region_code': 'europe-west3',
                             'name': 'Frankfurt, Germany Europe',
                             'tags': {'latitude': '', 'longitude': ''}},
            'europe-west4': {'region_code': 'europe-west4',
                             'name': 'Eemshaven, Netherlands, Europe',
                             'tags': {'latitude': '', 'longitude': ''}},
            'europe-west6': {'region_code': 'europe-west6',
                             'name': 'Zurich, Switzerland, Europe',
                             'tags': {'latitude': '', 'longitude': ''}},
            'northamerica-northeast1': {'region_code': 'northamerica-northeast1',
                                        'name': 'Montréal, Québec, North America',
                                        'tags': {'latitude': '', 'longitude': ''}},
            'southamerica-east1': {'region_code': 'southamerica-east1',
                                   'name': 'Osasco, São Paulo, Brazil, South America',
                                   'tags': {'latitude': '', 'longitude': ''}},
            'us-central1': {'region_code': 'us-central1',
                            'name': 'Council Bluffs, Iowa, North America',
                            'tags': {'latitude': '', 'longitude': ''}},
            'us-east1': {'region_code': 'us-east1',
                         'name': 'Moncks Corner, South Carolina, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
            'us-east4': {'region_code': 'us-east4',
                         'name': 'Ashburn, Virginia, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
            'us-west1': {'region_code': 'us-west1',
                         'name': 'The Dalles, Oregon, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
            'us-west2': {'region_code': 'us-west2',
                         'name': 'Los Angeles, California, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
            'us-west3': {'region_code': 'us-west3',
                         'name': 'Salt Lake City, Utah, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
            'us-west4': {'region_code': 'us-west4',
                         'name': 'Las Vegas, Nevada, North America',
                         'tags': {'latitude': '', 'longitude': ''}},
        }

        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            return RegionResource(match_region_info, strict=False)

        return None
