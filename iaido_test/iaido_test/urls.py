from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from iaido.views import PersonViewSet, LoginView

router = DefaultRouter()
router.register(r'persons', PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('api-token-auth/', views.obtain_auth_token),
]
