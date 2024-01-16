from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from tinyapp.serializers.tiny import TinySerializer
from tinyapp.models import ShortenedURLStore, User
from tinyapp.serializers.account import AccountSerializer,LoginSerializer


class TinyViewSet(viewsets.ModelViewSet):
    queryset = ShortenedURLStore.objects.all()
    http_method_names = [
        "post",
        "get",
    ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TinySerializer
        elif self.request.method == "GET":
            return TinySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "TinyUrl",
                "message": "Created successfully",
                "data": response.data,
            }
        )

    def list(self, request, *args, **kwargs):
        url = self.request.query_params.get("url")

        if not url:
            response = super().list(request, *args, **kwargs)
            return Response(
                {
                    "title": "Tiny",
                    "message": "Listed successfully",
                    "data": response.data,
                }
            )

        else:
            url = ShortenedURLStore.objects.filter(custom_url=url)
            if not url.exists():
                return Response(
                    {
                        "title": "Tiny",
                        "message": "TinyUrl Not found",
                    }
                )
            else:
                url = url.first()
                return Response(
                    {
                        "title": "Tiny",
                        "message": "Retrieved successfully",
                        "data": f"Original URL is: {url.original_url}",
                    }
                )
    
class AccountsCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Accounts",
                "message": "Accounts created successfully",
            }
        )

class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "email" in serializer.validated_data:
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
        elif "phone" in serializer.validated_data:
            user = User.objects.filter(phone=serializer.validated_data["phone"]).first()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response(
            {
                "title": "Login",
                "message": "Logged in successfully",
                "data": {
                    **AccountSerializer(instance=user).data,
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
            }
        )    
    