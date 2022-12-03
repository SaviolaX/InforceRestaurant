from django.urls import reverse, resolve

from menus.views import (MenuCreateView, MenuDeleteView,
                               MenuRetrieveView, MenusListView,
                               MenuUpdateView)

def test_create_url():
    assert resolve(reverse('create_menu')).func.view_class == MenuCreateView
    
def test_update_url():
    assert resolve(reverse('update_menu', kwargs={'pk': 1})).func.view_class == MenuUpdateView
    
def test_delete_url():
    assert resolve(reverse('delete_menu', kwargs={'pk': 1})).func.view_class == MenuDeleteView
    
def test_get_url():
    assert resolve(reverse('get_menu', kwargs={'pk': 1})).func.view_class == MenuRetrieveView
    
def test_list_url():
    assert resolve(reverse('list_menu')).func.view_class == MenusListView
    