from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, DestroyAPIView,
                                     ListAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantDeleteView(DestroyAPIView):
    """Delete a single restaurant object"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'


class RestaurantUpdateView(UpdateAPIView):
    """Update a single restaurant object"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'


class RestaurantRetrieveView(RetrieveAPIView):
    """Retrieve a single restaurant object"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'


class RestaurantCreateView(CreateAPIView):
    """Create a new restaurant object"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser, )


class RestaurantsListView(ListAPIView):
    """Retrieve a list of all restaurants"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminUser, )