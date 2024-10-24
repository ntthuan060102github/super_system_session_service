from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Demo",
        default_version="latest",
        contact=openapi.Contact(email="ntthuan060102.work@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=()
)

urlpatterns = (
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
)