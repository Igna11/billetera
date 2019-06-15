# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos
"""
import pandas as pd
from datetime import datetime
import os
directorio = r"C:\Users\igna\Desktop\Igna\Python Scripts\billetera"
os.chdir(directorio)
# %%


def Info():
    # lista con los nombres de los archivos de cuenta
    lista = os.listdir()
    for elem in lista:
        if "CUENTA.txt" not in elem:
            lista.remove(elem)
    # lista con el saldo total de dinero de cada cuenta
    total = []
    for elem in lista:
        total.append(pd.read_csv(elem, sep="\t").values[-1, 4])
    # lista con sólo el nombre de las cuentas
    lista_de_cuentas = []
    for elem in lista:
        lista_de_cuentas.append(elem[:-10])
    # nombre de la cuenta con el saldo total
    informacion = ""
    for i in range(len(lista_de_cuentas)):
        informacion += "\n" + lista_de_cuentas[i] + ":" + "Saldo total $"\
            + str(total[i]) + "\n"
    return informacion


def Fecha():
    """
    simplemente genera la hora en formato argento
    """
    fecha_hora = datetime.now()
    fecha = str(fecha_hora)[:10]
    hora = str(fecha_hora)[11:19]
    fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")
    return fecha, hora


def datos_cuenta():
    """
    los datos crudos de la cuenta
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    if os.path.isfile(nombre):
        datos = pd.read_csv(nombre, sep="\t")
        return datos
    else:
        print("\nNo existe la cuenta %s\n" % nombre[:-4])


def Crear_cuenta():
    """
    Crea un .txt cuyo nombre será el nombre de la cuenta
    """
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    nombre += "CUENTA.txt"
    Encabezados = ["Fecha", "hora", "Ingresos", "Extracciones", "Total",
                   "Balance"]
    fila = ""
    for elementos in Encabezados:
        fila += elementos + "\t"  # TODO: arreglar el tab al final
    fila += "\n"
    with open(nombre, "x") as micuenta:
        micuenta.write(fila)
    print("\nSe ha creado la cuenta %s\n" % nombre[:-4])


def Eliminar_cuenta():
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    if os.path.isfile(nombre):
        advertencia = "¿Seguro que queres eliminar la cuenta?\n\n\
        todos los datos contenidos en ella se perderán para siempre.\n\n\
        Ingrese '1', 'si' o 'y' para borrar\n\
        Ingrese cualquier otra cosa para cancelar\n"
        respuesta = input(advertencia)
        posibles_respuestas = ["1", "si", "y"]
        if respuesta in posibles_respuestas:
            os.remove(nombre)
            print("\nSe eliminó la cuenta %s\n" % nombre[:-4])
        else:
            print("\nNo se eliminó la cuenta %s\n" % nombre[:-4])
    else:
        print("\nNo existe la cuenta %s\n" % nombre[:-4])


def Ingresar_dinero():
    """
    Ingresa el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t")
    datos = contenido_cuenta.values
    if os.path.isfile(nombre):
        fecha = Fecha()[0]
        hora = Fecha()[1]
        ingreso = input("\nCantidad de dinero a ingresar\n")
        extraccion = "0"  # esto siempre debería ser 0 al ingresar dinero
        if len(datos) == 0:
            total = ingreso
        else:
            total = str(float(ingreso) + datos[-1, 4])
        balance = "0"  # TODO: ver si balance es necesario
        Campos = [fecha, hora, ingreso, extraccion, total, balance]
        fila = ""
        for elementos in Campos:
            fila += elementos + "\t"  # TODO: Arreglar el tab al final
        fila += "\n"
        with open(nombre, "a") as micuenta:
            micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 4]
    print("\nDinero total en cuenta: $%.2f\n" % dinero_final)


def Extraer_dinero():
    """
    Extrae el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    # se fija si el archivo existe
    if os.path.isfile(nombre):
        # Abre y lee los datos de la cuenta
        contenido_cuenta = pd.read_csv(nombre, sep="\t")
        datos = contenido_cuenta.values
        fecha = Fecha()[0]
        hora = Fecha()[1]
        ingreso = "0"  # esto siempre debería ser 0 al extraer dinero
        if len(datos) == 0:
            print("\nNo se ha ingresado dinero en la cuenta\n")
        else:
            extraccion = input("\nCantidad de dinero a extraer\n")
            if datos[-1, 4] < float(extraccion):
                print("\nNo hay dinero suficiente en la cuenta\n")
            else:
                total = str(datos[-1, 4] - float(extraccion))
                balance = "0"  # TODO: ver si balance es necesario
                Campos = [fecha, hora, ingreso, extraccion, total, balance]
                fila = ""
                for elementos in Campos:
                    fila += elementos + "\t"  # TODO: Arreglar el tab al final
                fila += "\n"
                with open(nombre, "a") as micuenta:
                    micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 4]
    print("\nDinero total en cuenta: $%.2f\n" % dinero_final)
# %%


print(Info())
