"""
User Views - API Layer.

Receives the HTTP request, delegates to the service layer,
and returns the HTTP response. No business logic here.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from core.exceptions import ServiceException
from .serializers import RegisterSerializer, UserProfileSerializer
from .services import UserService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
            request=RegisterSerializer, 
            responses={201: UserProfileSerializer},
            summary="Register a new user",
            tags=["Auth"],
        )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService.regiter(**serializer.validated_data)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        
        return Response(
            UserProfileSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
            responses={200: UserProfileSerializer},
            summary="Get authenticated user's profile",
            tags=["Users"],
        )
    def get(self, request):
        try:
            user = UserService.get_profile(request.user)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        
        return Response(UserProfileSerializer(user).data)
    

# JWT Views re-exported with Swagger tags
class LoginView(TokenObtainPairView):
    @extend_schema(
        Summary="Login - obtain JWT tokens", 
        tags=["Auth"]
    )
    def get(self, request):
        try:
            user = UserService.get_profile(request.user)
        except ServiceException as e:
            return Response({"detail": e.message}, status=e.status_code)
        
        return Response(UserProfileSerializer(user).data)
    

class RefreshTokenView(TokenRefreshView):
    @extend_schema(
        summary="Refresh access token", 
        tags=["Auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

