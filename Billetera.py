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
    time = datetime.now()
    date = time.strftime("%d-%m-%Y")
    hour = time.strftime("%H:%M:%S")
    return {"Fecha": date, "hora": hour}


def precio_dolar(verbose=False):
    """
    Gets the current dollar price by scrapping from web or inferring it from
    previuos data from Balances.txt
    """
    # Creo el objeto que maneja la consulta y me devuelve el precio
    exchange = ConversorMoneda(verbose=verbose)
    try:
        # Trato de conseguir el precio de internet, si no, handleo el error
        dollar_val = exchange.precio()["Dolar U.S.A"]["Compra"]
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


def extra_char_cleanner(charchain: str):
    """
    Streaps all chars from the account string name except of its name
    returns the name cleaned
    """
    charchain = (
        charchain.replace("CUENTA", "")
        .replace("_DOL", "")
        .replace(".txt", "")
        .replace("USR", "")
    )
    return charchain


def info(verbose=True):
    """List of functions, utilities and total balances"""
    functions = [
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
        acc_total = pd.read_csv(elem, sep="\t", encoding="latin1")["Total"]
        # Si la cuenta tiene datos, appendeo el valor
        if len(acc_total) != 0:
            total.append(acc_total.values[-1])
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
    info_msg = extra_char_cleanner(info_msg)

    # Calculo todos los totales
    totals_dict = totales()
    # Printeo toda la información
    str_functions = "\n".join(functions)
    if verbose:
        print("Funciones:\n", str_functions)
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
    folder_name = input("\nIngrese el nombre de usuario\n") + "USR"
    user_name = extra_char_cleanner(folder_name)
    if os.path.isdir(folder_name):
        print(f"\nYa existe el usuario '{user_name}'\n")
    else:
        os.makedirs(folder_name)
        print(f"\nSe creo el usuario '{user_name}'\n")


def iniciar_sesion():
    """Changes the current working directory to the user's directory"""
    folder_name = input("\nNombre de usuario\n") + "USR"
    user_name = extra_char_cleanner(folder_name)
    if os.path.isdir(folder_name):
        path = directory + "/" + folder_name
        os.chdir(path)
        print(f"\nInicio de sesion de {user_name}\n")
        info()
    else:
        print(f"\nNo existe el usuario '{user_name}'\n")


def cerrar_sesion():
    """Changes the current working directory to the base directory"""
    os.chdir(directory)
    print("\nSe ha cerrado sesión\n")


def eliminar_usuario():
    """
    Delets the directory of the given user, including all data stored in it
    """
    folder_name = input("\nIngrese el nombre de usuario a borrar\n") + "USR"
    user_name = extra_char_cleanner(folder_name)
    if os.path.isdir(folder_name):
        advertencia = (
            f"¿Seguro que queres eliminar el usuario '{user_name}'?\n\n"
            "todos los datos contenidos en él se perderán para siempre.\n\n"
            "Ingrese '1', 'si' o 'y' para borrar\n"
            "Ingrese cualquier otra cosa para cancelar\n"
        )
        respuesta = input(advertencia)
        posibles_respuestas = ["1", "si", "y"]
        if respuesta in posibles_respuestas:
            try:
                os.rmdir(folder_name)
                print(f"\nSe eliminó el usuario {user_name}\n")
            except OSError:
                from shutil import rmtree

                rmtree(folder_name)
                print(f"\nSe eliminó el usr. {user_name} y todos sus datos.")
        else:
            print(f"\nNo se eliminó el usuario {user_name}\n")
    else:
        print(f"\nNo existe el usuario {user_name}\n")


# %%


def crear_cuenta():
    """Creates a .txt file which name will be the account name"""
    file_name = input("\nIntroduzca el nombre para la nueva cuenta\n")
    acc_type = input(
        "\nIngresar 0 para cuenta en pesos\n"
        "Ingresar 1 para cuenta en dolares\n"
    )
    if acc_type == "0":
        file_name += "CUENTA.txt"
    elif acc_type == "1":
        file_name += "CUENTA_DOL.txt"
    else:
        print(f"\n '{acc_type}' inválido\n")
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
    row = "\t".join(columns) + "\n"
    with open(file_name, "x") as micuenta:
        micuenta.write(row)
    acc_name = extra_char_cleanner(file_name)
    print(f"\nSe ha creado la cuenta {acc_name}\n")


def eliminar_cuenta():
    """Deletes the .txt file of the given account name"""
    file_name = asignador_cuentas()
    warning = "¿Seguro que queres eliminar la cuenta?\n\n\
    todos los datos contenidos en ella se perderán para siempre.\n\n\
    Ingrese '1', 'si' o 'y' para borrar\n\
    Ingrese cualquier otra cosa para cancelar\n"
    user_answer = input(warning)
    possible_answers = ["1", "si", "y"]
    if user_answer in possible_answers:
        os.remove(file_name)
        acc_name = extra_char_cleanner(file_name)
        print(f"\nSe eliminó la cuenta {acc_name}\n")
    else:
        acc_name = extra_char_cleanner(file_name)
        print(f"\nNo se eliminó la cuenta {acc_name}\n")


def lista_cuentas():
    """Lists all accounts found inside the given user's directory"""
    file_list = os.listdir()
    acc_list = []
    for file in file_list:
        if "CUENTA.txt" in file or "CUENTA_DOL.txt" in file:
            acc_list.append(file)
    return acc_list


def datos_cuenta():
    """Return a pandas DataFrame with data of a given account"""
    file_name = asignador_cuentas()
    data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    return data


def asignador_cuentas():
    """
    Account selector in a numerical way: Associates a number to a given account
    so it can be selected by typing the number and not the name
    """
    acc_list = lista_cuentas()
    acc_range = range(1, len(acc_list) + 1)
    dic = dict(zip(acc_range, acc_list))
    account_index = ""
    for i, acc in enumerate(acc_list):
        # defino una variable sin sufijos para printear
        acc_str = extra_char_cleanner(acc)
        # actualizo el string final que se imprime en consola
        account_index += "\n" + str(i + 1) + ": " + acc_str + "\n"
    # Meto un input de teclado
    while True:
        acc_number = int(input("\nElija la cuenta\n" + account_index + "\n"))
        try:
            acc_name = dic[acc_number]
            return acc_name
        except KeyError:
            print("=" * 79)
            print(
                f"\nValor elegido: '{acc_number}' erroneo, intente de nuevo."
            )
            print("Presione Ctrol+C para salir\n")
            print("=" * 79)


def totales():
    """Calculate the total amount of money for all accounts"""
    # lista con los nombres de los archivos de cuenta
    acc_list = lista_cuentas()
    dollar_val = precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = 0
    total_pesos = 0
    total_dol = 0
    for acc in acc_list:
        df_data = pd.read_csv(acc, sep="\t", encoding="latin1")
        # Si la cuenta no es nueva, entonces busca el total, si no, al no tener
        # dinero adentro, va a tirar IndexError. En ese caso el valor_elem = 0
        try:
            valor_elem = float(df_data["Total"].values[-1])
            if "DOL" in acc:
                total_dol += valor_elem
                total += valor_elem * dollar_val
            else:
                total_pesos += valor_elem
                total += valor_elem
        except IndexError:
            pass
    # Reciclo las variables reescribiéndolas
    total = round(total, 2)
    total_pesos = round(total_pesos, 2)
    total_dol = round(total_dol, 2)
    dic = {"total": total, "total_pesos": total_pesos, "total_dol": total_dol}
    return dic


def input_selector():
    """ 
    Non-user operation:
    Intended to be only by operation_selector
    """
    category = input("\nCategoría: \n")
    subcategory = input("\nSubcategoría: \n")
    description = input("\nDescripción: \n")
    return category, subcategory, description


def operation_seletor(operation: str) -> dict:
    """
    Non-user operation:
    generates de columns that will be append into the account file
    """
    date = Fecha()["Fecha"]
    hour = Fecha()["hora"]
    income = expense = extraction = total = balance = "0.00"
    if operation == "income":
        income = input("\nCantidad de dinero a ingresar\n")
        category, subcategory, description = input_selector()
    elif operation == "expense":
        expense = input("\nValor del gasto\n")
        category, subcategory, description = input_selector()
    elif operation == "extraction":
        extraction = input("\nCantidad de dinero a extraer\n")
        category, subcategory, description = input_selector()
    elif operation == "transfer":
        income = extraction = input("\nCantidad de dinero a transferir\n")
        expense = "0.00"
        category = "Transferencia"
        subcategory = ""
        description = ""
    elif operation == "readjust":
        total = input("\nIngrese el saldo actual\n")
    columns_dict = {
        "date": date,
        "hour": hour,
        "total": total,
        "income": income,
        "extraction": extraction,
        "expense": expense,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "balance": balance,
    }
    return columns_dict


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
    file_name = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    acc_data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    columns = operation_seletor(operation="income")
    if float(columns["income"]) == 0:
        return print("\nNo se está ingresando dinero.\n")
    if len(acc_data) == 0:
        columns["total"] = new_total = columns["income"]
    else:
        last_total = acc_data["Total"].values[-1]
        new_total = float(columns["income"]) + last_total
        columns["total"] = f"{new_total:.2f}"
    # redefine columns from dict to list
    columns = list(columns.values())
    # Escribo la fila que se va a appendear al archivo
    row = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(file_name, "a") as micuenta:
        micuenta.write(row)
    print(
        f"\nDinero en cuenta: ${new_total}\n",
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
    file_name = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    acc_data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    if len(acc_data) == 0:
        return print("\nAún no se ha ingresado dinero en la cuenta\n")
    last_total = acc_data["Total"].values[-1]
    columns = operation_seletor("extraction")
    if last_total < float(columns["extraction"]):
        return print("\nNo hay dinero suficiente en la cuenta\n")
    new_total = last_total - float(columns["extraction"])
    columns["total"] = f"{new_total:.2f}"
    # redefine columns from dict to list
    columns = list(columns.values())
    # Escribo la fila que se va a appendear al archivo
    row = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(file_name, "a") as micuenta:
        micuenta.write(row)
    print(
        f"\nDinero en cuenta: ${new_total:.2f}\n"
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
    file_name = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    acc_data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    if len(acc_data) == 0:
        return print("\nNo hay dinero en la cuenta\n")
    last_total = acc_data["Total"].values[-1]
    columns = operation_seletor("expense")
    if last_total < float(columns["expense"]):
        return print("\nNo hay dinero suficiente en la cuenta\n")
    new_total = last_total - float(columns["expense"])
    columns["total"] = f"{new_total:.2f}"
    # redefine columns from dict to list
    columns = list(columns.values())
    # Escribo la fila que se va a appendear al archivo
    row = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(file_name, "a") as micuenta:
        micuenta.write(row)
    print(
        f"\nDinero en cuenta: ${new_total:.2f}\n",
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
    # Select the outgoing account, open its data, save its name and its total
    print("Cuenta salida:")
    file_name_out = asignador_cuentas()
    acc_name_out = extra_char_cleanner(file_name_out)
    acc_data_out = pd.read_csv(file_name_out, sep="\t", encoding="latin1")
    # check if the acc is empty or with 0 total
    if len(acc_data_out) == 0:
        return print(f"\nNo hay datos en la cuenta {acc_name_out}\n")
    last_total_out = acc_data_out["Total"].values[-1]
    if last_total_out == 0:
        return print(f"\nFondos insuficientes en la cuenta {acc_name_out}\n")

    # Select de incoming account, open its data, save its name and its total
    print("cuenta entrada:")
    file_name_in = asignador_cuentas()
    acc_name_in = extra_char_cleanner(file_name_in)
    acc_data_in = pd.read_csv(file_name_in, sep="\t", encoding="latin1")
    try:
        last_total_in = acc_data_in["Total"].values[-1]
    except IndexError:
        last_total_in = 0.0

    # Transfers with the same account are not allowed
    if file_name_in == file_name_out:
        return print("\nNo tiene sentido transferir a una misma cuenta!!\n")

    # Format all de columns correctly
    columns_in = operation_seletor(operation="transfer")
    columns_out = columns_in.copy()
    columns_in["extraction"] = "0.00"
    columns_in["subcategory"] = "Transferencia de entrada"
    columns_in["description"] = f"Transferencia de {acc_name_out}"
    columns_out["income"] = "0.00"
    columns_out["subcategory"] = "Transferencia de salida"
    columns_out["description"] = f"Transferencia a {acc_name_in}"

    # Insuficient if the amount to transfer is grater than the last_total_out
    if last_total_out < float(columns_in["income"]):
        return print(f"\nFondos insuficiente en la cuenta {acc_name_out}")

    # New total and columns total
    new_total_in = float(columns_in["income"]) + last_total_in
    columns_in["total"] = f"{new_total_in:.2f}"
    new_total_out = last_total_out - float(columns_out["extraction"])
    columns_out["total"] = f"{new_total_out:.2f}"

    # Dict columns to list columns
    columns_in = list(columns_in.values())
    columns_out = list(columns_out.values())

    # List columns to char string to be written
    row_in = "\t".join(columns_in) + "\n"
    row_out = "\t".join(columns_out) + "\n"

    # Append the new data
    with open(file_name_in, "a") as myaccount:
        myaccount.write(row_in)
    with open(file_name_out, "a") as myaccount:
        myaccount.write(row_out)
    print(
        f"\nDinero en {acc_name_in}: ${new_total_in:.2f}\n",
        f"\nDinero en {acc_name_out}: ${new_total_out:.2f}\n",
    )


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
