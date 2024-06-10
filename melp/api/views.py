from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Avg
from django.db.models import StdDev
from rest_framework import views
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from api.models import Restaurant
from api.serializers import RestaurantSerializer
from api.serializers import RestaurantStatisticsSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'site', 'email', 'phone', 'street', 'city', 'state']


class RestaurantStatisticsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        radius = request.query_params.get('radius')
        if not latitude or not longitude or not radius:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        latitude = float(request.query_params.get('latitude', 0))
        longitude = float(request.query_params.get('longitude', 0))
        radius = float(request.query_params.get('radius', 0))

        user_location = Point(latitude, longitude, srid=4326)

        nearby_restaurants = Restaurant.objects.annotate(distance=Distance('location', user_location)).filter(
            location__distance_lte=(user_location, D(m=radius))
        )

        results = nearby_restaurants.aggregate(Avg('rating'), StdDev('rating'))
        count = nearby_restaurants.count()
        avg = results['rating__avg']
        std = results['rating__stddev']

        serializer = RestaurantStatisticsSerializer({'count': count, 'avg': avg, 'std': std})
        return Response(serializer.data)


restaurant_statics = RestaurantStatisticsView.as_view()
