from app.models import AppUser, Category

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(max_length=255)
    class Meta:
        model = AppUser
        fields = ['user_id', 'first_name', 'last_name', 'middle_name', 'email', 'account_balance']