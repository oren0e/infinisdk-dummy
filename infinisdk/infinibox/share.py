from ..core import Field, MillisecondsDatetimeType
from ..core.api.special_values import Autogenerate
from ..core.bindings import RelatedObjectBinding, RelatedObjectNamedBinding
from ..core.translators_and_types import MunchListType
from .system_object import InfiniBoxObject


class Share(InfiniBoxObject):
    FIELDS = [
        Field("id", type=int, is_identity=True, is_filterable=True, is_sortable=True),
        Field(
            "name",
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
            default=Autogenerate("share_{uuid}"),
        ),
        Field(
            "inner_path",
            creation_parameter=True,
            optional=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "enabled",
            type=bool,
            mutable=True,
            optional=True,
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "offline_caching",
            mutable=True,
            optional=True,
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "access_based_enumeration",
            api_name="access_based_enumeration_enabled",
            type=bool,
            mutable=True,
            optional=True,
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "require_encryption",
            type=bool,
            mutable=True,
            optional=True,
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "snapdir_visible",
            type=bool,
            mutable=True,
            optional=True,
            creation_parameter=True,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "description",
            mutable=True,
            optional=True,
            creation_parameter=True,
        ),
        Field(
            "permissions",
            type=MunchListType,
        ),
        Field(
            "created_at",
            type=MillisecondsDatetimeType,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "updated_at",
            type=MillisecondsDatetimeType,
            is_filterable=True,
            is_sortable=True,
        ),
        Field(
            "filesystem",
            type="infinisdk.infinibox.filesystem:Filesystem",
            api_name="filesystem_id",
            binding=RelatedObjectNamedBinding(),
            is_filterable=True,
            is_sortable=True,
            creation_parameter=True,
        ),
        Field(
            "tenant",
            type="infinisdk.infinibox.tenant:Tenant",
            api_name="tenant_id",
            binding=RelatedObjectBinding("tenants"),
            is_filterable=True,
            is_sortable=True,
        ),
    ]

    @classmethod
    def is_supported(cls, system):
        return system.compat.has_native_smb()
