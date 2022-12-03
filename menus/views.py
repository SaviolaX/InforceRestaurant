from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, DestroyAPIView,
                                     ListAPIView)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Menu
from .serializers import MenuSerializer


class MenuDeleteView(DestroyAPIView):
    """Delete a single menu object"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'


class MenuUpdateView(UpdateAPIView):
    """Update a single menu object"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminUser, )
    lookup_field = 'pk'


class MenuRetrieveView(RetrieveAPIView):
    """Retrieve a single menu object"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'


class MenuCreateView(CreateAPIView):
    """Create a new menu object"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminUser, )


class MenusListView(ListAPIView):
    """Retrieve a list of all menus"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated, )
