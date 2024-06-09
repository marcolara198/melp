import statistics
from geopy import distance
from django_filters.rest_framework import DjangoFilterBackend
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

        restaurants = Restaurant.objects.all()

        count = 0
        avg = 0
        rating_added = 0
        dict_rating = []
        std = 0
        for restaurant in restaurants:
            if radius >= distance.distance((latitude, longitude), (restaurant.lat, restaurant.lng)).m:
                rating_added += restaurant.rating
                dict_rating.append(restaurant.rating)
                count += 1

        avg = rating_added / count
        std = statistics.stdev(dict_rating)
        print(count, avg, rating_added, dict_rating, std)

        serializer = RestaurantStatisticsSerializer({'count': count, 'avg': avg, 'std': std})
        return Response(serializer.data)


restaurant_statics = RestaurantStatisticsView.as_view()
