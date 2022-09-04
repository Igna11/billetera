# -*- coding: utf-8 -*-
"""
Created on Sat Sept 03 20:01:51 2022

@author: igna
Modulo para condensar las funciones que tienen movimientos
gastos
ingresos
extracciones
transferencias
"""
import pandas as pd


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
    """
    Non-user function:
    Lists all accounts found inside the given user's directory"""
    file_list = os.listdir()
    acc_list = []
    for file in file_list:
        if "CUENTA.txt" in file or "CUENTA_DOL.txt" in file:
            acc_list.append(file)
    return acc_list


def datos_cuenta():
    """
    Analysis function:
    Return a pandas DataFrame with data of a given account
    """
    file_name = asignador_cuentas()
    data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    return data


def asignador_cuentas():
    """
    Non-user function:
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


def input_selector() -> tuple:
    """
    Non-user function:
    Intended to be only by operation_selector
    """
    category = input("\nCategoría: \n")
    subcategory = input("\nSubcategoría: \n")
    description = input("\nDescripción: \n")
    return category, subcategory, description


def operation_selector(operation: str) -> dict:
    """
    Non-user function:
    generates de columns that will be append into the account file
    """
    date = date_gen()["Fecha"]
    hour = date_gen()["hora"]
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
        subcategory = description = ""
    elif operation == "readjustment":
        total = input("\nIngrese el saldo actual\n")
        category = "Reajuste"
        subcategory = description = ""
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