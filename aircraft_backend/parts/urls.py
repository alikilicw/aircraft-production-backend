from django.urls import path
from .views import PartAPIView, PartDetailAPIView, AssemblyAPIView, PartModelAPIView

from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', PartAPIView.as_view(), name='part-list-create'),
    path('part-models/', PartModelAPIView.as_view(), name='part-model-list'),
    path('assembly/', AssemblyAPIView.as_view(), name='assembly'),
    path('<int:pk>/', PartDetailAPIView.as_view(), name='part-detail'),
]
