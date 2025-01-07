# urls.py
from django.urls import path
from .views import PartAPIView, PartDetailAPIView

urlpatterns = [
    path('', PartAPIView.as_view(), name='part-list-create'),
    path('<int:pk>/', PartDetailAPIView.as_view(), name='part-detail'),
]
