from django.urls import path

from .views import (RestaurantCreateView, RestaurantRetrieveView,
                    RestaurantsListView, RestaurantUpdateView,
                    RestaurantDeleteView)

urlpatterns = [
    path('create/', RestaurantCreateView.as_view(), name='create_rest'),
    path('<str:pk>/', RestaurantRetrieveView.as_view(), name='get_rest'),
    path('', RestaurantsListView.as_view(), name='list_rest'),
    path('<str:pk>/update/', RestaurantUpdateView.as_view(), name='update_rest'),
    path('<str:pk>/delete/', RestaurantDeleteView.as_view(), name='delete_rest'),
]