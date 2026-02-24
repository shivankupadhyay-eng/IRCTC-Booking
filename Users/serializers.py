import django
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

user=get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email','password']
    
    def create(self, validated_data):
        user=CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        data['user']=user
        return data