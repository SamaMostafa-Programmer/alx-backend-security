from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

schema_view = get_schema_view(
   openapi.Info(
      title="IP Tracking API",
      default_version='v1',
      description="API documentation for security and IP tracking",
   ),
   public=True, # هذا السطر ضروري ليكون الوصول عاماً
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ... روابطك الحالية ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
