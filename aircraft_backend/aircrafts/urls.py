from django.urls import path
from .views import AircraftAPIView, AircraftDetailAPIView

urlpatterns = [
    path('', AircraftAPIView.as_view(), name='aircraft'),
    path('<int:pk>/complete-production/', AircraftDetailAPIView.as_view(), name='complete-production')
]