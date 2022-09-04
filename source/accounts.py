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

import os

import pandas as pd

from source.misc import extra_char_cleaner
from source.misc import date_gen
from source.info import lista_cuentas


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
    acc_name = extra_char_cleaner(file_name)
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
        acc_name = extra_char_cleaner(file_name)
        print(f"\nSe eliminó la cuenta {acc_name}\n")
    else:
        acc_name = extra_char_cleaner(file_name)
        print(f"\nNo se eliminó la cuenta {acc_name}\n")



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
        acc_str = extra_char_cleaner(acc)
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