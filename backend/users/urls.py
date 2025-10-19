from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # User sends username/password, receives access & refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # User sends refresh token, receives new access token
    path('hello/', views.HelloUserView.as_view(), name='hello-user'), # Protected endpoint, requires valid JWT
    path('public/', views.PublicView.as_view(), name='public-endpoint'), # Public endpoint, no auth required
]