
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, logout
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__email', 'phone_number']  # Поля модели UserProfile, по которым можно фильтровать
    search_fields = ['user__email', 'phone_number']  # Поля модели UserProfile, по которым можно осуществлять поиск
    ordering_fields = ['created_at', 'modified_at']  # Поля модели UserProfile, по которым можно осуществлять сортировку


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSerializer,  # Add this line to document the request body
        responses={
            200: openapi.Response(description="Login Successful"),
            400: openapi.Response(description="Invalid Credentials"),
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'You are not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)