import math
from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import GoogleCloudConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse

REGION_INFO = {
    "asia-east1": {"name": "Taiwan (Changhua County)", "tags": {"latitude": "24.051196", "longitude": "120.516430"}},
    "asia-east2": {"name": "Hong Kong", "tags": {"latitude": "22.283289", "longitude": "114.155851"}},
    "asia-northeast1": {"name": "Japan (Tokyo)", "tags": {"latitude": "35.628391", "longitude": "139.417634"}},
    "asia-northeast2": {"name": "Japan (Osaka)", "tags": {"latitude": "34.705403", "longitude": "135.490119"}},
    "asia-northeast3": {"name": "South Korea (Seoul)", "tags": {"latitude": "37.499968", "longitude": "127.036376"}},
    "asia-south1": {"name": "India (Mumbai)", "tags": {"latitude": "19.164951", "longitude": "72.851765"}},
    "asia-southeast1": {"name": "Singapore (Jurong West)", "tags": {"latitude": "1.351376", "longitude": "103.709574"}},
    "asia-southeast2": {"name": "Indonesia (Jakarta)", "tags": {"latitude": "-6.227851", "longitude": "106.808169"}},
    "australia-southeast1": {"name": "Australia (Sydney)", "tags": {"latitude": "-33.733694", "longitude": "150.969840"}},
    "europe-north1": {"name": "Finland (Hamina)", "tags": {"latitude": "60.539504", "longitude": "27.113819"}},
    "europe-west1": {"name": "Belgium (St.Ghislain)", "tags": {"latitude": "50.471248", "longitude": "3.825493"}},
    "europe-west2": {"name": "England, UK (London)", "tags": {"latitude": "51.515998", "longitude": "-0.126918"}},
    "europe-west3": {"name": "Germany (Frankfurt)", "tags": {"latitude": "50.115963", "longitude": "8.669625"}},
    "europe-west4": {"name": "Netherlands (Eemshaven)", "tags": {"latitude": "53.427625", "longitude": "6.865703"}},
    "europe-west6": {"name": "Switzerland (Zürich)", "tags": {"latitude": "47.365663", "longitude": "8.524881"}},
    "northamerica-northeast1": {"name": "Canada, Québec (Montréal)", "tags": {"latitude": "45.501926", "longitude": "-73.570086"}},
    "southamerica-east1": {"name": "Brazil, São Paulo (Osasco)", "tags": {"latitude": "43.8345", "longitude": "2.1972"}},
    "us-central1": {"name": "US, Iowa (Council Bluffs)", "tags": {"latitude": "41.221419", "longitude": "-95.862676"}},
    "us-east1": {"name": "US, South Carolina (Moncks Corner)", "tags": {"latitude": "33.203394", "longitude": "-79.986329"}},
    "us-east4": {"name": "US, Northern Virginia (Ashburn)", "tags": {"latitude": "39.021075", "longitude": "-77.463569"}},
    "us-west1": {"name": "US, Oregon (The Dalles)", "tags": {"latitude": "45.631800", "longitude": "-121.200921"}},
    "us-west2": {"name": "US, California (Los Angeles)", "tags": {"latitude": "34.049329", "longitude": "-118.255265"}},
    "us-west3": {"name": "US, Utah (Salt Lake City)", "tags": {"latitude": "40.730109", "longitude": "-111.951386"}},
    "us-west4": {"name": "US, Nevada (Las Vegas)", "tags": {"latitude": "36.092498", "longitude": "-115.086073"}},
    "global": {"name": "Global"}
}


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
        resources = []

        # Collect Cloud Service Type
        resources.extend(self.collect_cloud_service_type())

        # Collect Cloud Service
        resources.extend(self.collect_cloud_service(params))

        # Collect Region
        resources.extend(self.collect_region())

        return resources

    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({'resource': region}))

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = 'global'

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
        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_code
            })
            return RegionResource(region_info, strict=False)

        return None

    @staticmethod
    def convert_labels_format(labels):
        convert_labels = []
        for k, v in labels.items():
            convert_labels.append({
                'key': k,
                'value': v
            })
        return convert_labels

    @staticmethod
    def _convert_size(size_bytes):
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    @staticmethod
    def convertMillis(millis):
        s = millis / 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)

        return d, h, m, s