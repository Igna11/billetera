#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:03:06 2022

@author: igna
Modulo con funciones que realizan operaciones en cuentas

account_checker() <- decorator
ingreso()
extraccion()
gasto()
transferencia()
reajuste()
"""
import os

import pandas as pd

from source.misc import extra_char_cleaner, lista_cuentas
from source.misc import asignador_cuentas
from source.misc import operation_selector

from source.analysis import balances
from source.analysis import totales


def account_checker(func):
    """
    Decorator function: Checks if there is existing accounts and if not it
    bypasses the function.
    """

    def decorator():
        if len(lista_cuentas()) != 0:
            func()
        else:
            print("No existen cuentas.")

    return decorator


@account_checker
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
    columns = operation_selector(operation="income")
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
        f"\nDinero en cuenta: ${new_total:.2f}\n",
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()


@account_checker
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
    columns = operation_selector("extraction")
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


@account_checker
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
    columns = operation_selector("expense")
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


@account_checker
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
    acc_name_out = extra_char_cleaner(file_name_out)
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
    # Check the same type of account
    if (
        "_DOL" in file_name_out
        and "_DOL" not in file_name_in
        or "_DOl" not in file_name_out
        and "_DOL" in file_name_in
    ):
        return print(
            "Solo se pueden realizar transferencias entre el mismo tipo de cuentas:",
            " Pesos-Pesos o Dolar-Dolar",
        )
    acc_name_in = extra_char_cleaner(file_name_in)
    acc_data_in = pd.read_csv(file_name_in, sep="\t", encoding="latin1")
    try:
        last_total_in = acc_data_in["Total"].values[-1]
    except IndexError:
        last_total_in = 0.0

    # Transfers with the same account are not allowed
    if file_name_in == file_name_out:
        return print("\nNo tiene sentido transferir a una misma cuenta!!\n")

    # Format all de columns correctly
    columns_in = operation_selector(operation="transfer")
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


@account_checker
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
    file_name = asignador_cuentas()
    acc_name = extra_char_cleaner(file_name)
    acc_data = pd.read_csv(file_name, sep="\t", encoding="latin1")["Total"]
    # If empty account, then do nothing
    if len(acc_data) == 0:
        return print(f"\nNo hay datos en la cuenta {acc_name}\n")
    last_total = acc_data.values[-1]
    columns = operation_selector(operation="readjustment")
    new_total = float(columns["total"])
    # Negative values not allowed
    if new_total < 0:
        return print("\nNo se puede reajustar a valores negativos!\n")
    # No readjustment
    if last_total == new_total:
        return print("\nNo hay nada que reajustar.\n")
    # Positive readjustment
    if last_total < new_total:
        columns["subcategory"] = "Positivo"
        columns["description"] = "Reajuste positivo de saldo"
        income = new_total - last_total
        columns["income"] = f"{income:.2f}"
    # Negative readjustment
    elif last_total > new_total:
        columns["subcategory"] = "Negativo"
        columns["description"] = "Reajuste negativo de saldo"
        extraction = last_total - new_total
        columns["extraction"] = f"{extraction:.2f}"
    # Redefine columns from dict to list
    columns = list(columns.values())
    # Escribo la fila que se va a appendear al archivo
    row = "\t".join(columns) + "\n"
    # La appendeo al archivo
    with open(file_name, "a") as myaccount:
        myaccount.write(row)
    print(
        f"\nDinero en cuenta: ${new_total:.2f}",
        f"\nDinero total {totales()['total']:.2f}\n",
    )
    balances()
