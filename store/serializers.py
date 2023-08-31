from store.models import Box
from rest_framework import serializers
from django.contrib.auth import get_user_model

class AdminBoxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Box
        fields = "__all__"


class UserBoxSerializer(serializers.ModelSerializer):
    # Prevent exposing createdBy , createdOn , updatedOn
    class Meta:
        model = Box
        exclude = ["createdBy" ,"createdOn", "updatedOn"]
        


# Serializer for creating User
User = get_user_model()
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        
    def create(self, validated_data):
        user = User.objects.create_user(username = validated_data["username"], email = validated_data["email"], password = validated_data["password"])
        return user