
from rest_framework import viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, logout, login
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer, UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__email', 'phone_number']  # Поля модели UserProfile, по которым можно фильтровать
    search_fields = ['user__email', 'phone_number']  # Поля модели UserProfile, по которым можно осуществлять поиск
    ordering_fields = ['created_at', 'modified_at']  # Поля модели UserProfile, по которым можно осуществлять сортировку


class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            200: openapi.Response(description="Registration Successful"),
            400: openapi.Response(description="Invalid Credentials"),
        }
    )

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserProfileSerializer(user.profile).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response(description="Login Successful"),
            400: openapi.Response(description="Invalid Credentials"),
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(**serializer.validated_data)
            if user:
                login(request, user)
                Token.objects.filter(user=user).delete()  # Удаляем старый токен
                token = Token.objects.create(user=user)  # Создаем новый токен
                return Response({
                    'token': token.key,
                    'user': UserProfileSerializer(user.profile).data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()  # Удаляем токен
            logout(request)
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'You are not logged in'}, status=status.HTTP_403_FORBIDDEN)