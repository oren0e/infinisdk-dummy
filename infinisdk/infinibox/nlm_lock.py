from ..core.system_object import BaseSystemObject
from ..core.type_binder import TypeBinder
from ..core.api.special_values import OMIT
from ..core.bindings import RelatedObjectNamedBinding
from ..core import Field
from urlobject import URLObject as URL

class NlmLockTypeBinder(TypeBinder):
    def break_lock(self, lock_id=OMIT, filesystem_id=OMIT, file_path=OMIT, client=OMIT):
        data = {'lock_id': lock_id, 'filesystem_id': filesystem_id, 'file_path': file_path, 'client': client}
        url = URL(self.object_type.get_url_path(self.system))
        return self.system.api.post(url.add_path('break'), data=data)

    def remove_orphan(self):
        url = URL(self.object_type.get_url_path(self.system))
        return self.system.api.post(url.add_path('remove_orphan'))

class NlmLock(BaseSystemObject):
    BINDER_CLASS = NlmLockTypeBinder

    @classmethod
    def get_tags_for_object_operations(cls, system):
        return [cls.get_type_name().lower(), system.get_type_name().lower()]

    @classmethod
    def get_type_name(cls):
        return 'nlm_lock'

    FIELDS = [
        Field("lock_id", type=str, is_identity=True, is_filterable=True, is_sortable=True),
        Field("filesystem", type='infinisdk.infinibox.filesystem:Filesystem', api_name="filesystem_id",
              is_filterable=True, is_sortable=True, binding=RelatedObjectNamedBinding()),
        Field("file_path", type=str, is_filterable=True, is_sortable=True),
        Field("file_path_status", type=str, is_filterable=True, is_sortable=True),
        Field("client", type=str, is_filterable=True, is_sortable=True),
        Field("state", type=str, is_filterable=True, is_sortable=True),
        Field("offset", type=int),
        Field("length", type=int),
        Field("lock_type", type=str, is_filterable=True, is_sortable=True),
        Field("granted_at", type=int, is_filterable=True, is_sortable=True),
        Field("owner", type=str, is_filterable=True, is_sortable=True),
    ]

    @classmethod
    def is_supported(cls, system):
        return system.compat.has_nlm()
