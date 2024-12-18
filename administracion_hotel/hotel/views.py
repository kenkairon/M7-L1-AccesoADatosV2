from django.shortcuts import render
from django.db import connection
from .models import Cliente, Habitacion

# Consultas directa a Base de Datos 
"""def habitacion_disponible_base_datos(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hotel_habitacion WHERE disponible = TRUE")
        rows = cursor.fetchall()

    return render(request, 'habitaciones_db.html', {'habitaciones': rows}) """

"""

"""
def habitacion_disponible_base_datos(request):
    # Ejecutar consulta SQL directa
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hotel_habitacion WHERE disponible = TRUE")
        columnas = [col[0] for col in cursor.description]  # Obtener nombres de columnas
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]  # Convertir filas a diccionarios

        # Renderizar la plantilla con los datos
        return render(request, 'habitaciones_db.html', {'habitaciones': filas})


def lista_clientes_base_datos(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hotel_cliente ORDER BY fecha_ingreso DESC")
        columnas = [col[0] for col in cursor.description]  # Obtener nombres de columnas
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]  # Convertir filas a diccionarios

        # Renderizar la plantilla con los datos
        return render(request, 'clientes_db.html', {'clientes': filas})

# Consultas indirecta mediante el modelo a la Base de Datos 
def habitacion_disponible(request):
    habitaciones = Habitacion.objects.raw('SELECT * FROM hotel_habitacion WHERE disponible = TRUE')
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

def lista_clientes(request):
    clientes = Cliente.objects.raw('SELECT * FROM hotel_cliente ORDER BY fecha_ingreso DESC')
    return render(request, 'clientes.html', {'clientes': clientes})