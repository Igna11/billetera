#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:24:19 2022

@author: igna
"""

import os

import pandas as pd

from source.misc import extra_char_cleaner
from source.ConversorClass import ConversorMoneda


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


def info(verbose=False):
    """List of functions, utilities and total balances"""
    functions = [
        "date_gen()",
        "precio_dolar()",
        "extra_char_cleaner()",
        "info()",
        "crear_usuario()",
        "iniciar_sesion()",
        "cerrar_sesion()",
        "crear_cuenta()",
        "lista_cuentas()",
        "datos_cuenta()",
        "asignador_cuentas()",
        "totales()",
        "input_selector()",
        "operation_selector()",
        "ingreso()",
        "extraccion()",
        "gasto()",
        "transferencia()",
        "reajuste()",
        "balances()<--NO USAR-ver help",
        "balance_graf()",
        "filtro()",
        "balances_cta()",
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
    info_msg = extra_char_cleaner(info_msg)

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