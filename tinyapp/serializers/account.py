from rest_framework import serializers, generics
from rest_framework.exceptions import ValidationError
from tinyapp.models import User
from common.utils import (
    validate_password,
)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "password",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }
        
    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("full_name") == "":
            raise ValidationError(
                {
                    "title": "Accounts",
                    "message": "FullName is required fields!",
                }
            )    
            
        if data.get("password") == "":
            raise ValidationError(
                {
                    "title": "Accounts",
                    "message": "Password is required fields!",
                }
            )
        if not validate_password(data.get("password")):
            raise ValidationError(
                {
                    "title": "Accounts",
                    "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character!",
                }
            )   
        if User.objects.filter(email=data.get("email")).exists():
            raise ValidationError(
                {
                    "title": "Accounts",
                    "message": "Email already linked with another user!",
                },
            ) 
        if User.objects.filter(email=data.get("full_name")).exists():
            raise ValidationError(
                {
                    "title": "Accounts",
                    "message": "User already exist!",
                },
            )  
        return super().is_valid(raise_exception=raise_exception)     

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        user = User.objects.get(email=data.get("email"))
        if data.get("email") == "":
            raise ValidationError(
                {
                    "title": "Login",
                    "message": "Email is required fields!",
                }
            )    
            
        if data.get("password") == "":
            raise ValidationError(
                {
                    "title": "Login",
                    "message": "Password is required fields!",
                }
            )
            
        if not User.objects.filter(email=data.get("email")).exists():
            raise ValidationError(
                {
                    "title": "Login",
                    "message": "Email does not exist!",
                },
            )    
        if not User.objects.filter(password = data.get("password")).exists():
            raise ValidationError(
                {
                    "title": "Login",
                    "message": "Incorrect password!",
                }
            )
            
                
        return super().is_valid(raise_exception=raise_exception)