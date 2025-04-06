from rest_framework import serializers
from .models import UserModel
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel # specifying the model for use
        # fields to be serialized
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password']

# serializers for registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel # specifying the model for use
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password']

    # method to create new user
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password'],
        )
        return user
    
# serializers for login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username = data['username'],
            password = data['password']
        )
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        return {'user': user}
