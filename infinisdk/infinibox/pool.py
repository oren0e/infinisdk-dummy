###!
### Infinidat Ltd.  -  Proprietary and Confidential Material
###
### Copyright (C) 2014, 2015, Infinidat Ltd. - All Rights Reserved
###
### NOTICE: All information contained herein is, and remains the property of Infinidat Ltd.
### All information contained herein is protected by trade secret or copyright law.
### The intellectual and technical concepts contained herein are proprietary to Infinidat Ltd.,
### and may be protected by U.S. and Foreign Patents, or patents in progress.
###
### Redistribution and use in source or binary forms, with or without modification,
### are strictly forbidden unless prior written permission is obtained from Infinidat Ltd.
###!
from capacity import TB
from ..core.type_binder import TypeBinder
from ..core import Field, CapacityType, MillisecondsDatetimeType
from ..core.api.special_values import Autogenerate
from .system_object import InfiniBoxObject
from ..core.bindings import ListOfRelatedObjectIDsBinding, InfiniSDKBindingWithSpecialFlags
from ..core.object_query import ObjectQuery
from ..core.utils import deprecated

from urlobject import URLObject


class PoolBinder(TypeBinder):
    """Implements *system.pools*
    """

    def get_administered_pools(self):
        """Returns the pools that can be managed by the current user
        """
        return ObjectQuery(self.system, URLObject('/api/rest/pools/administered_pools'), Pool)


class Pool(InfiniBoxObject):

    BINDER_CLASS = PoolBinder

    FIELDS = [
        Field("id", type=int, is_identity=True, is_filterable=True, is_sortable=True),
        Field("name", creation_parameter=True, mutable=True, is_filterable=True, is_sortable=True, default=Autogenerate("pool_{uuid}")),
        Field("virtual_capacity",  creation_parameter=True, mutable=True, default=TB, type=CapacityType, is_filterable=True, is_sortable=True),
        Field("physical_capacity", creation_parameter=True, mutable=True, default=TB, type=CapacityType, is_filterable=True, is_sortable=True),
        Field("owners", mutable=True, type=list, binding=ListOfRelatedObjectIDsBinding('users')),
        Field("allocated_physical_capacity", api_name="allocated_physical_space", type=CapacityType),
        Field("free_physical_capacity", api_name="free_physical_space", type=CapacityType),
        Field("free_virtual_capacity", api_name="free_virtual_space", type=CapacityType),
        Field("reserved_capacity", type=CapacityType),
        Field("created_at", type=MillisecondsDatetimeType, is_sortable=True, is_filterable=True),
        Field("updated_at", type=MillisecondsDatetimeType, is_sortable=True, is_filterable=True),
        Field("ssd_enabled", type=bool, mutable=True, creation_parameter=True, is_filterable=True, is_sortable=True, optional=True),
        Field("max_extend", type=CapacityType, mutable=True, binding=InfiniSDKBindingWithSpecialFlags([0, -1])),
        Field("state", cached=False),
    ]

    def get_volumes(self, **kwargs):
        return self.system.volumes.find(pool_id=self.id, **kwargs)

    def get_filesystems(self, **kwargs):
        return self.system.filesystems.find(pool_id=self.id, **kwargs)

    def _get_pool_owners_url(self, owner_id=None):
        url = self.get_this_url_path().add_path('owners')
        if owner_id:
            url = url.add_path(str(owner_id))
        return url

    @deprecated("Use set_owners instead")
    def add_owner(self, user):
        self.system.api.post(self._get_pool_owners_url(user.id), data={})

    @deprecated("Use set_owners instead")
    def discard_owner(self, user):
        self.system.api.delete(self._get_pool_owners_url(user.id), data={})

    def set_owners(self, users):
        url = self.get_this_url_path().add_path('owners')
        self.system.api.put(url, data=[user.id for user in users])

    def is_locked(self, *args, **kwargs):
        return self.get_state(*args, **kwargs) == 'LOCKED'

    def is_limited(self, *args, **kwargs):
        return self.get_state(*args, **kwargs) == 'LIMITED'

    def lock(self):
        self.system.api.post(self.get_this_url_path().add_path('lock'))

    def unlock(self):
        self.system.api.post(self.get_this_url_path().add_path('unlock'))
