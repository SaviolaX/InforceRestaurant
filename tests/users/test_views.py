import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User


client = APIClient()

@pytest.fixture
def user_data() -> dict:
    payload = dict(
        email='test_email@mail.com',
        username='test_username',
        password='test_password'
    )
    return payload

# login
@pytest.mark.django_db
def test_login_with_data_to_get_tokens(user_data: dict) -> None:
    User.objects.create_user(**user_data)
    res = client.post(reverse('login'), user_data, format='json')
    assert len(res.data) != 0
    assert type(res.data) == dict
    assert res.data['access'] != ''
    assert res.data['refresh'] != ''
    assert res.status_code == 200

@pytest.mark.django_db
def test_login_with_no_data_to_get_tokens(user_data: dict) -> None:
    User.objects.create_user(**user_data)
    res = client.post(reverse('login'), format='json')
    assert res.data['email'][0] == 'This field is required.'
    assert res.data['password'][0] == 'This field is required.'
    assert res.status_code == 400

# refresh token  
@pytest.mark.django_db
def test_login_with_data_refresh_token(user_data: dict) -> None:
    User.objects.create_user(**user_data)
    user_res = client.post(reverse('login'), user_data, format='json')
    refresh_token = dict(refresh=user_res.data['refresh'])
    res = client.post(reverse('login_refresh'), refresh_token, format='json')
    assert len(res.data) != 0
    assert type(res.data) == dict
    assert res.data['access'] != ''
    assert res.status_code == 200
    
@pytest.mark.django_db
def test_login_with_no_data_refresh_token() -> None:
    res = client.post(reverse('login_refresh'), format='json')
    assert res.data['refresh'][0] == 'This field is required.'
    assert res.status_code == 400
    
# logout
@pytest.mark.django_db
def test_user_logout_reset_token(user_data: dict) -> None:
    User.objects.create_user(**user_data)
    res_tokens = client.post(reverse('login'), user_data, format='json')
    res = client.post(reverse('logout'), res_tokens.data['refresh'], format='json')
    assert res.status_code == 205
    assert res.data == None

@pytest.mark.django_db
def test_logout_reset_tokens_without_refresh_token() -> None:
    res = client.post(reverse('logout'), format='json')
    assert res.status_code == 400
    
# register
@pytest.mark.django_db
def test_register_with_data(user_data: dict) -> None:
    users = User.objects.all()
    assert len(users) == 0
    res = client.post(reverse('register'), user_data, format='json')
    users = User.objects.all()
    assert len(users) == 1
    assert res.data['email'] == user_data['email']
    assert res.data['username'] == user_data['username']
    assert res.status_code == 201
    
    
@pytest.mark.django_db
def rest_register_with_no_data() -> None:
    users = User.objects.all()
    assert len(users) == 0
    res = client.post(reverse('register'), format='json')
    users = User.objects.all()
    assert len(users) == 0
    assert res.data['email'][0] == 'This field is required.'
    assert res.data['username'][0] == 'This field is required.'
    assert res.data['password'][0] == 'This field is required.'
    assert res.status_code == 400