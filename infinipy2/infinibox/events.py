from ..core import Events as EventsBase
from ..core import Field, SystemObject
from ..core.api.special_values import Autogenerate


class Events(EventsBase):

    def create_custom_event(self,
                            level='INFO',
                            description='custom event',
                            visibility='INFINIDAT',
                            data=None):

        _data = {"data": data or [],
                 "level": level,
                 "description_template": description,
                 "visibility":visibility}
        return self.system.api.post("events/custom", data=_data).get_result()

    def get_levels(self):
        sorted_levels = sorted(self._get_events_types()['levels'], key=lambda d: d['value'])
        return [level_info['name'] for level_info in sorted_levels]

    def get_levels_name_to_number_mapping(self):
        return {level_info['name']: level_info['value'] for level_info in self._get_events_types()['levels']}


class EmailRule(SystemObject):

    URL_PATH = "/api/rest/events/mail"

    FIELDS = [
        Field("id", type=int, is_identity=True, is_filterable=True, is_sortable=True),
        Field("visibility", creation_parameter=True, default="CUSTOMER", is_filterable=True, is_sortable=True),
        Field("filters", creation_parameter=True, type=list, default=list),
        Field("recipients", creation_parameter=True, type=list, default=["a@a.com"]),
        Field("name", creation_parameter=True, default=Autogenerate("rule_{timestamp}"), is_filterable=True, is_sortable=True),
    ]
