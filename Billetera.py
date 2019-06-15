# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos
"""
import numpy as np
from datetime import datetime
import os
directorio = r"C:\Users\igna\Desktop\Igna\Python Scripts\billetera"
os.chdir(directorio)
# %%
# cuenta:


def Fecha():
    """
    simplemente genera la hora en formato argento
    """
    fecha_hora = datetime.now()
    fecha = str(fecha_hora)[:10]
    hora = str(fecha_hora)[10:19]
    fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")
    return fecha, hora


def Crear_cuenta():
    """
    Crea un .txt cuyo nombre será el nombre de la cuenta
    """
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    nombre += ".txt"
    Encabezados = ["Fecha", "hora", "Total", "Ingresos", "Gastos", "Balance"]
    fila = ""
    for elementos in Encabezados:
        fila += elementos + "\t"
    fila += "\n"
    with open(nombre, "x") as micuenta:
        micuenta.write(fila)


def Ingresar_dinero():
    """
    Ingresa el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += ".txt"
    # Abre y lee los datos de la cuenta
    with open(nombre, "r") as cuenta:
        contenido = cuenta.read()
    if os.path.isfile(nombre):
        ingreso = input("\nCantidad de dinero a ingresar\n")
        fecha = Fecha()[0]
        hora = Fecha()[1]
        total = ingreso
        gasto = "0"  # esto siempre debería ser 0 al ingresar dinero
        balance = str(float(ingreso) - float(gasto))
        Campos = [fecha, hora, total, ingreso, gasto, balance]
        fila = ""
        for elementos in Campos:
            fila += elementos + "\t"
        fila += "\n"
        with open(nombre, "a") as micuenta:
            micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")