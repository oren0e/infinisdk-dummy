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
from urlobject import URLObject as URL
from ..core.bindings import RelatedObjectBinding
from ..core import Field, SystemObject


class NotificationRule(SystemObject):


    URL_PATH = URL('/api/rest/notifications/rules')

    FIELDS = [
        Field('id', type=int, is_identity=True),
        Field('name', mutable=True),
        Field('event_code', type=str),
        Field('event_level', type=list),
        Field('target_parameters', type=dict),
        Field('target', api_name='target_id', binding=RelatedObjectBinding('notification_targets')),
        Field('include_events', type=list),
        Field('exclude_events', type=list),
        Field('event_visibility', type=list),
    ]

    @classmethod
    def get_type_name(cls):
        return 'notification_rule'
