# urls.py
from django.urls import path
from .views import PartAPIView, PartDetailAPIView, AssemblyAPIView

urlpatterns = [
    path('', PartAPIView.as_view(), name='part-list-create'),
    path('assembly/', AssemblyAPIView.as_view(), name='assembly'),
    path('<int:pk>/', PartDetailAPIView.as_view(), name='part-detail'),
]
