from django.conf.urls.static import static
from rest_framework import routers

from website import settings
from django.contrib import admin
from django.urls import path, include, re_path
from debate.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('debate.urls')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/debate/', DebateAPIList.as_view()),
    path('api/v1/debate/<int:pk>/', DebateAPIUpdate.as_view()),
    path('api/v1/debatedelete/<int:pk>/', DebateAPIDestroy.as_view()),
    path('api/v1/auth/', include('djoser.urls')),  # new
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # new
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
