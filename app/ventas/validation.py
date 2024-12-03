from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal

def validate_venta(venta):
    """
    Validations for Venta (Sale) model
    """
    # Ensure the sale has at least one detail
    if venta.detalles.count() == 0:
        raise ValidationError("La venta debe tener al menos un detalle de producto.")

    # Validate total matches calculated total
    calculated_total = sum(detalle.subtotal for detalle in venta.detalles.all())
    if venta.total != calculated_total:
        raise ValidationError(f"El total de la venta (${venta.total}) no coincide con el subtotal calculado (${calculated_total}).")

def validate_pago(pago):
    """
    Validations for Pago (Payment) model
    """
    venta_total = pago.venta.total

    # Allow overpayment only for cash payments
    if pago.metodo_pago == 'EF':  # Efectivo (Cash)
        # Cash payments can be higher to provide change
        if pago.monto < venta_total:
            raise ValidationError("El pago en efectivo debe ser mayor o igual al total de la venta.")
    else:
        # For other payment methods, payment must match sale total exactly
        if pago.monto != venta_total:
            raise ValidationError(f"El monto del pago (${pago.monto}) debe ser exactamente igual al total de la venta (${venta_total}).")

    # Check partial payment logic for non-cash payments
    if not pago.es_pago_parcial and pago.monto < venta_total:
        raise ValidationError("El pago no está marcado como parcial pero no cubre el total de la venta.")
def validate_detalle_venta(detalle):
    """
    Validations for DetalleVenta (Sale Detail) model
    """
    # Validate quantity against product stock
    if detalle.producto and detalle.cantidad > detalle.producto.stock:
        raise ValidationError(f"Cantidad ({detalle.cantidad}) supera el stock disponible del producto ({detalle.producto.stock}).")

    # Validate positive quantities and prices
    if detalle.cantidad <= 0:
        raise ValidationError("La cantidad debe ser un número positivo mayor que cero.")

    if detalle.precio_unitario <= 0:
        raise ValidationError("El precio unitario debe ser un número positivo mayor que cero.")

    # Validate subtotal calculation
    calculated_subtotal = Decimal(detalle.cantidad) * Decimal(detalle.precio_unitario)
    if abs(detalle.subtotal - calculated_subtotal) > Decimal('0.01'):
        raise ValidationError(f"El subtotal calculado (${calculated_subtotal}) no coincide con el subtotal registrado (${detalle.subtotal}).")