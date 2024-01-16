from django.urls import path, include

from rest_framework.routers import DefaultRouter
from tinyapp.views import TinyViewSet,AccountsCreateView,LoginView

router = DefaultRouter()
router.register("Tinyurl", TinyViewSet, basename="demand")


urlpatterns = [
    path("", include(router.urls)),
    path("registration/", AccountsCreateView.as_view()),
    path("login/", LoginView.as_view()),


]
