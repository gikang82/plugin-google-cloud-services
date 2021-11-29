from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, ModelType
from .base import BaseMetaData, BaseResponse, MetaDataView, MetaDataViewSubData, ReferenceModel


class Labels(Model):
    key = StringType()
    value = StringType()


class CloudServiceMeta(BaseMetaData):
    @classmethod
    def set(cls):
        sub_data = MetaDataViewSubData()
        return cls({'view': MetaDataView({'sub_data': sub_data})})

    @classmethod
    def set_layouts(cls, layouts=[]):
        sub_data = MetaDataViewSubData({'layouts': layouts})
        return cls({'view': MetaDataView({'sub_data': sub_data})})


class CloudServiceResource(Model):
    provider = StringType(default="google_cloud")
    cloud_service_type = StringType()
    cloud_service_group = StringType()
    data = PolyModelType(Model, default=lambda: {})
    name = StringType(default="")
    reference = ModelType(ReferenceModel)
    region_code = StringType()
    tags = ListType(ModelType(Labels), serialize_when_none=False)
    _metadata = PolyModelType(CloudServiceMeta, serialize_when_none=False, serialized_name='metadata')


class CloudServiceResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id', 'provider', 'cloud_service_type', 'cloud_service_group']
    })
    resource_type = StringType(default='inventory.CloudService')
    resource = PolyModelType(CloudServiceResource)


class ErrorResource(Model):
    resource_type = StringType(default='inventory.CloudService')
    cloud_service_group = StringType(default='ComputeEngine', serialize_when_none=False)
    cloud_service_type = StringType(default='Instance', serialize_when_none=False)
    resource_id = StringType(serialize_when_none=False)


class ErrorResourceResponse(CloudServiceResponse):
    state = StringType(default='FAILURE')
    resource_type = StringType(default='inventory.ErrorResource')
    resource = ModelType(ErrorResource, default={})
