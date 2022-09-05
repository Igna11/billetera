#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:06:08 2022

@author: igna
"""

import os
from datetime import datetime


def date_gen():
    """
    Non-user function:
    Generates a dictionary with date an time in a latin-format: d-m-y
    """
    time = datetime.now()
    date = time.strftime("%d-%m-%Y")
    hour = time.strftime("%H:%M:%S")
    return {"Fecha": date, "hora": hour}


def extra_char_cleaner(charchain: str):
    """
    Non-user function:
    Strips all chars from the account string name except of its name
    returns the name cleaned
    """
    charchain = (
        charchain.replace("CUENTA", "")
        .replace("_DOL", "")
        .replace(".txt", "")
        .replace("USR", "")
    )
    return charchain


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
