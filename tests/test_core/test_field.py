import pytest
from infinisdk.core.field import Field
from infinisdk.core.utils import DONT_CARE


def test_field_cached():
    assert Field('testing_field').cached is DONT_CARE
    assert Field('testing_field', cached=True).cached is True
    assert Field('testing_field', cached=False).cached is False
    assert Field('testing_field', cached=DONT_CARE).cached is DONT_CARE


def test_identity_field_caching():
    # pylint: disable=expression-not-assigned
    assert Field('testing_field', is_identity=True).cached is True
    assert Field('testing_field', is_identity=True, cached=True).cached is True
    with pytest.raises(AssertionError):
        Field('testing_field', is_identity=True, cached=False).cached
    with pytest.raises(AssertionError):
        Field('testing_field', is_identity=True, cached=DONT_CARE).cached


def test_updater_toggle_name():
    assert Field('testing_field', toggle_name='my_toggle', type=bool, mutable=True).toggle_name == 'my_toggle'
    assert Field('testing_field', type=bool, mutable=False).toggle_name is None
    assert Field('testing_field', type=bool, mutable=True).toggle_name is 'testing_field'
    with pytest.raises(AssertionError):
        assert Field('testing_field', toggle_name='my_toggle', type=str, mutable=True)
    with pytest.raises(AssertionError):
        assert Field('testing_field', toggle_name='my_toggle', type=bool, mutable=False)
