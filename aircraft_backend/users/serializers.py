from rest_framework import serializers
from .models import Personnel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class PersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Personnel
        fields = ['user', 'team_name']
