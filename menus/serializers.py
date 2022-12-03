from rest_framework.serializers import ModelSerializer

from .models import Menu


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'title', 'file', 'restaurant', 'created_at')
        extra_kwargs = {
            'created_at': {'read_only': True},
        }