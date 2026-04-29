from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertRuleViewSet

router = DefaultRouter()
router.register(r'alert-rules', AlertRuleViewSet, basename='alert-rule')

urlpatterns = [
    path('', include(router.urls)),
]
