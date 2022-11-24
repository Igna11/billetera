#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:06:08 2022

@author: igna
"""

import os
from datetime import datetime


def extra_char_cleaner(charchain: str):
    """
    Non-user function:
    Strips all chars from the account string name except of its name
    returns the name cleaned
    """
    charchain = (
        charchain.replace("_ACC", "")
        .replace("_ARS", "")
        .replace("_USD", "")
        .replace(".txt", "")
        .replace("USR", "")
    )
    return charchain


def users_list():
    """
    Non-user function:
    Lists all users found inside the main directory
    """
    file_list = os.listdir()
    user_list = []
    for dirfile in file_list:
        if "USR" in dirfile:
            user_list.append(dirfile)
    return user_list


def asignador_cuentas():
    """
    Non-user function:
    Account selector in a numerical way: Associates a number to a given account
    so it can be selected by typing the number and not the name
    """
    acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]
    acc_range = range(1, len(acc_list) + 1)
    dic = dict(zip(acc_range, acc_list))
    account_index = ""
    for i, acc in enumerate(acc_list):
        # defino una variable sin sufijos para printear
        acc_str = extra_char_cleaner(acc)
        # actualizo el string final que se imprime en consola
        account_index += str(i + 1) + ": " + acc_str + "\n"
    # Meto un input de teclado
    while True:
        acc_number = int(input("\nElija la cuenta\n" + account_index + "\n"))
        try:
            acc_name = dic[acc_number]
            print(extra_char_cleaner(acc_name))
            return acc_name
        except KeyError:
            print("=" * 79)
            print(
                f"\nValor elegido: '{acc_number}' erroneo, intente de nuevo."
            )
            print("Presione Ctrol+C para salir\n")
            print("=" * 79)
