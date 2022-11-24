#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:03:06 2022

@author: igna
Modulo con funciones que realizan operaciones en cuentas

income()
expense()
extraction()
transfer()
readjustment()
"""

from source import info
from source import analysis
from source import account_core as account
from source import operations_core as operation


def account_selector() -> None:
    """Helping function to select the account when perfoming opreations"""
    accounts_info = account.AccountParser()
    acc_properties = accounts_info.get_acc_properties()
    for key, value in acc_properties.items():
        print(f"{key}: {value['acc_name']}({value['currency']})")
    while True:
        acc_number = int(input("\nElija la cuenta\n"))
        try:
            account_dict = acc_properties[acc_number]
            return account_dict
        except KeyError:
            print("=" * 79)
            print(
                f"\nValor elegido: '{acc_number}' erroneo, intente de nuevo."
            )
            print("Presione Ctrol+C para salir\n")
            print("=" * 79)


def income(
    value=None,
    acc_name=None,
    acc_currency=None,
    category=None,
    subcategory=None,
    description=None,
    test_mode=False,
) -> str:
    """Saves into the account file the income information."""
    if acc_name is None or acc_currency is None:
        account_dict = account_selector()
        acc_name = account_dict["acc_name"]
        acc_currency = account_dict["currency"]
    if value is None:
        value = float(input("\nCantidad de dinero a ingresar\n"))
    new_income = operation.Operations(acc_name, acc_currency, value)
    new_income.income_operation()
    if category is None:
        category = input("\nCategoría: \n")
    if subcategory is None:
        subcategory = input("\nSubcategoría: \n")
    if description is None:
        description = input("\nDescripción: \n")
    columns_dict = {
        "date": new_income.opdate,
        "hour": new_income.optime,
        "total": new_income.new_total,
        "income": new_income.new_income,
        "extraction": new_income.new_extraction,
        "expense": new_income.new_expense,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "balance": new_income.new_balance,
    }
    columns = list(columns_dict.values())
    new_row = "\t".join(columns) + "\n"
    if not test_mode:
        with open(new_income.acc_file_name, "a") as acc:
            acc.write(new_row)
        print(
            f"\nDinero en cuenta: ${float(new_income.new_total):.2f}\n"
            f"\nDinero total {info.totales()['total']:.2f}\n",
        )
        analysis.balances()
        return
    if test_mode:
        return new_row


def expense(
    value=None,
    acc_name=None,
    acc_currency=None,
    category=None,
    subcategory=None,
    description=None,
    test_mode=False,
) -> None:
    """Saves into the account file the expense information."""
    if acc_name is None or acc_currency is None:
        account_dict = account_selector()
        acc_name = account_dict["acc_name"]
        acc_currency = account_dict["currency"]
    if value is None:
        value = float(input("\nValor del gasto:\n"))
    new_expense = operation.Operations(acc_name, acc_currency, value)
    new_expense.expense_operation()
    if category is None:
        category = input("\nCategoría: \n")
    if subcategory is None:
        subcategory = input("\nSubcategoría: \n")
    if description is None:
        description = input("\nDescripción: \n")
    columns_dict = {
        "date": new_expense.opdate,
        "hour": new_expense.optime,
        "total": new_expense.new_total,
        "income": new_expense.new_income,
        "extraction": new_expense.new_extraction,
        "expense": new_expense.new_expense,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "balance": new_expense.new_balance,
    }
    columns = list(columns_dict.values())
    new_row = "\t".join(columns) + "\n"
    if not test_mode:
        with open(new_expense.acc_file_name, "a") as acc:
            acc.write(new_row)
        print(
            f"\nDinero en cuenta: ${float(new_expense.new_total):.2f}\n"
            f"\nDinero total {info.totales()['total']:.2f}\n",
        )
        analysis.balances()
        return
    if test_mode:
        return new_row


def extraction(
    value=None,
    acc_name=None,
    acc_currency=None,
    category=None,
    subcategory=None,
    description=None,
    test_mode=False,
) -> None:
    """Saves into the account file the extraction information."""
    if acc_name is None or acc_currency is None:
        account_dict = account_selector()
        acc_name = account_dict["acc_name"]
        acc_currency = account_dict["currency"]
    if value is None:
        value = float(input("\nCantidad de dinero a extraer\n"))
    new_extraction = operation.Operations(acc_name, acc_currency, value)
    new_extraction.expense_operation()
    if category is None:
        category = input("\nCategoría: \n")
    if subcategory is None:
        subcategory = input("\nSubcategoría: \n")
    if description is None:
        description = input("\nDescripción: \n")
    columns_dict = {
        "date": new_extraction.opdate,
        "hour": new_extraction.optime,
        "total": new_extraction.new_total,
        "income": new_extraction.new_income,
        "extraction": new_extraction.new_extraction,
        "expense": new_extraction.new_expense,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "balance": new_extraction.new_balance,
    }
    columns = list(columns_dict.values())
    new_row = "\t".join(columns) + "\n"
    if not test_mode:
        with open(new_extraction.acc_file_name, "a") as acc:
            acc.write(new_row)
        print(
            f"\nDinero en cuenta: ${float(new_extraction.new_total):.2f}\n"
            f"\nDinero total {info.totales()['total']:.2f}\n",
        )
        analysis.balances()
        return
    if test_mode:
        return new_row


def transfer(
    value=None,
    origin_acc=None,
    origin_currency=None,
    dest_acc=None,
    dest_currency=None,
    test_mode=False,
) -> None:
    """Saves into the account file the extraction information."""
    if origin_acc is None or origin_currency is None:
        origin_account = account_selector()
        origin_acc = origin_account["acc_name"]
        origin_currency = origin_account["currency"]
    if dest_acc is None or dest_currency is None:
        dest_account = account_selector()
        dest_acc = dest_account["acc_name"]
        dest_currency = dest_account["currency"]
    if value is None:
        value = float(input("\nCantidad de dinero a transferir\n"))
    new_transfer = operation.Operations(origin_acc, origin_currency, value)
    dest_new_transfer = new_transfer.transfer_operation(
        dest_acc, dest_currency
    )
    category = "Transferencia"
    origin_subcategory = "Tranferencia de salida"
    dest_subcategory = "Transferencia de entrada"
    origin_description = f"Transferencia a {dest_acc}"
    dest_description = f"Transferencia de {origin_acc}"
    origin_columns_dict = {
        "date": new_transfer.opdate,
        "hour": new_transfer.optime,
        "total": new_transfer.new_total,
        "income": new_transfer.new_income,
        "extraction": new_transfer.new_extraction,
        "expense": new_transfer.new_expense,
        "category": category,
        "subcategory": origin_subcategory,
        "description": origin_description,
        "balance": new_transfer.new_balance,
    }
    dest_columns_dict = {
        "date": new_transfer.opdate,
        "hour": new_transfer.optime,
        "total": dest_new_transfer.Total,
        "income": dest_new_transfer.income,
        "extraction": "0.00",
        "expense": "0.00",
        "category": category,
        "subcategory": dest_subcategory,
        "description": dest_description,
        "balance": new_transfer.new_balance,
    }
    origin_columns = list(origin_columns_dict.values())
    origin_new_row = "\t".join(origin_columns) + "\n"
    dest_columns = list(dest_columns_dict.values())
    dest_new_row = "\t".join(dest_columns) + "\n"
    if not test_mode:
        with open(new_transfer.acc_file_name, "a") as acc:
            acc.write(origin_new_row)
        with open(dest_new_transfer.acc_file_name, "a") as acc:
            acc.write(dest_new_row)
        print(
            f"\nOrigen: Dinero en {origin_acc}: ${float(new_transfer.new_total):.2f}\n",
            f"\nDestino: Dinero en {dest_acc}: ${float(dest_new_transfer.Total):.2f}\n",
        )
        return
    if test_mode:
        return origin_new_row, dest_new_row


def readjustment(
    value=None, acc_name=None, acc_currency=None, test_mode=False
) -> None:
    """Saves into the account file the readjustment information."""
    if acc_name is None or acc_currency is None:
        account_dict = account_selector()
        acc_name = account_dict["acc_name"]
        acc_currency = account_dict["currency"]
    if value is None:
        value = float(input("\nIngrese saldo actual\n"))
    category = "Reajuste"
    new_readjustment = operation.Operations(acc_name, acc_currency, value)
    new_readjustment.readjustment_operation()

    if value < float(new_readjustment.Total):
        subcategory = "Negativo"
        description = "Reajuste negativo de saldo"
    if value > float(new_readjustment.Total):
        subcategory = "Positivo"
        description = "Reajuste positivo de saldo"
    columns_dict = {
        "date": new_readjustment.opdate,
        "hour": new_readjustment.optime,
        "total": new_readjustment.new_total,
        "income": new_readjustment.new_income,
        "extraction": new_readjustment.new_extraction,
        "expense": new_readjustment.new_expense,
        "category": category,
        "subcategory": subcategory,
        "description": description,
        "balance": new_readjustment.new_balance,
    }
    columns = list(columns_dict.values())
    new_row = "\t".join(columns) + "\n"
    if not test_mode:
        with open(new_readjustment.acc_file_name, "a") as acc:
            acc.write(new_row)
        print(
            f"\nDinero en cuenta: ${float(new_readjustment.new_total):.2f}\n"
            f"\nDinero total {info.totales()['total']:.2f}\n",
        )
        analysis.balances()
        return
    if test_mode:
        return new_row
