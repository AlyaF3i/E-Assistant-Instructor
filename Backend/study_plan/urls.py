from django.contrib import admin  # Import the admin module
from django.urls import path, include
from django.shortcuts import render
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define a view to serve the index.html template
def index(request):
    return render(request, 'images/index.html')  # Render the home page template

# Swagger and Redoc setup
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for my project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# URL patterns
urlpatterns = [
    path('', index),  # Route the root URL to the index view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('classroom.urls')),  # Include URLs from your classroom app
    path('admin/', admin.site.urls),  # Add this line to include the admin interface
]
