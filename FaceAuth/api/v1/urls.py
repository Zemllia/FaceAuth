from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from FaceAuth.api.v1 import views

router = routers.SimpleRouter()
schema_view = get_schema_view(
    openapi.Info(
        title="programmers_competition_server",
        default_version='base',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = router.urls + [
    path(
        'documentation/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path('check-image/', views.CheckImageView.as_view(), name='check_image'),
    path('get-my-name/', views.GetCameraName.as_view(), name='get_my_name'),
]