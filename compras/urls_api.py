from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProveedorViewSet, OrdenCompraViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'ordenes', OrdenCompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
