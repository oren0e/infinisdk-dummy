import pytest
from infinisdk.core import extensions
from infinisdk.infinibox import InfiniBox


def test_no_extensions_by_default():
    assert len(extensions.active) == 0

@pytest.mark.parametrize('different_name', [True, False])
def test_extending(infinibox, different_name):
    with pytest.raises(AttributeError):
        infinibox.new_method

    if different_name:
        @extensions.add_method(InfiniBox, 'new_method')
        def some_other_name(self, a, b, c):
            return "{0} {1} {2} {3}".format(type(self).__name__, a, b, c)

    else:
        @extensions.add_method(InfiniBox)
        def new_method(self, a, b, c):
            return "{0} {1} {2} {3}".format(type(self).__name__, a, b, c)

    assert infinibox.new_method(1, 2, 3) == 'InfiniBox 1 2 3'

