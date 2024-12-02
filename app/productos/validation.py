import re
from django.core.exceptions import ValidationError
from datetime import date

# Método para generar el nombre estandarizado
def validar_nombre_general(nombre, tipo=""):
    # Validar que el nombre no esté vacío o solo contenga espacios
    if not nombre or nombre.strip() == "":
        raise ValidationError(f'El nombre de {tipo} no puede estar vacío.')
    
    # Validar que el nombre siga el formato: primera palabra solo letras, luego puede haber números
    if not re.match(r'^[A-Za-z]+(\s[A-Za-z0-9]+)*$', nombre.strip()):
        raise ValidationError(f'El nombre de {tipo} debe comenzar con letras y luego permite letras y números.')
    
    # Validar que el nombre tenga una longitud mínima (por ejemplo, 3 caracteres)
    if len(nombre.strip()) < 3:
        raise ValidationError(f'El nombre de {tipo} debe tener al menos 3 caracteres.')

def generar_nombre_producto(categoria, marca, nombre, descripcion, codigo_barra):
    # Verificar si categoria y marca existen y asignar un valor por defecto si no
    categoria_nombre = categoria.nombre if categoria else "Desconocida"
    marca_nombre = marca.nombre if marca else "Desconocida"
    
    # Crear el nombre del producto
    nombre_producto = f"{categoria_nombre} - {marca_nombre} - {nombre}"

    # Si tiene descripción, la añadimos
    if descripcion:
        nombre_producto += f" - {descripcion}"

    # Añadir código de barra al final
    nombre_producto += f" - {codigo_barra}"

    # Recortar el nombre si supera los 150 caracteres
    if len(nombre_producto) > 150:
        nombre_producto = nombre_producto[:150]

    return nombre_producto



### Funciones para EAN8 Y EAN13 ###
def calcular_digito_verificacion(codigo):
    pesos = [1, 3] if len(codigo) == 13 else [3, 1]
    suma = sum(int(d) * pesos[i % 2] for i, d in enumerate(codigo[:-1]))
    digito_verificador = (10 - suma % 10) % 10
    return digito_verificador

# Función para validar el código de barras
def validar_codigo_barra(value):
    # Verificar que el código de barras tenga 8 o 13 dígitos y que sean números
    if len(value) not in [8, 13] or not value.isdigit():
        raise ValidationError("El código de barras debe tener 8 o 13 dígitos numéricos.")
    
    # Verificar que el dígito verificador sea correcto
    if int(value[-1]) != calcular_digito_verificacion(value):
        raise ValidationError("El código de barras no tiene un dígito de verificación válido.")


# Validación de las fechas
def validar_fechas(fecha_elaboracion, fecha_vencimiento):
    if fecha_elaboracion > date.today():
        raise ValidationError('La fecha de elaboración no puede ser en el futuro.')

    # No permitir fechas de elaboración más antiguas que 10 años
    if fecha_elaboracion < date.today().replace(year=date.today().year - 3):
        raise ValidationError('La fecha de elaboración no puede ser más antigua que 3 años.')

    # Validación de la fecha de vencimiento
    if fecha_vencimiento < fecha_elaboracion:
        raise ValidationError('La fecha de vencimiento no puede ser anterior a la fecha de elaboración.')

    # No permitir fechas de vencimiento demasiado lejanas (por ejemplo más de 10 años)
    if fecha_vencimiento > fecha_elaboracion.replace(year=fecha_elaboracion.year + 10):
        raise ValidationError('La fecha de vencimiento no puede ser más de 10 años después de la fecha de elaboración.')


def validar_stock(stock, stock_minimo, stock_maximo, stock_critico):
    # 1. El stock mínimo no puede ser mayor que el stock máximo
    if stock_minimo > stock_maximo:
        raise ValidationError('El stock mínimo no puede ser mayor que el stock máximo.')

    # 2. El stock no puede ser inferior al stock mínimo
    if stock < stock_minimo:
        raise ValidationError(f"El stock debe ser al menos {stock_minimo} unidades.")

    # 3. El stock no puede ser superior al stock máximo
    if stock > stock_maximo:
        raise ValidationError(f"El stock no puede exceder las {stock_maximo} unidades.")

    # 4. El stock crítico no puede ser mayor que el stock máximo
    if stock_critico > stock_maximo:
        raise ValidationError('El stock crítico no puede ser mayor que el stock máximo.')

    # 5. El stock crítico debe ser menor que el stock mínimo (opcional)
    if stock_critico >= stock_minimo:
        raise ValidationError('El stock crítico debe ser menor que el stock mínimo.')