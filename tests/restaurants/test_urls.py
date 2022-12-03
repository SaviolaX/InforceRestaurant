# from django.urls import reverse, resolve

# from restaurants.views import (RestaurantCreateView, RestaurantDeleteView,
#                                RestaurantRetrieveView, RestaurantsListView,
#                                RestaurantUpdateView)

# def test_create_url():
#     assert resolve(reverse('create_rest')).func.view_class == RestaurantCreateView
    
# def test_update_url():
#     assert resolve(reverse('update_rest', kwargs={'pk': 1})).func.view_class == RestaurantUpdateView
    
# def test_delete_url():
#     assert resolve(reverse('delete_rest', kwargs={'pk': 1})).func.view_class == RestaurantDeleteView
    
# def test_get_url():
#     assert resolve(reverse('get_rest', kwargs={'pk': 1})).func.view_class == RestaurantRetrieveView
    
# def test_list_url():
#     assert resolve(reverse('list_rest')).func.view_class == RestaurantsListView
    