import pytest
import flux
from ecosystem.mocks.mock_mailboxer import get_simulated_mail_server
import re

def test_name(infinibox, user):
    curr_name = user.get_name()
    new_name = 'other_user_name'
    user.update_name(new_name)

    assert curr_name.startswith('user_')
    assert curr_name != new_name
    assert user.get_name() == new_name

def test_creation(infinibox, user):
    kwargs = {"role": "ReadOnly",
              "name": "some_user_name",
              "email": "fake@email.com",
              "password": "some_password"}
    user = infinibox.users.create(**kwargs)

    assert user.get_name() == kwargs['name']
    assert user.get_role() == kwargs['role']
    assert user.get_email() == kwargs['email']
    assert user in infinibox.users.get_all()
    user.delete()
    assert (not user.is_in_system())

def test_password(infinibox, user):
    with pytest.raises(AttributeError):
        user.get_password()
    user.update_password('some_password')

def test_email(infinibox, user):
    orig_email = user.get_email()
    new_email = 'some@email.com'

    user.update_email(new_email)
    assert orig_email != new_email
    assert user.get_email() == new_email

def test_role(infinibox, user):
    orig_role = user.get_role()
    new_role = 'ReadOnly'

    user.update_role(new_role)
    assert orig_role != new_role
    assert user.get_role() == new_role

def test_get_pools(infinibox, user):
    flux.current_timeline.sleep(1)
    user = infinibox.users.create(role='PoolAdmin')
    assert user.get_pools() == []

    pool = infinibox.pools.create()
    pool.add_owner(user)

    pools = user.get_pools()
    assert len(pools) == 1
    assert pools[0] == pool

    pool.discard_owner(user)
    assert user.get_pools() == []

def _get_token_from_mail(simulator, mail_address):
    msg = _get_last_mailboxer_msg(simulator, mail_address)
    return re.findall("token=(.*)\"", msg.content)[0]

def _get_last_mailboxer_msg(simulator, mail_address):
    msg = get_simulated_mail_server(simulator).get_messages(mail_address)
    return msg[0]

def test_reset_password(infinibox, infinibox_simulator, user):
    user_email = user.get_email()
    user.request_reset_password()
    token = _get_token_from_mail(infinibox_simulator, user_email)
    user.reset_password(token)
    msg = _get_last_mailboxer_msg(infinibox_simulator, user_email)
    assert 'successfully' in msg.content
