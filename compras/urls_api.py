from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ProveedorViewSet, OrdenCompraViewSet, CategoriaViewSet, InsumoViewSet

router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet)
router.register(r'ordenes', OrdenCompraViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'insumos', InsumoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
