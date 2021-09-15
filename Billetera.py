# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos
"""
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from ConversorClass import ConversorMoneda

directory = os.path.dirname(os.path.abspath(__file__))

os.chdir(directory)
pd.set_option("display.max_columns", 11)
# %%
"""
Cosas que quisiera ir agregándole al script:


TODO    Editor de entradas:
        Alguna manera para editar un gasto, un ingreso, o algo que fue mal
        ingresado (puede que haga falta usar archivos temporales y librerias
        afines)

TODO    Graficos:
        Alguna forma fácil de ver gastos/ingresos/whatever por día, por semana
        por mes, por año.

TODO    Interfaz Gráfica y ejectuable:
        nada, eso, a futuro (lejano)

TODO    Que no se pueda crear usuario estando logueado en algún usuario

TODO    Separar todo este script en módulos.

TODO    Que no se puedan hace transferencias de cuentas de distintos tipos
        (de pesos a dolares o dolares a pesos)
"""


def Fecha():
    """Generates a dictionary with date an time in a latin-format: d-m-y"""
    fecha_hora = datetime.now()
    fecha = fecha_hora.strftime("%d-%m-%Y")
    hora = fecha_hora.strftime("%H:%M:%S")
    return {"Fecha": fecha, "hora": hora}


def precio_dolar(verbose=False):
    """
    Gets the current dollar price by scrapping from web or inferring it from
    previuos data from Balances.txt
    """
    # Creo el objeto que maneja la consulta y me devuelve el precio
    dolar = ConversorMoneda(verbose=verbose)
    try:
        # Trato de conseguir el precio de internet, si no, handleo el error
        dollar_val = dolar.precio()["Dolar U.S.A"]["Compra"]
    except AttributeError as error:
        if verbose is True:
            print("Ocurrio el siguiente error durante la consulta:")
            print(error)
            print("Seguramente se debe a un error urlopen y no de Attribute")
        print(
            "No se pudo obtener el precio del dolar de internet, se usó la",
            " última cotización",
        )
        # Como no pude conseguir el precio de internet, lo infiero de el último
        # balance en la cuenta Balance.txt
        bal_datos = pd.read_csv("Balance.txt", sep="\t", encoding="latin1")
        tot_dinero = bal_datos["Total"].values[-1]
        tot_pesos = bal_datos["Total_pesos"].values[-1]
        tot_dolares = bal_datos["Total_dolares"].values[-1]
        try:
            dollar_val = str(round((tot_dinero - tot_pesos) / tot_dolares, 2))
        except ZeroDivisionError:
            print("No hay dolares, asi que no importa cuanto vale")
            dollar_val = "0.00"

    return float(dollar_val.replace(",", "."))


def info():
    """List of functions, utilities and total balances"""
    funciones = [
        "Fecha()",
        "precio_dolar()",
        "info()",
        "crear_usuario()",
        "iniciar_sesion()",
        "cerrar_sesion()",
        "Crear_cuenta()",
        "Lista_cuentas()",
        "Datos_cuenta()",
        "asignador_cuentas()",
        "totales()",
        "Ingreso()",
        "Extraccion()",
        "Gasto()",
        "Transferencia()",
        "Reajuste()",
        "balances()<--NO USAR-ver help",
        "BalanceGraf()",
        "Filtro()",
        "balances()",
        "balances_totales()",
    ]
    # lista con los nombres de los archivos de cuenta
    acc_list = lista_cuentas()
    dollar_val = precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = []
    for elem in acc_list:
        total_cta = pd.read_csv(elem, sep="\t", encoding="latin1")["Total"]
        # Si la cuenta tiene datos, appendeo el valor
        if len(total_cta) != 0:
            total.append(total_cta.values[-1])
        # Si la cuenta es nueva y no tiene datos, appendeo 0
        else:
            total.append(0)
    # Parrafo con los datos de todas las cuentas
    info_msg = ""
    for i, elem in enumerate(acc_list):
        if "DOL" in elem:
            dolar_tot = total[i]
            pesos_tot = total[i] * dollar_val
            info_msg += f"\n{elem}: Saldo u$s {dolar_tot:.2f}, "
            info_msg += f"saldo total ${pesos_tot:.2f}\n"
        else:
            info_msg += f"\n{elem}: Saldo total $ {total[i]:.2f}\n"
    # Limpio los strings que molestan
    info_msg = (
        info_msg.replace("CUENTA", "").replace("_DOL", "").replace(".txt", "")
    )
    # Calculo todos los totales
    totals_dict = totales()
    # Printeo toda la información
    str_funciones = "\n".join(funciones)
    print("Funciones:\n", str_funciones)
    print("=" * 79)
    print("Cuentas existentes:\n", info_msg)
    print("=" * 79)
    print(f"Dolares totales: ${totals_dict['total_dol']:.2f}")
    print("=" * 79)
    print(f"Pesos totales: ${totals_dict['total_pesos']:.2f}")
    print("=" * 79)
    print(f"Dinero total en cuentas: ${totals_dict['total']:.2f}")
    print("=" * 79)


# %%


def crear_usuario():
    """Creates the user's directory where all accounts will be stored"""
    nombre = input("\nIngrese el nombre de usuario\n") + "USR"
    if os.path.isdir(nombre):  # 10/01/2020 msj al intentar crear usr existente
        print("\nYa existe el usuario\n")
    else:
        os.makedirs(nombre)
        print("\nSe creo el usuario %s\n" % nombre.strip("USR"))


def iniciar_sesion():
    """Changes the current working directory to the user's directory"""
    nombre = input("\nNombre de usuario\n") + "USR"
    if os.path.isdir(nombre):
        path = directory + "/" + nombre
        os.chdir(path)
        print("\nInicio de sesion de %s\n" % nombre.strip("USR"))
        info()
    else:
        print("\nNo existe el usuario\n")


def cerrar_sesion():
    """Changes the current working directory to the base directory"""
    os.chdir(directory)
    print("\nSe ha cerrado sesión\n")


def eliminar_usuario():
    """
    Delets the directory of the given user, including all data stored in it
    """
    nombre = input("\nIngrese el nombre de usuario a borrar\n") + "USR"
    if os.path.isdir(nombre):
        advertencia = "¿Seguro que queres eliminar el usuario?\n\n\
        todos los datos contenidos en ella se perderán para siempre.\n\n\
        Ingrese '1', 'si' o 'y' para borrar\n\
        Ingrese cualquier otra cosa para cancelar\n"
        respuesta = input(advertencia)
        posibles_respuestas = ["1", "si", "y"]
        if respuesta in posibles_respuestas:
            try:
                os.rmdir(nombre)
                print("\nSe eliminó el usuario %s\n" % nombre.strip("USR"))
            except OSError:
                from shutil import rmtree

                rmtree(nombre)
                nombre = nombre.strip("USR")
                print(f"\nSe eliminó el usuario {nombre} y todos sus datos.")
        else:
            nombre = nombre.strip("USR")
            print(f"\nNo se eliminó el usuario {nombre}\n")
    else:
        print("\nNo existe el usuario\n")


# %%


def crear_cuenta():
    """Creates a .txt file which name will be the account name"""
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    tipo_cuenta = input(
        "\nIngresar 0 para cuenta en pesos\n"
        "Ingresar 1 para cuenta en dolares\n"
    )
    if tipo_cuenta == "0":
        nombre += "CUENTA.txt"
    elif tipo_cuenta == "1":
        nombre += "CUENTA_DOL.txt"
    else:
        print("\n %s inválido\n" % tipo_cuenta)
    columns = [
        "Fecha",
        "hora",
        "Total",
        "Ingresos",
        "Extracciones",
        "Gasto",
        "Categoria",
        "Subcategoria",
        "Descripcion",
        "Balance",
    ]
    fila = "\t".join(columns) + "\n"
    with open(nombre, "x") as micuenta:
        micuenta.write(fila)
    print(
        "\nSe ha creado la cuenta %s\n"
        % nombre.strip("_DOL.txt").strip("CUENTA")
    )


def eliminar_cuenta():
    """Deletes the .txt file of the given account name"""
    nombre = asignador_cuentas()
    advertencia = "¿Seguro que queres eliminar la cuenta?\n\n\
    todos los datos contenidos en ella se perderán para siempre.\n\n\
    Ingrese '1', 'si' o 'y' para borrar\n\
    Ingrese cualquier otra cosa para cancelar\n"
    respuesta = input(advertencia)
    posibles_respuestas = ["1", "si", "y"]
    if respuesta in posibles_respuestas:
        os.remove(nombre)
        print(
            "\nSe eliminó la cuenta %s\n"
            % nombre.strip("_DOL.txt").strip("CUENTA")
        )
    else:
        print(
            "\nNo se eliminó la cuenta %s\n"
            % nombre.strip("_DOL.txt").strip("CUENTA")
        )


def lista_cuentas():
    """
    Lists all accounts found inside the given user's directory
    """
    file_list = os.listdir()
    acc_list = []
    for elem in file_list:
        if "CUENTA.txt" in elem or "CUENTA_DOL.txt" in elem:
            acc_list.append(elem)
    return acc_list


def datos_cuenta():
    """Return a pandas DataFrame with data of a given account"""
    nombre = asignador_cuentas()
    datos = pd.read_csv(nombre, sep="\t", encoding="latin1")
    return datos


def asignador_cuentas():
    """
    Account selector in a numerical way: Associates a number to a given account
    so it can be selected by typing the number and not the name
    """
    alfabeto = lista_cuentas()
    dic = {}
    Cuentas = ""
    for i, elem in enumerate(alfabeto):
        # voy armando un diccionario que asigna un numero a cada cuenta
        dic.update({str(i + 1): elem})
        # defino una variable sin sufijos para printear
        cuenta_str = (
            elem.replace("CUENTA", "").replace("_DOL", "").replace(".txt", "")
        )
        # actualizo el string final que se imprime en consola
        Cuentas += "\n" + str(i + 1) + ": " + cuenta_str + "\n"
    # Meto un input de teclado
    while True:
        numero_cta = input("\nElija la cuenta\n" + Cuentas + "\n")
        try:
            nombre_cuenta = dic[numero_cta]
            return nombre_cuenta
        except KeyError:
            print("=" * 50)
            print(
                "\nValor elegido: '%s' erroneo, intente de nuevo." % numero_cta
            )
            print("Presione Ctrol+C para salir\n")
            print("=" * 50)


def totales():
    """Calculate the total amount of money for all accounts"""
    # lista con los nombres de los archivos de cuenta
    acc_list = lista_cuentas()
    dollar_val = precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = 0
    total_pesos = 0
    total_dol = 0
    for elem in acc_list:
        df_data = pd.read_csv(elem, sep="\t", encoding="latin1")
        # Si la cuenta no es nueva, entonces busca el total, si no, al no tener
        # dinero adentro, va a tirar IndexError. En ese caso el valor_elem = 0
        try:
            valor_elem = float(df_data["Total"].values[-1])
            if "DOL" in elem:
                total_dol += valor_elem
                total += valor_elem * dollar_val
            else:
                total_pesos += valor_elem
                total += valor_elem
        except IndexError:
            total.append(0)
    # Reciclo las variables reescribiéndolas
    total = round(total, 2)
    total_pesos = round(total_pesos, 2)
    total_dolares = round(total_dol, 2)
    dic = {"total": total, "total_pesos": total_pesos, "total_dol": total_dol}
    return dic


# %%


def ingreso():
    """
    Account operation:
    Income with input commands:
        account name,
        income amount,
        category,
        subcategory,
        description
    saves the data into the given account and appends one row into the balance
    file
    """
    nombre = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = input("\nCantidad de dinero a ingresar\n")
    categoria = input("\nCategoría: \n")
    subcategoria = input("\nSubcategoría: \n")
    descripcion = input("\nDescripción: \n")
    extraccion = "0.00"  # esto siempre debería ser 0 al ingresar dinero
    gasto = "0.00"  # esto siempre debería ser 0 al ingresar dinero
    if len(datos) == 0:
        total = ingreso
    else:
        total = str(round(float(ingreso) + datos[-1, 2], 2))
    balance = "0"  # TODO: ver si balance es necesario
    columns = [
        fecha,
        hora,
        total,
        ingreso,
        extraccion,
        gasto,
        categoria,
        subcategoria,
        descripcion,
        balance,
    ]
    # Escribo la fila que se va a appendear al archivo
    fila = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(nombre, "a") as micuenta:
        micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")["Total"]
    print(
        "\nDinero en cuenta: $%.2f\n" % dinero_final.values[-1],
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()


def extraccion():
    """
    Account operation:
    Extraction with input commands:
        account name,
        extraction amount,
        category,
        subcategory,
        description
    saves the data into the given account and appends one row into the balance
    file
    """
    nombre = asignador_cuentas()
    # se fija si el archivo de la cuenta existe
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = "0.00"  # esto siempre debería ser 0 al extraer dinero
    gasto = "0.00"  # esto es 0 por definicion de extraccion =/= gasto
    if len(datos) == 0:
        print("\nAún no se ha ingresado dinero en la cuenta\n")
    else:
        extraccion = input("\nCantidad de dinero a extraer\n")
        if datos[-1, 2] < float(extraccion):
            print("\nNo hay dinero suficiente en la cuenta\n")
        else:
            categoria = input("\nCategoría: \n")
            subcategoria = input("\nSubcategoría: \n")
            descripcion = input("\nDescripción: \n")
            total = str(round(datos[-1, 2] - float(extraccion), 2))
            balance = "0"  # TODO: ver si balance es necesario
            columns = [
                fecha,
                hora,
                total,
                ingreso,
                extraccion,
                gasto,
                categoria,
                subcategoria,
                descripcion,
                balance,
            ]
            # Escribo la fila que se va a appendear al archivo
            fila = "\t".join(columns) + "\n"
            # La appendeo al archivo
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")["Total"]
    print(
        "\nDinero en cuenta: $%.2f\n" % dinero_final.values[-1],
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()


def gasto():
    """
    Account operation:
    Expenses with input commands:
        account name,
        expense amount,
        category,
        subcategory,
        description
    saves the data into the given account and appends one row into the balance
    file
    """
    nombre = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = "0.00"  # esto siempre debería ser 0 al hacer un gasto
    extraccion = "0.00"  # esto siempre debería ser 0 al hacer un gasto
    if len(datos) == 0:
        return print("\nNo hay dinero en la cuenta\n")
    else:
        valor = input("\nValor del gasto\n")
        if datos[-1, 2] < float(valor):
            print("\nNo hay dinero suficiente en la cuenta\n")
        else:
            categoria = input("\nCategoría: \n")
            subcategoria = input("\nSubcategoría: \n")
            descripcion = input("\nDescripción: \n")
            total = str(round(datos[-1, 2] - float(valor), 2))
            balance = "0"  # TODO: ver si balance es necesario
            columns = [
                fecha,
                hora,
                total,
                ingreso,
                extraccion,
                valor,
                categoria,
                subcategoria,
                descripcion,
                balance,
            ]
            # Escribo la fila que se va a appendear al archivo
            fila = "\t".join(columns) + "\n"
            # La appendeo al archivo
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")["Total"]
    print(
        "\nDinero en cuenta: $%.2f\n" % dinero_final.values[-1],
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()


def transferencia():
    """
    Account operation:
    Makes a tranfer between to accounts of the same type only (currentyl it
    is possible to make transfers between to accounts of different type but
    it will lead to data errors). If the input is the same account twice, it
    returns a message and nothing happens.
    No balance change are made with this operation.
    """
    # Abro la cuenta de salida
    print("Cuenta salida:")
    nombre_salida = asignador_cuentas()
    info_salida = pd.read_csv(nombre_salida, sep="\t", encoding="latin1")
    # Si la cuenta de saldia está vacía, o no tiene dinero, se cancela la
    # transferencia
    if len(info_salida) == 0 or info_salida["Total"].values[-1] == 0:
        return print("\nNo hay dinero en la cuenta %s\n" % nombre_salida[:-10])
    # Abro la cuenta de entrada
    print("cuenta entrada:")
    nombre_entrada = asignador_cuentas()
    info_entrada = pd.read_csv(nombre_entrada, sep="\t", encoding="latin1")
    try:
        tot_entrada_i = info_entrada["Total"].values[-1]
    except IndexError:
        tot_entrada_i = 0.0
    # No permito transferencias a una misma cuenta.
    if nombre_entrada == nombre_salida:
        return print("\nNo tiene sentido transferir a una misma cuenta!!\n")
    # Fecha y hora
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    # Valor a transferir
    valor = input("\nCantidad de dinero a transferir\n")
    tot_salida_i = info_salida["Total"].values[-1]
    if tot_salida_i < float(valor):
        print(
            "\nNo hay dinero suficiente en la cuenta %s" % nombre_salida[:-10]
        )
    else:
        categoria = "Transferencia"
        subcategoria_salida = "Transferencia de salida"
        descripcion_salida = "Transferencia a %s" % nombre_entrada.strip(
            "CUENTA.txt"
        )
        subcategoria_entrada = "Transferencia de entrada"
        descripcion_entrada = "Transferencia de %s" % nombre_salida.strip(
            "CUENTA.txt"
        )
        tot_salida_f = str(round(tot_salida_i - float(valor), 2))
        tot_entrada_f = str(round(tot_entrada_i + float(valor), 2))
        balance = gasto = extraccion = ingreso = "0.00"
        # TODO: ver si balance es necesario
        columns_in = [
            fecha,
            hora,
            tot_entrada_f,
            valor,
            extraccion,
            gasto,
            categoria,
            subcategoria_entrada,
            descripcion_entrada,
            balance,
        ]
        columns_out = [
            fecha,
            hora,
            tot_salida_f,
            ingreso,
            valor,
            gasto,
            categoria,
            subcategoria_salida,
            descripcion_salida,
            balance,
        ]
        # Escribo las filas que se van a appendear al archivo
        fila_entrada = "\t".join(columns_in) + "\n"
        fila_salida = "\t".join(columns_out) + "\n"
        # Las appendeo a los archivos
        with open(nombre_entrada, "a") as micuenta:
            micuenta.write(fila_entrada)
        with open(nombre_salida, "a") as micuenta:
            micuenta.write(fila_salida)


def reajuste():
    """
    Account operation:
    Ajust the account total according to the given input. It is used if for
    some reason the tracked expenses/incomes are not precise and a correction
    to the total values is needed in order to update amounts. It automatically
    decides if it is an income or and expense.
    Saves the data into the given account and appends one row into the balance
    file
    """
    nombre = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    acc_total = pd.read_csv(nombre, sep="\t", encoding="latin1")["Total"]
    acc_total = acc_total.values[-1]
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    total = input("\nIngrese el saldo actual\n")
    categoria = "Reajuste"
    if acc_total < float(total):
        subcategoria = "Positivo"
        descripcion = "Reajuste positivo de saldo"
        extraccion = "0.00"
        gasto = "0.00"
        balance = "0.00"
        ingreso = str(round(float(total) - acc_total, 2))
        columns = [
            fecha,
            hora,
            total,
            ingreso,
            extraccion,
            gasto,
            categoria,
            subcategoria,
            descripcion,
            balance,
        ]
    else:
        subcategoria = "Negativo"
        descripcion = "Reajuste negativo de saldo"
        ingreso = "0.00"
        gasto = "0.00"
        balance = "0.00"
        extraccion = str(round(acc_total - float(total), 2))
        columns = [
            fecha,
            hora,
            total,
            ingreso,
            extraccion,
            gasto,
            categoria,
            subcategoria,
            descripcion,
            balance,
        ]
    # Escribo la fila que se va a appendear al archivo
    fila = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(nombre, "a") as micuenta:
        micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")["Total"]
    print(
        "\nDinero en cuenta: $%.2f\n" % dinero_final.values[-1],
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()


def balances():
    """
    Non-user operation:
    Appends one row to the balance file everytime an account operation that
    modifies the balance is done.
    If the balance file exists, appends data. If the balance file does not
    exists, it creates it and appends the data.
    --------------------------------------------------------------------------
    Do not use this function manually, it is only intended to be used by other
    functions.
    """
    total, total_pesos, total_dolares = list(totales().values())
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    if not os.path.isfile("Balance.txt"):
        with open("Balance.txt", "x") as balance:
            balance.write("Hora\tFecha\tTotal\tTotal_pesos\tTotal_dolares\n")
            balance.write(
                "%s\t%s\t%s\t%s\t%s\n"
                % (hora, fecha, total, total_pesos, total_dolares)
            )
    elif os.path.isfile("Balance.txt"):
        with open("Balance.txt", "a") as balance:
            balance.write(
                "%s\t%s\t%s\t%s\t%s\n"
                % (hora, fecha, total, total_pesos, total_dolares)
            )
    else:
        print("\nO Se ErRoR rE lOcO\n")


def balance_graf():
    """
    Makes a plot with all data from the balance file. It includes:
        Total amount,
        Total pesos only,
        Total dollars only,
    """
    data = pd.read_csv("Balance.txt", sep="\t")
    # Armo un string con la fecha y la hora en el formato del .txt
    str_time = data["Fecha"] + "-" + data["Hora"]
    # Especifico ese formato acá, para usarlo en la funcion strptime
    formato = "%d-%m-%Y-%H:%M:%S"
    # transformo el string a un objeto datetime usando el formato dado
    time = [datetime.strptime(i, formato) for i in str_time]
    plt.plot(
        time,
        data["Total"],
        "o-",
        alpha=0.5,
        fillstyle="full",
        markersize=5,
        label="Total: $%.2f" % data["Total"].values[-1],
    )
    plt.plot(
        time,
        data["Total_pesos"],
        "o-",
        alpha=0.5,
        fillstyle="none",
        markersize=3,
        label="Total de pesos: $%.2f" % data["Total_pesos"].values[-1],
    )
    plt.plot(
        time,
        data["Total_dolares"],
        "-",
        alpha=0.5,
        fillstyle="none",
        label="Total de dolares: u$s%.2f" % data["Total_dolares"].values[-1],
    )
    plt.grid()
    plt.legend()
    plt.xticks(rotation=25)
    plt.show()


def filtro():
    """
    Analysis function:
    Easy way to filter data from a given account by category and subcategory
    """
    nombre = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    datos = pd.read_csv(nombre, sep="\t", encoding="latin1")
    categoria = input("\nIngrese la categoría\n")
    datos = datos[datos["Categoria"] == categoria]
    print(datos)
    respuesta = input("\n\nSeguir filtrando?\n\nsi/no\n\n")
    if respuesta == "si":
        subcategoria = input("\nIngrese la subcategoría\n")
        datos = datos[datos["Subcategoria"] == subcategoria]
        return datos
    return datos


# %%


def balances_cta(account: str, month: int, year: int):
    """
    Analysis function:
    Easy way to get the monthly balance of a given account: Incomes, expenses
    and balance: income - expenses
    Inputs:
        account: str
        Acccount name as file or path, ej: MercadoPagoCUENTA.txt
        month: int
        Month number to check balance: Valids from 1 to 12
        year: int
        Year numberto check balance: Valids 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por cuenta: float
    """
    df_data = pd.read_csv(
        account,
        sep="\t",
        index_col=("Fecha"),
        parse_dates=True,
        dayfirst=True,
        encoding="latin1",
    )
    montly_src = df_data[
        (df_data.index.month == month)
        & (df_data.index.year == year)
        & (df_data["Categoria"] != "Transferencia")
    ]
    montly_spend = montly_src["Gasto"].sum()
    montly_spend += montly_src["Extracciones"].sum()
    montly_earn = montly_src["Ingresos"].sum()
    balance = montly_earn - montly_spend

    return {
        "Ingresos_m": round(montly_earn, 2),
        "Gasto_m": round(montly_spend, 2),
        "Balance_m": round(balance, 2),
    }


def balances_totales(month: int, year: int, verbose=False):
    """
    Analysis function:
    Easy way to see the total balance of the sum all over the accounts, given
    a month and a year:  Total incomes, total expenses and total balances.
    It uses balances()
    Inputs:
        month: int
        Month number to check balance: Valids from 1 to 12
        year: int
        Year numberto check balance: Valids 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por usuario: float
    """
    ingresos_tot = gastos_tot = balances_tot = 0
    for cuenta in os.listdir():
        if "CUENTA" in cuenta and "DOL" not in cuenta:
            try:
                dic_c = balances_cta(cuenta, month, year)
            except AttributeError as error:
                if verbose is True:
                    print("Error en la cuenta: ", cuenta)
                    print(error)
            ingresos_tot += dic_c["Ingresos_m"]
            gastos_tot += dic_c["Gasto_m"]
            balances_tot += dic_c["Balance_m"]

    return {
        "Ingresos_tot": round(ingresos_tot, 2),
        "Gasto_tot": round(gastos_tot, 2),
        "Balance_tot": round(balances_tot, 2),
    }


# %%


iniciar_sesion()
