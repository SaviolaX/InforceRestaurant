import pytest

from users.models import User
from restaurants.models import Restaurant

@pytest.fixture
def user_no_restaurant():
    return User.objects.create_user(email='test@email.com',
                                    username='test_username',
                                    password='test_password')
    
@pytest.fixture
def user_with_restaurant():
    rest = Restaurant.objects.create(title='Test_restaurant')
    return User.objects.create_user(email='test@email.com',
                                    username='test_username',
                                    password='test_password',
                                    restaurant=rest)
    
@pytest.mark.django_db
def test_user_with_restaurant(user_with_restaurant):
    assert user_with_restaurant.restaurant.title == 'Test_restaurant'

@pytest.mark.django_db
def test_user_restaurant_not_none(user_with_restaurant):
    assert user_with_restaurant.restaurant != None

@pytest.mark.django_db
def test_username(user_no_restaurant):
    assert user_no_restaurant.username == 'test_username'

@pytest.mark.django_db
def test_email(user_no_restaurant):
    assert user_no_restaurant.email == 'test@email.com'
    
@pytest.mark.django_db    
def test_is_active(user_no_restaurant):
    assert user_no_restaurant.is_active is True
    
@pytest.mark.django_db    
def test_is_not_active(user_no_restaurant):
    user_no_restaurant.is_active = False
    assert user_no_restaurant.is_active is False
    
@pytest.mark.django_db    
def test_password(user_no_restaurant):
    assert user_no_restaurant.check_password('test_password') is True
    
@pytest.mark.django_db    
def test_is_not_staff(user_no_restaurant):
    assert user_no_restaurant.is_staff is False
    
@pytest.mark.django_db    
def test_is_staff(user_no_restaurant):
    user_no_restaurant.is_staff = True
    assert user_no_restaurant.is_staff is True
    
@pytest.mark.django_db
def test_is_restaurant_null(user_no_restaurant):
    assert user_no_restaurant.restaurant == None