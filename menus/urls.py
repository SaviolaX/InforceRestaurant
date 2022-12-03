from django.urls import path

from .views import (MenuCreateView, MenuRetrieveView,
                    MenusListView, MenuUpdateView,
                    MenuDeleteView)

urlpatterns = [
    path('create/', MenuCreateView.as_view(), name='create_menu'),
    path('<str:pk>/', MenuRetrieveView.as_view(), name='get_menu'),
    path('', MenusListView.as_view(), name='list_menu'),
    path('<str:pk>/update/', MenuUpdateView.as_view(), name='update_menu'),
    path('<str:pk>/delete/', MenuDeleteView.as_view(), name='delete_menu'),
]