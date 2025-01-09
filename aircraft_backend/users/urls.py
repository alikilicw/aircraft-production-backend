from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import WhoAmIView, LogoutView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('whoami/', WhoAmIView.as_view(), name='whoami'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
