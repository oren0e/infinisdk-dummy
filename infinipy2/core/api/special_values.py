import itertools
import time
from uuid import uuid1

from ..._compat import iteritems


class SpecialValue(object):
    pass

OMIT = SpecialValue()

class Autogenerate(SpecialValue):
    """
    Designates a value that should be autogenerated upon request. The argument to the constructor is a
    template string. When formatted, these fields can be used:

    - ordinal: the number of times this template has been used already in this session
    - time: the current time, as a floating point number
    - timestamp: an integral value designating the current time (milliseconds)
    - uuid: a unique identifier generated from uuid1
    """

    _ORDINALS = {}

    def __init__(self, template):
        super(Autogenerate, self).__init__()
        self.template = template

    def generate(self):
        counter = self._ORDINALS.get(self.template, None)
        if counter is None:
            counter = self._ORDINALS[self.template] = itertools.count(1)
        current_time = time.time()
        return self.template.format(time=current_time, timestamp=int(current_time * 1000), ordinal=next(counter), uuid=_LAZY_UUID_FACTORY)

class _LazyUUIDFactory(object):
    def __str__(self):
        return str(uuid1()).lower().replace("-", "")

_LAZY_UUID_FACTORY = _LazyUUIDFactory()

def translate_special_values(d):
    for key, value in list(iteritems(d)):
        if isinstance(value, dict):
            translate_special_values(value)
        elif isinstance(value, SpecialValue):
            if value is OMIT:
                d.pop(key)
            elif isinstance(value, Autogenerate):
                d[key] = value.generate()
            else:
                raise NotImplementedError() # pragma: no cover
    return d
