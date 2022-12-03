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

from PIL import Image

from restaurants.models import Restaurant
from users.models import User
from menus.models import Menu

client = APIClient()


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
def user_payload_as_admin() -> dict:
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


# get menu view
@pytest.mark.django_db
def test_get_menu_not_auth(restaurant) -> None:
    menu = Menu.objects.create(
        title='test_menu',
        file = SimpleUploadedFile('temp_file.pdf', b'some test content'),
        restaurant=restaurant
    )
    menu = client.get(reverse('get_menu', kwargs={'pk': 1}))
    assert menu.data['detail'] == 'Authentication credentials were not provided.'
    assert menu.status_code == 401
    delete_all_temp_files()


@pytest.mark.django_db
def test_get_menu_auth_as_admin(restaurant: object, user_payload_as_admin: dict) -> None:
    menu = Menu.objects.create(
        title='test_menu',
        file = SimpleUploadedFile('temp_file.pdf', b'some test content'),
        restaurant=restaurant
    )
    User.objects.create_user(**user_payload_as_admin)
    user_data = client.post(reverse('login'), user_payload_as_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    menu = client.get(reverse('get_menu', kwargs={'pk': 1}))
    assert menu.status_code == 200
    assert menu.data['file'].split('/')[-1] == 'temp_file.pdf'
    assert menu.data['title'] == 'test_menu'
    assert menu.data['restaurant'] == restaurant.id
    delete_all_temp_files()
    

# create menu view
@pytest.mark.django_db
def test_create_menu_not_authenticated() -> None:
    res = client.post(reverse('create_rest'), format='json')
    assert res.status_code == 401
    
@pytest.mark.django_db
def test_create_menu_authenticated_but_not_admin(user_payload_not_admin:dict, restaurant: object) -> None:
    payload = dict(
        title='test_title',
        file='temp_file.pdf',
        restaurant=restaurant.id
    )
    User.objects.create_user(**user_payload_not_admin)
    user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.post(reverse('create_menu'), payload, format='json')
    assert res.status_code == 403
    assert res.data['detail'] == 'You do not have permission to perform this action.'

    
@pytest.mark.django_db
def test_create_menu_authenticated_as_admin_with_no_data(user_payload_as_admin:dict) -> None:
    User.objects.create_user(**user_payload_as_admin)
    user_data = client.post(reverse('login'), user_payload_as_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.post(reverse('create_menu'), format='json')
    assert res.status_code == 400
    assert res.data['title'][0] == 'This field is required.'
    assert res.data['file'][0] == 'No file was submitted.'
    assert res.data['restaurant'][0] == 'This field is required.'
    
@pytest.mark.django_db
def test_create_menu_authenticated_as_admin_with_data(user_payload_as_admin:dict, restaurant: object) -> None:
    temp_file = tempfile.TemporaryFile(suffix='.pdf', prefix='temp_', dir=os.path.join(settings.BASE_DIR/'media/menus'))
    temp_file.write(b'some content')
    temp_file.seek(0)
    payload = dict(
        title='test_menu', 
        file=temp_file, 
        restaurant=restaurant.id
    )
    User.objects.create_user(**user_payload_as_admin)
    user_data = client.post(reverse('login'), user_payload_as_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    assert len(Menu.objects.all()) == 0
    res = client.post(reverse('create_menu'), payload, format='multipart')
    assert res.status_code == 201
    assert res.data['id'] == 1
    assert res.data['title'] == payload['title']
    assert res.data['restaurant'] == payload['restaurant']
    assert len(Menu.objects.all()) == 1
    

#  restaurants list view
@pytest.mark.django_db
def test_list_menu_not_auth(restaurant:object) -> None:
    assert len(Menu.objects.all()) == 0
    Menu.objects.create(
        title='test_menu',
        file = SimpleUploadedFile('temp_file.pdf', b'some test content'),
        restaurant=restaurant
    )
    assert len(Menu.objects.all()) == 1
    res = client.get(reverse('list_menu'))
    assert res.status_code == 401
    delete_all_temp_files()
    
@pytest.mark.django_db
def test_list_menu_auth_as_admin(user_payload_as_admin:dict, restaurant:object) -> None:
    assert len(Menu.objects.all()) == 0
    Menu.objects.create(
        title='test_menu',
        file = SimpleUploadedFile('temp_file.pdf', b'some test content'),
        restaurant=restaurant
    )
    assert len(Menu.objects.all()) == 1
    User.objects.create_user(**user_payload_as_admin)
    user_data = client.post(reverse('login'), user_payload_as_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.get(reverse('list_menu'))
    assert type(res.data[0]) == OrderedDict
    assert res.status_code == 200
    delete_all_temp_files()
    
@pytest.mark.django_db
def test_list_menu_auth_not_admin(restaurant: object, user_payload_not_admin:dict) -> None:
    assert len(Menu.objects.all()) == 0
    Menu.objects.create(
        title='test_menu',
        file = SimpleUploadedFile('temp_file.pdf', b'some test content'),
        restaurant=restaurant
    )
    assert len(Menu.objects.all()) == 1
    User.objects.create_user(**user_payload_not_admin)
    user_data = client.post(reverse('login'), user_payload_not_admin, format='json')
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_data.data['access'])
    res = client.get(reverse('list_menu'))
    assert type(res.data[0]) == OrderedDict
    assert res.status_code == 200
    delete_all_temp_files()
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
    

def delete_all_temp_files():
    """
        remove all temporary created files for tests
    """
    files = os.listdir(settings.BASE_DIR/'media/menus')
    for x in files:
        splited = x.split('_')
        if splited[0] == 'temp':
            abs_path = os.path.join(settings.BASE_DIR/'media/menus/', x)
            os.remove(abs_path)
        else:
            pass