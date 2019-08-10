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
pd.set_option("display.max_columns", 11)
# %%


def CrearUsuario():
    nombre = input("\nIngrese el nombre de usuario\n") + "USR"
    os.makedirs(nombre)
    print("\nSe creo el usuario %s\n" % nombre[:-3])


def IniciarSesion():
    nombre = input("\nNombre de usuario\n") + "USR"
    if os.path.isdir(nombre):
        Dir = directorio + "\\" + "%s" % nombre
        os.chdir(Dir)
        print("\nInicio de sesion de %s\n" % nombre[:-3])
        Info()
    else:
        print("\nNo existe el usuario\n")


def CerrarSesion():
    os.chdir(directorio)


def Info():  # TODO solucionar el error que aparece al no haber cuentas o al
    # haber cuentas creadas sin datos dentro
    # asd
    # directorio sin extension
    # lista con los nombres de los archivos de cuenta
    lista = os.listdir()
    Lista = []
    for elem in lista:
        if "CUENTA.txt" in elem:
            Lista.append(elem)
    # lista con el saldo total de dinero de cada cuenta
    total = []
    for elem in Lista:
        total.append(pd.read_csv(elem, sep="\t").values[-1, 2])
    # lista con sólo el nombre de las cuentas
    lista_de_cuentas = []
    for elem in Lista:
        lista_de_cuentas.append(elem[:-10])
    # nombre de la cuenta con el saldo total
    informacion = ""
    for i in range(len(lista_de_cuentas)):
        informacion += "\n" + lista_de_cuentas[i] + ":" + "Saldo total $"\
            + str(total[i]) + "\n"
    print("Cuentas existentes:\n", informacion)
    str_funciones = "\nCrearUsuario()\nIniciarSesion()\nCerrarSesion()\n"\
        + "\nInfo()\nFecha()\nDatos_cuenta()\nCrear_cuenta()\n"\
        + "Eliminar_cuenta()\nIngresar_dinero()\nExtraer_dinero()\n"\
        + "Transferencia()\nGasto()\n"
    print("Funciones:\n", str_funciones)
    # return informacion


def Fecha():
    """
    simplemente genera la hora en formato argento
    """
    fecha_hora = datetime.now()
    fecha = str(fecha_hora)[:10]
    hora = str(fecha_hora)[11:19]
    fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")
    return fecha, hora


def Datos_cuenta():
    """
    los datos crudos de la cuenta
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    if os.path.isfile(nombre):
        datos = pd.read_csv(nombre, sep="\t")
        return datos
    else:
        print("\nNo existe la cuenta %s\n" % nombre[:-10])


def Crear_cuenta():
    """
    Crea un .txt cuyo nombre será el nombre de la cuenta
    """
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    nombre += "CUENTA.txt"
    Encabezados = ["Fecha", "hora", "Total", "Ingresos", "Extracciones",
                   "Gasto", "Categoria", "Subcategoria", "Descripcion",
                   "Balance"]
    fila = ""
    for elementos in Encabezados:
        fila += elementos + "\t"  # TODO: arreglar el tab al final
    fila += "\n"
    with open(nombre, "x") as micuenta:
        micuenta.write(fila)
    print("\nSe ha creado la cuenta %s\n" % nombre[:-10])


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
            print("\nSe eliminó la cuenta %s\n" % nombre[:-10])
        else:
            print("\nNo se eliminó la cuenta %s\n" % nombre[:-10])
    else:
        print("\nNo existe la cuenta %s\n" % nombre[:-10])


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
        categoria = input("\nCategoria: \n")
        subcategoria = input("\nSubcategoria: \n")
        descripcion = input("\nDescripcion: \n")
        extraccion = "0"  # esto siempre debería ser 0 al ingresar dinero
        gasto = "0"  # esto siempre debería ser 0 al ingresar dinero
        if len(datos) == 0:
            total = ingreso
        else:
            total = str(float(ingreso) + datos[-1, 2])
        balance = "0"  # TODO: ver si balance es necesario
        Campos = [fecha, hora, total, ingreso, extraccion,
                  gasto, categoria, subcategoria, descripcion,
                  balance]
        fila = ""
        for elementos in Campos:
            fila += elementos + "\t"  # TODO: Arreglar el tab al final
        fila += "\n"
        with open(nombre, "a") as micuenta:
            micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    print("\nDinero total en cuenta: $%.2f\n" % dinero_final)


def Extraer_dinero():
    """
    Extrae el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    # se fija si el archivo de la cuenta existe
    if os.path.isfile(nombre):
        # Abre y lee los datos de la cuenta
        contenido_cuenta = pd.read_csv(nombre, sep="\t")
        datos = contenido_cuenta.values
        fecha = Fecha()[0]
        hora = Fecha()[1]
        ingreso = "0"  # esto siempre debería ser 0 al extraer dinero
        gasto = "0"  # esto es 0 por definicion de extraccion =/= gasto
        if len(datos) == 0:
            print("\nAún no se ha ingresado dinero en la cuenta\n")
        else:
            extraccion = input("\nCantidad de dinero a extraer\n")
            if datos[-1, 2] < float(extraccion):
                print("\nNo hay dinero suficiente en la cuenta\n")
            else:
                categoria = input("\nCategoria: \n")
                subcategoria = input("\nSubcategoria: \n")
                descripcion = input("\nDescripcion: \n")
                total = str(datos[-1, 2] - float(extraccion))
                balance = "0"  # TODO: ver si balance es necesario
                Campos = [fecha, hora, total, ingreso, extraccion,
                          gasto, categoria, subcategoria, descripcion,
                          balance]
                fila = ""
                for elementos in Campos:
                    fila += elementos + "\t"  # TODO: Arreglar el tab al final
                fila += "\n"
                with open(nombre, "a") as micuenta:
                    micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    print("\nDinero total en cuenta: $%.2f\n" % dinero_final)


def Transferencia():
    """
    Funcion de transferencias
    """
    nombre_salida = input("\nIngrese la cuenta de salida\n") + "CUENTA.txt"
    nombre_entrada = input("\nIngrese la cuenta de entrada\n") + "CUENTA.txt"
    if os.path.isfile(nombre_salida) and os.path.isfile(nombre_entrada):
        # si las dos cuentas existen
        contenido_salida = pd.read_csv(nombre_salida, sep="\t")
        contenido_entrada = pd.read_csv(nombre_entrada, sep="\t")
        datos_salida = contenido_salida.values
        datos_entrada = contenido_entrada.values
        fecha = Fecha()[0]
        hora = Fecha()[1]
        if len(datos_salida) == 0:
            print("\nNo hay dinero en la cuenta %s\n" % nombre_salida[:-10])
        else:
            valor = input("\nCantidad de dinero a transferir\n")
            if datos_salida[-1, 2] < float(valor):
                print("\nNo hay dinero suficiente en la cuenta %s" 
                      % nombre_salida[:-10])
            categoria = "Transferencia"
            subcategoria_salida = "Transferencia de salida"
            descripcion_salida = "Transferencia a %s" % nombre_entrada[:-10]
            subcategoria_entrada = "Transferencia de entrada"
            descripcion_entrada = "Transferencia de %s" % nombre_salida[:-10]
            total_salida = str(datos_salida[-1, 2] - float(valor))
            total_entrada = str(datos_entrada[-1, 2] + float(valor))
            balance = gasto = extraccion = ingreso = "0"
            # TODO: ver si balance es necesario
            Campos_entrada = [fecha, hora, total_entrada, valor, extraccion,
                              gasto, categoria, subcategoria_entrada,
                              descripcion_entrada, balance]
            Campos_salida = [fecha, hora, total_salida, ingreso, valor,
                             gasto, categoria, subcategoria_salida,
                             descripcion_salida, balance]
            fila_entrada = ""
            fila_salida = ""
            for elementos in Campos_entrada:
                fila_entrada += elementos + "\t"  # TODO: Arreglar el tab al final
            fila_entrada += "\n"
            for elementos in Campos_salida:
                fila_salida += elementos + "\t"  # TODO: Arreglar el tab al final
            fila_salida += "\n"
            with open(nombre_entrada, "a") as micuenta:
                micuenta.write(fila_entrada)
            with open(nombre_salida, "a") as micuenta:
                micuenta.write(fila_salida)
    elif os.path.isfile(nombre_salida) and not os.path.isfile(nombre_entrada):
        # si no existe la cuenta entrada
        print("\nNo existe la cuenta '%s' de entrada\n" % nombre_entrada[:-10])
    elif not os.path.isfile(nombre_salida) and os.path.isfile(nombre_entrada):
        # si no existe la cuenta entrada
        print("\nNo existe la cuenta '%s' de salida\n" % nombre_salida[:-10])
    else:
        print("\nNo existen las cuentas '%s'" % nombre_salida[:-10],
              "ni la cuenta '%s'" % nombre_entrada[:-10])


def Gasto():
    """
    Genera un gasto en la cuenta indicada
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    if os.path.isfile(nombre):
        # Abre y lee los datos de la cuenta
        contenido_cuenta = pd.read_csv(nombre, sep="\t")
        datos = contenido_cuenta.values
        fecha = Fecha()[0]
        hora = Fecha()[1]
        ingreso = "0"  # esto siempre debería ser 0 al hacer un gasto
        extraccion = "0"  # esto siempre debería ser 0 al hacer un gasto
        if len(datos) == 0:
            print("\nNo hay dinero en la cuenta\n")
        else:
            valor = input("\nValor del gasto\n")
            if datos[-1, 2] < float(valor):
                print("\nNo hay dinero suficiente en la cuenta\n")
            else:
                categoria = input("\nCategoria: \n")
                subcategoria = input("\nSubategoria: \n")
                descripcion = input("\nDescripcion: \n")
                total = str(datos[-1, 2] - float(valor))
                balance = "0"  # TODO: ver si balance es necesario
                Campos = [fecha, hora, total, ingreso, extraccion,
                          valor, categoria, subcategoria, descripcion,
                          balance]
                fila = ""
                for elementos in Campos:
                    fila += elementos + "\t"  # TODO: Arreglar el tab al final
                fila += "\n"
                with open(nombre, "a") as micuenta:
                    micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    print("\nDinero total en cuenta: $%.2f\n" % dinero_final)
# %%


IniciarSesion()
