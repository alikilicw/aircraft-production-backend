from django.urls import path
from .views import AircraftAPIView, AircraftDetailAPIView, AircraftModelAPIView

urlpatterns = [
    path('', AircraftAPIView.as_view(), name='aircraft'),
    path('aircraft-models/', AircraftModelAPIView.as_view(), name='aircraft-models'),
    path('<int:pk>/complete-production/', AircraftDetailAPIView.as_view(), name='complete-production')
]