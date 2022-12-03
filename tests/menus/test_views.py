import pytest, tempfile, os
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib import auth
from collections import OrderedDict
from unittest.mock import Mock, patch
from django.core.files import File
from io import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import tempfile
import shutil

from restaurants.models import Restaurant
from users.models import User
from menus.models import Menu

client = APIClient()

@pytest.fixture
def mock_file_inst():
    mock_file = Mock(spec=File, name = 'test_file.pdf')
    return mock_file

@pytest.fixture
def user_payload_not_admin() -> dict:
    payload = dict(
        email='test_email@mail.com',
        username='test_username',
        password='test_password',
        is_staff=False
    )
    return payload


@pytest.fixture
def user_payload_is_admin() -> dict:
    payload = dict(
        email='test_email@mail.com',
        username='test_username',
        password='test_password',
        is_staff=True
    )
    return payload


@pytest.fixture
def restaurant() -> object:
    payload = dict(
        title='Test_restaurant#1'
    )
    rest = Restaurant.objects.create(**payload)
    return rest

@pytest.fixture
def menu_payload(restaurant) -> dict:
    payload = dict(
        title='test_menu',
        file='temp.pdf',
        restaurant=restaurant
    )
    return payload



# # get menu view
# @pytest.mark.django_db
# def test_get_menu_not_auth(restaurant) -> None:
#     menu = Menu.objects.create(
#         title='test_menu',
#         file = SimpleUploadedFile('test_.pdf', b'some test content'),
#         restaurant=restaurant
#     )
#     menu = client.get(reverse('get_menu', kwargs={'pk': 1}))
#     assert menu.data['detail'] == 'Authentication credentials were not provided.'
#     assert menu.status_code == 401


# @pytest.mark.django_db
# def test_get_menu_auth_as_admin(restaurant) -> None:
#     menu = Menu.objects.create(
#         title='test_menu',
#         file = SimpleUploadedFile('test_.pdf', b'some test content'),
#         restaurant=restaurant
#     )
#     print(menu)
    
    # User.objects.create_user(**user_payload_is_admin)
    # Menu.objects.create(**menu_payload)
    # user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
    # client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    # menu = client.get(reverse('get_menu', kwargs={'pk': 1}))
    # assert menu.data['id'] == 1
    # assert menu.data['title'] == menu_payload['title']
    # assert menu.data['file'] == menu_payload['file']
    # assert menu.data['restaurant'] == menu_payload['restaurant']
    # assert menu.status_code == 200
    # print(menu)
    # print(menu.data)


# # create restaurant view
# @pytest.mark.django_db
# def test_create_rest_not_authenticated() -> None:
#     res = client.post(reverse('create_rest'), format='json')
#     assert res.status_code == 401
    
# @pytest.mark.django_db
# def test_create_rest_authenticated_but_not_admin(user_payload_not_admin:dict) -> None:
#     User.objects.create_user(**user_payload_not_admin)
#     user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.post(reverse('create_rest'), format='json')
#     assert res.status_code == 403
#     assert res.data['detail'] == 'You do not have permission to perform this action.'
    
# @pytest.mark.django_db
# def test_create_rest_authenticated_as_admin_with_no_data(user_payload_is_admin:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.post(reverse('create_rest'), format='json')
#     assert res.status_code == 400
#     assert res.data['title'][0] == 'This field is required.'
    
# @pytest.mark.django_db
# def test_create_rest_authenticated_as_admin_with_data(user_payload_is_admin:dict, rest_payload:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.post(reverse('create_rest'), rest_payload, format='json')
#     assert res.status_code == 201
#     assert res.data['id'] == 1
#     assert res.data['title'] == rest_payload['title']
    

# #  restaurants list view
# @pytest.mark.django_db
# def test_list_rest_not_auth(rest_payload: dict) -> None:
#     Restaurant.objects.create(**rest_payload)
#     res = client.get(reverse('list_rest'))
#     assert res.status_code == 401
    
# @pytest.mark.django_db
# def test_list_rest_auth_as_admin(rest_payload: dict, user_payload_is_admin:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     Restaurant.objects.create(**rest_payload)
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.get(reverse('list_rest'))
#     assert type(res.data[0]) == OrderedDict
#     assert res.status_code == 200
    
# @pytest.mark.django_db
# def test_list_rest_auth_not_admin(rest_payload: dict, user_payload_not_admin:dict) -> None:
#     User.objects.create_user(**user_payload_not_admin)
#     Restaurant.objects.create(**rest_payload)
#     user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.get(reverse('list_rest'))
#     assert res.data['detail'] == 'You do not have permission to perform this action.'
#     assert res.status_code == 403
    
# # update restaurant
# @pytest.mark.django_db
# def test_update_rest_not_auth(rest_payload: dict) -> None:
#     Restaurant.objects.create(**rest_payload)
#     res = client.post(reverse('update_rest', kwargs={'pk': 1}))
#     assert res.status_code == 401
    
# @pytest.mark.django_db
# def test_update_rest_auth_as_admin(rest_payload: dict, user_payload_is_admin:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     Restaurant.objects.create(**rest_payload)
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     new_payload = dict(title='Test_restaurantEdited')
#     res = client.patch(reverse('update_rest', kwargs={'pk': 1}), new_payload, format='json')
#     assert res.data['title'] == new_payload['title']
#     assert res.data['id'] == 1
#     assert res.status_code == 200
    
# @pytest.mark.django_db
# def test_update_rest_auth_as_admin_no_data(rest_payload: dict, user_payload_is_admin:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     rest = Restaurant.objects.create(**rest_payload)
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.patch(reverse('update_rest', kwargs={'pk': 1}), format='json')
#     assert res.data['title'] == rest.title
#     assert res.data['id'] == 1
#     assert res.status_code == 200
    
# @pytest.mark.django_db
# def test_update_rest_auth_not_admin(rest_payload: dict, user_payload_not_admin:dict) -> None:
#     User.objects.create_user(**user_payload_not_admin)
#     Restaurant.objects.create(**rest_payload)
#     user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     new_payload = dict(title='Test_restaurantEdited')
#     res = client.patch(reverse('update_rest', kwargs={'pk': 1}), new_payload, format='json')
#     assert res.data['detail'] == 'You do not have permission to perform this action.'
#     assert res.status_code == 403
    
    
# # delete restaurant
# @pytest.mark.django_db
# def test_delete_rest_not_auth(rest_payload: dict) -> None:
#     Restaurant.objects.create(**rest_payload)
#     res = client.delete(reverse('delete_rest', kwargs={'pk': 1}))
#     assert res.status_code == 401
    
# @pytest.mark.django_db
# def test_delete_rest_auth_as_admin(rest_payload: dict, user_payload_is_admin:dict) -> None:
#     User.objects.create_user(**user_payload_is_admin)
#     assert len(User.objects.all()) == 1
#     Restaurant.objects.create(**rest_payload)
#     assert len(Restaurant.objects.all()) == 1
#     user_data = client.post(reverse('login'), user_payload_is_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.delete(reverse('delete_rest', kwargs={'pk': 1}))
#     assert res.status_code == 204
#     assert len(Restaurant.objects.all()) == 0
    
# @pytest.mark.django_db
# def test_delete_rest_auth_not_admin(rest_payload: dict, user_payload_not_admin:dict) -> None:
#     User.objects.create_user(**user_payload_not_admin)
#     assert len(User.objects.all()) == 1
#     Restaurant.objects.create(**rest_payload)
#     assert len(Restaurant.objects.all()) == 1
#     user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
#     res = client.delete(reverse('delete_rest', kwargs={'pk': 1}), format='json')
#     assert res.data['detail'] == 'You do not have permission to perform this action.'
#     assert res.status_code == 403
    

def test_delete_all_temp_files():
    files = os.listdir(settings.BASE_DIR/'media/menus')
    for x in files:
        file = x.split('_')
        if file[0] == 'test':
            os.remove(x)
        else:
            pass