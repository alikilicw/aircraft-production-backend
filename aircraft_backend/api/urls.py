from django.urls import path, include

urlpatterns = [
    path('users/', include('api.personel.urls')),
    path('teams/', include('api.team.urls')),
]