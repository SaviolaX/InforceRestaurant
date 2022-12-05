import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from collections import OrderedDict

from restaurants.models import Restaurant
from users.models import User

client = APIClient()


@pytest.fixture
def user_payload_not_admin() -> dict:
    payload = dict(email='test_email@mail.com',
                   username='test_username',
                   password='test_password',
                   is_staff=False)
    return payload


@pytest.fixture
def user_payload_is_admin() -> dict:
    payload = dict(email='test_email@mail.com',
                   username='test_username',
                   password='test_password',
                   is_staff=True)
    return payload


@pytest.fixture
def rest_payload() -> dict:
    payload = dict(title='Test_restaurant#1')
    return payload


@pytest.fixture
def restaurant(rest_payload: dict) -> object:
    rest = Restaurant.objects.create(**rest_payload)
    return rest


# get restaurant view
@pytest.mark.django_db
def test_get_rest_not_auth(rest_payload: dict) -> None:
    Restaurant.objects.create(**rest_payload)
    res = client.get(reverse('get_rest', kwargs={'pk': 1}))
    assert res.data[
        'detail'] == 'Authentication credentials were not provided.'
    assert res.status_code == 401


@pytest.mark.django_db
def test_get_rest_auth(rest_payload: dict,
                       user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.get(reverse('get_rest', kwargs={'pk': 1}))
    assert res.data['id'] == 1
    assert res.data['title'] == rest_payload['title']
    assert res.status_code == 200


# create restaurant view
@pytest.mark.django_db
def test_create_rest_not_authenticated() -> None:
    res = client.post(reverse('create_rest'), format='json')
    assert res.status_code == 401


@pytest.mark.django_db
def test_create_rest_authenticated_but_not_admin(
        user_payload_not_admin: dict) -> None:
    User.objects.create_user(**user_payload_not_admin)
    user_data = client.post(reverse('login'),
                            user_payload_not_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.post(reverse('create_rest'), format='json')
    assert res.status_code == 403
    assert res.data[
        'detail'] == 'You do not have permission to perform this action.'


@pytest.mark.django_db
def test_create_rest_authenticated_as_admin_with_no_data(
        user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.post(reverse('create_rest'), format='json')
    assert res.status_code == 400
    assert res.data['title'][0] == 'This field is required.'


@pytest.mark.django_db
def test_create_rest_authenticated_as_admin_with_data(
        user_payload_is_admin: dict, rest_payload: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.post(reverse('create_rest'), rest_payload, format='json')
    assert res.status_code == 201
    assert res.data['id'] == 1
    assert res.data['title'] == rest_payload['title']


#  restaurants list view
@pytest.mark.django_db
def test_list_rest_not_auth(rest_payload: dict) -> None:
    Restaurant.objects.create(**rest_payload)
    res = client.get(reverse('list_rest'))
    assert res.status_code == 401


@pytest.mark.django_db
def test_list_rest_auth_as_admin(rest_payload: dict,
                                 user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.get(reverse('list_rest'))
    assert type(res.data[0]) == OrderedDict
    assert res.status_code == 200


@pytest.mark.django_db
def test_list_rest_auth_not_admin(rest_payload: dict,
                                  user_payload_not_admin: dict) -> None:
    User.objects.create_user(**user_payload_not_admin)
    Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_not_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.get(reverse('list_rest'))
    assert res.data[
        'detail'] == 'You do not have permission to perform this action.'
    assert res.status_code == 403


# update restaurant
@pytest.mark.django_db
def test_update_rest_not_auth(rest_payload: dict) -> None:
    Restaurant.objects.create(**rest_payload)
    res = client.post(reverse('update_rest', kwargs={'pk': 1}))
    assert res.status_code == 401


@pytest.mark.django_db
def test_update_rest_auth_as_admin(rest_payload: dict,
                                   user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    new_payload = dict(title='Test_restaurantEdited')
    res = client.patch(reverse('update_rest', kwargs={'pk': 1}),
                       new_payload,
                       format='json')
    assert res.data['title'] == new_payload['title']
    assert res.data['id'] == 1
    assert res.status_code == 200


@pytest.mark.django_db
def test_update_rest_auth_as_admin_no_data(
        rest_payload: dict, user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    rest = Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.patch(reverse('update_rest', kwargs={'pk': 1}), format='json')
    assert res.data['title'] == rest.title
    assert res.data['id'] == 1
    assert res.status_code == 200


@pytest.mark.django_db
def test_update_rest_auth_not_admin(rest_payload: dict,
                                    user_payload_not_admin: dict) -> None:
    User.objects.create_user(**user_payload_not_admin)
    Restaurant.objects.create(**rest_payload)
    user_data = client.post(reverse('login'),
                            user_payload_not_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    new_payload = dict(title='Test_restaurantEdited')
    res = client.patch(reverse('update_rest', kwargs={'pk': 1}),
                       new_payload,
                       format='json')
    assert res.data[
        'detail'] == 'You do not have permission to perform this action.'
    assert res.status_code == 403


# delete restaurant
@pytest.mark.django_db
def test_delete_rest_not_auth(rest_payload: dict) -> None:
    Restaurant.objects.create(**rest_payload)
    res = client.delete(reverse('delete_rest', kwargs={'pk': 1}))
    assert res.status_code == 401


@pytest.mark.django_db
def test_delete_rest_auth_as_admin(rest_payload: dict,
                                   user_payload_is_admin: dict) -> None:
    User.objects.create_user(**user_payload_is_admin)
    assert len(User.objects.all()) == 1
    Restaurant.objects.create(**rest_payload)
    assert len(Restaurant.objects.all()) == 1
    user_data = client.post(reverse('login'),
                            user_payload_is_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.delete(reverse('delete_rest', kwargs={'pk': 1}))
    assert res.status_code == 204
    assert len(Restaurant.objects.all()) == 0


@pytest.mark.django_db
def test_delete_rest_auth_not_admin(rest_payload: dict,
                                    user_payload_not_admin: dict) -> None:
    User.objects.create_user(**user_payload_not_admin)
    assert len(User.objects.all()) == 1
    Restaurant.objects.create(**rest_payload)
    assert len(Restaurant.objects.all()) == 1
    user_data = client.post(reverse('login'),
                            user_payload_not_admin,
                            format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.delete(reverse('delete_rest', kwargs={'pk': 1}),
                        format='json')
    assert res.data[
        'detail'] == 'You do not have permission to perform this action.'
    assert res.status_code == 403
