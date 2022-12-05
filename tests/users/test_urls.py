from django.urls import reverse, resolve

from users.urls import TokenObtainPairView, TokenRefreshView
from users.views import RegisterUserView, LogoutView


def test_login_url():
    assert resolve(reverse('login')).func.view_class == TokenObtainPairView


def test_login_refresh_url():
    assert resolve(
        reverse('login_refresh')).func.view_class == TokenRefreshView


def test_logout_url():
    assert resolve(reverse('logout')).func.view_class == LogoutView


def test_register_url():
    assert resolve(reverse('register')).func.view_class == RegisterUserView