from rest_framework import routers

from django.urls import include
from django.urls import path

from api import views

router = routers.DefaultRouter()
router.register(r'restaurant', views.RestaurantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('restaurants/statistics/', views.restaurant_statics, name='restaurant-statistics'),
]
