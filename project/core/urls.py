"""project URL Configuration
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework.schemas import get_schema_view


schema_url_patterns = [
    path('api/v1/', include('api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url': 'openapi-schema'},
    ), name="docs"),
    path('openapi/', get_schema_view(
        title="Test Task Project",
        description="API",
        version="1.0.0",
        patterns=schema_url_patterns,
    ), name='openapi-schema'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include('api.urls')),
]
