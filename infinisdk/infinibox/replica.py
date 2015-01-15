###!
### Infinidat Ltd.  -  Proprietary and Confidential Material
###
### Copyright (C) 2014, Infinidat Ltd. - All Rights Reserved
###
### NOTICE: All information contained herein is, and remains the property of Infinidat Ltd.
### All information contained herein is protected by trade secret or copyright law.
### The intellectual and technical concepts contained herein are proprietary to Infinidat Ltd.,
### and may be protected by U.S. and Foreign Patents, or patents in progress.
###
### Redistribution and use in source or binary forms, with or without modification,
### are strictly forbidden unless prior written permission is obtained from Infinidat Ltd.
###!
from ..core.api.special_values import Autogenerate
from ..core.type_binder import TypeBinder
from ..core import Field
from ..core.bindings import RelatedObjectBinding
from .system_object import InfiniBoxObject


class ReplicaBinder(TypeBinder):
    """Implements *system.replicas*
    """

    def replicate_volume(self, volume, link, remote_pool):
        """Replicates a volume, creating its remote replica on the specified pool"""
        return self.create(
            link=link, remote_pool_id=remote_pool.id,
            entity_pairs = [{
                'local_entity_id': volume.id,
                'remote_base_action': 'CREATE',
            }], entity_type='VOLUME')



class Replica(InfiniBoxObject):

    BINDER_CLASS = ReplicaBinder

    FIELDS = [

        Field('id', type=int, is_identity=True),
        Field('link', api_name='link_id', binding=RelatedObjectBinding('links'), type='infinisdk.infinibox.link:Link', creation_parameter=True),
        Field("name", creation_parameter=True, mutable=True, is_filterable=True,
            default=Autogenerate("replica_{uuid}")),
        Field('entity_pairs', type=list, creation_parameter=True),
        Field('sync_interval', type=int, creation_parameter=True, default=30000),
        Field('entity_type', type=str, creation_parameter=True, default='VOLUME'),
        Field('remote_pool_id', type=int, creation_parameter=True),

    ]


