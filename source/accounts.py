#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sept 03 20:01:51 2022

@author: igna
Modulo para condensar las funciones que tienen las cuentas

crear_cuenta()
eliminar_cuenta()

TODO no poder crear cuentas, ni borrar cuentas si no hay sesión iniciada
"""

from source.account_core import AccountsCreator


def crear_cuenta():
    """Creates a .txt file which name will be the account name"""
    name_acc = input("\nIntroduzca el nombre para la nueva cuenta\n")
    currency_acc = input(
        "\nIngresar el tipo de moneda, por ejemplo: ARS, USD, etc\n"
    ).upper()
    account = AccountsCreator(acc_name=name_acc, acc_currency=currency_acc)
    account.add_account()
    print(f"\nSe ha creado la cuenta '{name_acc}'\n")


def eliminar_cuenta():
    """Deletes the .txt file of the given account name"""
    name_acc = input("\nIntroduzca el nombre de la cuenta a eliminar\n")
    currency_acc = input(
        "\nIntroduzca el tipo de moneda usada en la cuenta (ARS, USD, etc)\n"
    ).upper()
    account = AccountsCreator(acc_name=name_acc, acc_currency=currency_acc)
    if account.exists:
        warning = "¿Seguro que queres eliminar la cuenta?\n\n\
        todos los datos contenidos en ella se perderán para siempre.\n\n\
        Ingrese '1', 'si' o 'y' para borrar\n\
        Ingrese cualquier otra cosa para cancelar\n"
        user_answer = input(warning)
        possible_answers = ["1", "si", "y"]
        if user_answer in possible_answers:
            account.remove_account()
            print(f"\nSe eliminó la cuenta '{name_acc}'\n")
        else:
            print(f"\nNo se eliminó la cuenta '{name_acc}'\n")
    else:
        print(f"\nNo existe la cuenta '{name_acc}'\n")
