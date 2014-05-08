import abc
from ..._compat import with_metaclass
from .api import API
from ..type_binder_container import TypeBinderContainer
from ..config import config

class APITarget(with_metaclass(abc.ABCMeta)):
    """
    Abstract base class for anything that would like to become an API target
    """
    OBJECT_TYPES = []
    SYSTEM_EVENTS_TYPE = None
    SYSTEM_COMPONENTS_TYPE = None

    def __init__(self, address, auth=None):
        """
        :param address: Either a tuple of (host, port), or a list of such tuples for multiple addresses
        """
        if self._is_simulator(address):
            address = self._get_simulator_address(address)
        self._addresses = self._normalize_addresses(address)

        self.objects = TypeBinderContainer(self)

        if auth is None:
            auth = self._get_api_auth()
        self._auth = auth

        self._timeout = self._get_api_timeout()
        self.api = API(self)

        for object_type in self.OBJECT_TYPES:
            self.objects.install(object_type)

        self.components = self.SYSTEM_COMPONENTS_TYPE(self)
        self.events = self.SYSTEM_EVENTS_TYPE(self)

    def get_collections_names(self):
        return [obj_type.get_plural_name() for obj_type in self.OBJECT_TYPES]

    def _normalize_addresses(self, addresses):
        if not isinstance(addresses[0], (list, tuple)):
            addresses = [addresses]

        default_port = config.get_config('defaults.system_api_port').get_value()
        returned = []
        for address in addresses:
            if not isinstance(address, tuple):
                address = (address, default_port)
            if len(address) != 2:
                raise ValueError("Invalid address specified: {!r}".format(address))
            returned.append(address)
        return returned

    def get_api_addresses(self):
        return self._addresses

    def get_api_timeout(self):
        return self._timeout

    def get_api_auth(self):
        return self._auth

    def __repr__(self):
        return self._addresses[0][0]

    def _is_simulator(self, address):
        raise NotImplementedError() # pragma: no cover

    def _get_simulator_address(self, address):
        raise NotImplementedError() # pragma: no cover

    def _get_api_timeout(self):
        """
        :rtype: number of seconds to wait for a command to return before raising a timeout
        """
        raise NotImplementedError() # pragma: no cover

    def _get_api_auth(self):
        """
        :rtype: tuple of (username, password) to be used by default
        """
        raise NotImplementedError() # pragma: no cover

