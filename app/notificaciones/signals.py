from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from .models import Producto
from app.notificaciones.models import Notificacion
from django.contrib.auth.models import User

@receiver(post_save, sender=Producto)
def crear_notificacion_stock(sender, instance, **kwargs):
    """
    Crea notificaciones automáticas basadas en el stock del producto y la fecha de vencimiento.
    """
    # Determina el usuario (esto puede variar según tu sistema)
    try:
        usuario = instance.autor  # O ajusta según el campo que identifica al responsable
    except AttributeError:
        usuario = User.objects.filter(is_superuser=True).first()  # Por defecto el superusuario
    
    # Notificación por stock
    if instance.stock <= 0:
        tipo_notificacion = 'sin_stock'
        titulo = f"Producto sin stock: {instance.nombre}"
        descripcion = f"El producto {instance.nombre} se quedó sin stock. Se recomienda realizar un nuevo pedido a los proveedores o revisar los pedidos pendientes."
    elif instance.stock <= instance.stock_critico:
        tipo_notificacion = 'stock_critico'
        descripcion = f"El producto {instance.nombre} alcanzó el nivel de stock crítico ({instance.stock}). Se recomienda reabastecer el stock lo antes posible para evitar faltantes en la venta."
        titulo = f"Producto en stock crítico: {instance.nombre}"
    elif instance.stock <= instance.stock_minimo:
        tipo_notificacion = 'stock_minimo'
        descripcion = f"El producto {instance.nombre} se encuentra en su nivel de stock mínimo ({instance.stock}). Es recomendable hacer un pedido de reposición antes de que se agote."
        titulo = f"Producto en stock mínimo: {instance.nombre}"
    else:
        tipo_notificacion = None
        titulo = None
        descripcion = None
    
    # Si el producto está cerca de la fecha de vencimiento (7 días antes)
    if instance.fecha_vencimiento - timezone.now().date() <= timedelta(days=7) and instance.is_active:
        tipo_notificacion = 'fecha_vencimiento'
        titulo = f"Producto cerca de la fecha de vencimiento: {instance.nombre}"
        descripcion = f"El producto {instance.nombre} está cerca de su fecha de vencimiento. Fecha de vencimiento: {instance.fecha_vencimiento}."
    
    # Si el producto ya está vencido
    if instance.fecha_vencimiento < timezone.now().date() and instance.is_active:
        tipo_notificacion = 'producto_vencido'
        titulo = f"Producto vencido: {instance.nombre}"
        descripcion = f"El producto {instance.nombre} ha vencido. Fecha de vencimiento: {instance.fecha_vencimiento}."
        # Desactivar el producto
        instance.is_active = False
        instance.save()

    # Crear notificación si corresponde
    if tipo_notificacion:
        Notificacion.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            tipo=tipo_notificacion,
            usuario=usuario,
            producto=instance
        )