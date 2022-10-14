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

import os

from source.misc import asignador_cuentas
from source.misc import extra_char_cleaner


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
        return
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
