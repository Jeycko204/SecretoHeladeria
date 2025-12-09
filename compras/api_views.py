from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from .models import Proveedor, OrdenCompra, DetalleOrden, Categoria, Insumo
from .serializers import ProveedorSerializer, OrdenCompraSerializer, CategoriaSerializer, InsumoSerializer
from .permissions import IsJefeComprasOrReadOnly, IsBodeguero, IsFinanzas

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

class InsumoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated, IsJefeComprasOrReadOnly]

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenCompraSerializer
    permission_classes = [IsAuthenticated, IsJefeComprasOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Transacción: Crea una Orden de Compra y sus Detalles en una sola operación atómica.
        """
        # Verificar permisos de creación (Solo Compras puede crear)
        if not (request.user.is_staff or request.user.groups.filter(name='COMPRAS').exists()):
             return Response({'error': 'No tiene permiso para crear órdenes.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        detalles_data = data.get('detalles', [])
        
        if not detalles_data:
            return Response({'error': 'La orden debe tener al menos un detalle.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Crear la Orden (Cabecera)
                orden = OrdenCompra.objects.create(
                    solicitante=request.user,
                    estado='PENDIENTE'
                )
                
                # 2. Crear los Detalles (Líneas)
                for detalle in detalles_data:
                    DetalleOrden.objects.create(
                        orden=orden,
                        proveedor_id=detalle.get('proveedor'), # ID del proveedor
                        insumo=detalle.get('insumo', 'Insumo API'), # Nombre texto
                        unidad_medida=detalle.get('unidad_medida', 'UN'),
                        cantidad=detalle.get('cantidad'),
                        precio_unitario=detalle.get('precio_unitario')
                    )
                
                # 3. Actualizar totales
                orden.update_totals()
                
                # Serializar respuesta
                serializer = self.get_serializer(orden)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({'error': f'Error en la transacción: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    def get_serializer_class(self):
        return OrdenCompraSerializer

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def aprobar(self, request, pk=None):
        orden = self.get_object()
        if request.method == 'GET':
            return Response({'status': f'Orden {orden.id} está {orden.estado}. Realice un POST para aprobar.'})

        if not request.user.groups.filter(name='FINANZAS').exists() and not request.user.is_staff:
            return Response({'error': 'Solo Finanzas puede aprobar órdenes.'}, status=status.HTTP_403_FORBIDDEN)
        
        if orden.estado != 'PENDIENTE':
            return Response({'error': 'Solo se pueden aprobar órdenes pendientes.'}, status=status.HTTP_400_BAD_REQUEST)
            
        orden.estado = 'APROBADA'
        orden.save()
        return Response({'status': 'Orden aprobada'})

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def rechazar(self, request, pk=None):
        orden = self.get_object()
        if request.method == 'GET':
            return Response({'status': f'Orden {orden.id} está {orden.estado}. Realice un POST para rechazar.'})

        if not request.user.groups.filter(name='FINANZAS').exists() and not request.user.is_staff:
            return Response({'error': 'Solo Finanzas puede rechazar órdenes.'}, status=status.HTTP_403_FORBIDDEN)
            
        if orden.estado != 'PENDIENTE':
            return Response({'error': 'Solo se pueden rechazar órdenes pendientes.'}, status=status.HTTP_400_BAD_REQUEST)
            
        orden.estado = 'RECHAZADA'
        orden.save()
        return Response({'status': 'Orden rechazada'})

    @action(detail=True, methods=['post', 'get'], permission_classes=[IsAuthenticated])
    def cerrar(self, request, pk=None):
        orden = self.get_object()
        if request.method == 'GET':
            return Response({'status': f'Orden {orden.id} está {orden.estado}. Realice un POST para cerrar.'})

        if not request.user.groups.filter(name='BODEGA').exists() and not request.user.is_staff:
            return Response({'error': 'Solo Bodega puede cerrar órdenes.'}, status=status.HTTP_403_FORBIDDEN)
            
        if orden.estado != 'APROBADA':
            return Response({'error': 'Solo se pueden cerrar órdenes aprobadas.'}, status=status.HTTP_400_BAD_REQUEST)
            
        orden.estado = 'CERRADA'
        orden.save()
        return Response({'status': 'Orden cerrada'})
