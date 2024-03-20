from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Account, Transaction

User = get_user_model()


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_holder', 'account_balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'from_account', 'to_account', 'amount', 'description', 'status']


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'mobile', 'username']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)