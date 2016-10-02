from requests import codes
import pytest
import logbook

from infinisdk.infinibox.infinibox import InfiniBox
from infinisdk.core.exceptions import APICommandFailed, CacheMiss
from infinibox_sysdefs.defs import latest
from ..conftest import relevant_from_version

def test_login(infinibox):
    infinibox.login()

@relevant_from_version('3.0')
def test_is_logged_in(infinibox):
    assert infinibox.is_logged_in()
    infinibox.logout()
    assert not infinibox.is_logged_in()
    infinibox.login()
    assert infinibox.is_logged_in()

@relevant_from_version('3.0')
def test_is_logged_in_with_set_auth(infinibox):
    assert infinibox.is_logged_in()
    infinibox.api.set_auth('admin', '123456', login=False)
    assert not infinibox.is_logged_in()
    infinibox.api.set_auth('admin', '123456', login=True)
    assert infinibox.is_logged_in()

def test_passwords_are_not_logged(infinibox):
    with logbook.TestHandler() as handler:
        password = '12345678'
        infinibox.api.set_auth('user', password, login=False)
        with pytest.raises(APICommandFailed) as caught:
            infinibox.login()

        assert password not in str(caught.value)
        assert password not in caught.value.response.sent_data

    for record in handler.records:
        assert password not in record.message

def test_invalid_login(infinibox):
    with infinibox.api.get_auth_context('a', 'b', login=False):
        with pytest.raises(APICommandFailed) as caught:
            infinibox.login()

        assert caught.value.status_code in (codes.forbidden, codes.unauthorized)

@pytest.mark.parametrize('user_role', list(latest.enums.users.roles))
def test_after_loging_operations(infinibox, user_role):
    _PASS = '123456'
    infinibox_simulator = infinibox.get_simulator()
    user = infinibox.users.create(role=str(user_role), password=_PASS)

    infinibox2 = InfiniBox(infinibox_simulator, auth=None)
    infinibox2.api.set_auth(user.get_name(), _PASS, login=False)
    with pytest.raises(CacheMiss):
        infinibox2.components.system_component.get_field('name', from_cache=True, fetch_if_not_cached=False)
    infinibox2.login()
    infinibox2.components.system_component.get_field('name', from_cache=True, fetch_if_not_cached=False)


@relevant_from_version('3.0')
def test_reinitialize_session_keeps_cookies(infinibox):
    # pylint: disable=protected-access
    cookies = infinibox.api._session.cookies.copy()
    assert cookies
    assert infinibox.is_logged_in()
    infinibox.api.reinitialize_session()
    assert infinibox.api._session.cookies == cookies
    assert infinibox.is_logged_in()

@relevant_from_version('3.0')
def test_set_auth_no_login_doesnt_send_basic_auth(infinibox, infinibox_simulator):
    infinibox = InfiniBox(infinibox_simulator, auth=('infinidat', '123456'))
    infinibox.api.set_auth('admin', '123456', login=False)
    with pytest.raises(APICommandFailed) as caught:
        infinibox.api.get("volumes")
    assert caught.value.status_code == codes.unauthorized
