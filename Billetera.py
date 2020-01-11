# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos
"""
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt  # agregado 30-08-2019
directorio = r"C:\Users\igna\Desktop\Igna\Python Scripts\billetera"
os.chdir(directorio)
pd.set_option("display.max_columns", 11)
# %%
"""
Cosas que quisiera ir agregándole al script:


#TODO    Diferentes tipos de cuentas:
        Cuentas comunes con dinero gastable y cuentas especiales con dinero
        solo para ahorrar. Ejemplo: Quisiera que las cuentas en dólares sean
        solo cuentas para ahorrar y que se sumen o no (como opcion) al saldo
        total.
        También un scraper del precio del dolar para transformar esos valores
        a pesos.
        Usar el mismo scraper para tener un control de devaluación de ahorro.

#TODO    Editor de entradas:
        Alguna manera para editar un gasto, un ingreso, o algo que fue mal
        ingresado (puede que haga falta usar archivos temporales y librerias
        afines)

#TODO    Graficos:
        Alguna forma fácil de ver gastos/ingresos/whatever por día, por semana
        por mes, por año. (acá quizás podría estar el balance)

#TODO    Interfaz Gráfica y ejectuable:
        nada, eso, a futuro (lejano)
"""


def CrearUsuario():  # creada 10-02-2019
    nombre = input("\nIngrese el nombre de usuario\n") + "USR"
    if os.path.isdir(nombre):  # 10/01/2020 msj al intentar crear usr existente
        print("\nYa existe el usuario\n")
    else:
        os.makedirs(nombre)
        print("\nSe creo el usuario %s\n" % nombre[:-3])


def IniciarSesion():  # creada 10-02-2019
    nombre = input("\nNombre de usuario\n") + "USR"
    if os.path.isdir(nombre):
        Dir = directorio + "\\" + "%s" % nombre
        os.chdir(Dir)
        print("\nInicio de sesion de %s\n" % nombre[:-3])
        Info()
    else:
        print("\nNo existe el usuario\n")


def CerrarSesion():  # creada 10-02-2019
    os.chdir(directorio)


def EliminarUsuario():  # TODO solucion el PermissionError 10/01/2020
    nombre = input("\nIngrese el nombre de usuario a borrar\n") + "USR"
    if os.path.isdir(nombre):
        advertencia = "¿Seguro que queres eliminar el usuario?\n\n\
        todos los datos contenidos en ella se perderán para siempre.\n\n\
        Ingrese '1', 'si' o 'y' para borrar\n\
        Ingrese cualquier otra cosa para cancelar\n"
        respuesta = input(advertencia)
        posibles_respuestas = ["1", "si", "y"]
        if respuesta in posibles_respuestas:
            os.remove(nombre)
            print("\nSe eliminó el usuario %s\n" % nombre[:-10])
        else:
            print("\nNo se eliminó el usuario %s\n" % nombre[:-10])
    else:
        print("\nNo existe el usuario\n")


def Info():  # Creada 15-06-2019
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
            + str("%.2f" % total[i]) + "\n"
    total = Total()
    str_funciones = "\nCrearUsuario()\nIniciarSesion()\nCerrarSesion()\n"\
        + "\nInfo()\nTotal()\nFecha()\nDatos_cuenta()\nCrear_cuenta()\n"\
        + "Eliminar_cuenta()\nIngreso()\nExtraccion()\n"\
        + "Transferencia()\nGasto()\nBalance()<---NO USAR-Ver help(Balance)\n"\
        + "BalanceGraf()\n"
    print("Funciones:\n", str_funciones)
    print("Cuentas existentes:\n", informacion)
    print("\nDinero total en cuentas: $%.2f" % total)
    # return informacion


def Total():
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
    return sum(total)


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
        fila += elementos + "\t"
    fila = fila[:-1]  # Borra el "\t" del final
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


def Ingreso():
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
            fila += elementos + "\t"
        fila = fila[:-1]  # Borra el "\t" del final
        fila += "\n"
        with open(nombre, "a") as micuenta:
            micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    total = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Extraccion():
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
                    fila += elementos + "\t"
                fila = fila[:-1]  # Borra el "\t" del final
                fila += "\n"
                with open(nombre, "a") as micuenta:
                    micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    total = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Transferencia():  # creada 10-02-2019
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
                fila_entrada += elementos + "\t"
            fila_entrada = fila_entrada[:-1]  # Borra el "\t" de mas
            fila_entrada += "\n"
            for elementos in Campos_salida:
                fila_salida += elementos + "\t"
            fila_salida = fila_salida[:-1]  # Borra el "\t" de mas
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
                    fila += elementos + "\t"
                fila = fila[:-1]  # Borra el "\t" del final
                fila += "\n"
                with open(nombre, "a") as micuenta:
                    micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    total = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Balance():  # creada 12-08-2019
    """
    Funcion que guarda en cada transaccion el saldo total de las cuentas
    en función de la fecha.
        Si no está creado el archivo 'Balance.txt' lo crea y guarda el
        primer dato.
        Si ya está creado el archivo 'Balance.txt' appendea los nuevos
        datos.
    Esta función está sólo para ser usada por las funciones que modifican
    los saldos de las cuentas de alguna manera (Gasto(), Ingreso(), etc). No
    usar por usar porque va a appendear datos al pedo.
    """
    total = round(Total(), 2)
    hora = Fecha()[0]
    fecha = Fecha()[1]
    if not os.path.isfile("Balance.txt"):
        with open("Balance.txt", "x") as balance:
            balance.write("Hora\tFecha\tTotal\n")
            balance.write("%s\t%s\t%s\n" % (fecha, hora, total))
    elif os.path.isfile("Balance.txt"):
        with open("Balance.txt", "a") as balance:
            balance.write("%s\t%s\t%s\n" % (fecha, hora, total))
    else:
        print("\nO Se ErRoR rE lOcO\n")


def BalanceGraf():  # 10-09-2019 Se agrega el graficador de balance
    """
    30-08-2019
    Primera aproximación a grafico de balance con fechas y horas.
    Lo que quiero lograr:
        Lograr poner tics solo en los meses.
            Lograr que los puntos se separen
            segun su valor horario. ->10-09-201 solucionado
    """
    data = pd.read_csv("Balance.txt", sep="\t", skiprows=1)
    Data = data.values
    horas = Data[:, 0]
    dias = Data[:, 1]
    T = dias + "-" + horas
    formato = "%d-%m-%Y-%H:%M:%S"
    Tiempo = [datetime.strptime(i, formato) for i in T]
    plt.plot(Tiempo, Data[:, 2], 'o-', fillstyle="none")
    plt.grid()
    plt.xticks(rotation=25)
    plt.show()


def Reajuste():
    """
    17-12-2019
    Funcion que modifica el total del dinero en la cuenta y lo guarda como
    gasto(ingreso) llenando los campos de categoria, subcategoria y
    descripción de la siguiente manera
        Categoria: Reajuste
        Subcategoria: Negativo(Positivo)
        Descripción: Reajuste Negativo(Positivo) de saldo
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre += "CUENTA.txt"
    if os.path.isfile(nombre):
        # Abre y lee los datos de la cuenta
        contenido_cuenta = pd.read_csv(nombre, sep="\t")
        datos = contenido_cuenta.values
        fecha = Fecha()[0]
        hora = Fecha()[1]
        total = input("\nIngrese el saldo actual\n")
        categoria = "Reajuste"
        if datos[-1, 2] < float(total):
            subcategoria = "Positivo"
            descripcion = "Reajuste positivo de saldo"
            extraccion = "0"
            gasto = "0"
            balance = "0"
            ingreso = str(float(total) - datos[-1, 2])
            Campos = [fecha, hora, total, ingreso, extraccion,
                      gasto, categoria, subcategoria, descripcion,
                      balance]
        else:
            subcategoria = "Negativo"
            descripcion = "Reajuste negativo de saldo"
            ingreso = "0"
            gasto = "0"
            balance = "0"
            extraccion = str(datos[-1, 2] - float(total))
            Campos = [fecha, hora, total, ingreso, extraccion,
                      gasto, categoria, subcategoria, descripcion,
                      balance]
        fila = ""
        for elementos in Campos:
            fila += elementos + "\t"
        fila = fila[:-1]  # Borra el "\t" del final
        fila += "\n"
        with open(nombre, "a") as micuenta:
            micuenta.write(fila)
    else:
        print("\nNo existe la cuenta\n")
    dinero_final = pd.read_csv(nombre, sep="\t").values[-1, 2]
    total = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Filtro():  # 10/01/2020
    """
    Con esta funcion se puede ver puntualmente categorias de gastos/ingresos
    para poder llevar un control más sencillo y rápido de cuánto se está 
    gastando/ingresando.
    """
    nombre = input("\nIngrese la cuenta\n")
    nombre = nombre + "CUENTA.txt"
    if os.path.isfile(nombre):
        # Abre y lee los datos de la cuenta
        datos = pd.read_csv(nombre, sep="\t")
        Categoria = input("\nIngrese la categoria\n")
        datos = datos[datos["Categoria"] == Categoria]
        print(datos)
        respuesta = input("\n\nSeguir filtrando?\n\nsi/no\n\n")
        if respuesta == "si":
            Subcategoria = input("\nIngrese la subcategoria\n")
            datos = datos[datos["Subcategoria"] == Subcategoria]
            return datos
        else:
            return datos
    else:
        print("\nNo existe la cuenta\n")
# %%


IniciarSesion()
