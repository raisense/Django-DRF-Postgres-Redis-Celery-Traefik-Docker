"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.schemas import get_schema_view

from app.api.shared.permissions import IsSuperUser
from app.api.shared.schemas import CustomOpenApiGenerator
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/v1/openapi/',
        get_schema_view(
            generator_class=CustomOpenApiGenerator,
            title='App REST API',
            description='App REST API',
            version='0.0.7',
            urlconf='app.api.urls.v1',
            permission_classes=[IsSuperUser],
            authentication_classes=[BasicAuthentication, SessionAuthentication],
            url='/api/v1/',
        ),
        name='openapi-schema-v1'
    ),
    path('api/v1/docs/', TemplateView.as_view(
        template_name='docs/redoc.html',
        extra_context={'schema_url': 'openapi-schema-v1'}
    ), name='docs-v1')

]

urlpatterns += i18n_patterns(
    path('api/v1/', include(('app.api.urls.v1', 'api'), namespace='v1')), prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
