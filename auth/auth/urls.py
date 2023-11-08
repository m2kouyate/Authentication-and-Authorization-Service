"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import TokenAuthentication
from authentication.views import UserProfileViewSet, UserRegistrationView, UserLoginView, UserLogoutView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Users API",
      default_version='v1',
      description="API for managing users",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dev@trophystays.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(TokenAuthentication,),
)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),

    # Include router urls
    path('api/', include(router.urls)),

    # Token auth endpoint
    path('api/token/', obtain_auth_token, name='api_token_auth'),

    # Registration, login, and logout endpoints
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/logout/', UserLogoutView.as_view(), name='logout'),

    # Swagger schema
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Static and media settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
