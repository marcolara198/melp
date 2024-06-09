from rest_framework import serializers

from api.models import Restaurant


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'rating', 'name', 'site', 'email', 'phone', 'street', 'city', 'state', 'lat', 'lng']


class RestaurantStatisticsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=9, decimal_places=2)
    std = serializers.DecimalField(max_digits=9, decimal_places=2)
