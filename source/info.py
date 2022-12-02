#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:24:19 2022

@author: igna
"""

import os
import pandas as pd

from source import account_core as account
from source.currency import ConversorMoneda


def precio_dolar(verbose=False):
    """
    Gets the current dollar price by scrapping from web or inferring it from
    previuos data from Balances.txt
    """
    # Creo el objeto que maneja la consulta y me devuelve el precio
    exchange = ConversorMoneda(verbose=verbose)
    try:
        # Trato de conseguir el precio de internet, si no, handleo el error
        usd_val = exchange.precio()["Dolar U.S.A"]["Compra"]
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
        tot_pesos = bal_datos["Total(ARS)"].values[-1]
        tot_dolares = bal_datos["Total(USD)"].values[-1]
        try:
            usd_val = str(round((tot_dinero - tot_pesos) / tot_dolares, 2))
        except ZeroDivisionError:
            print("No hay dolares, asi que no importa cuanto vale")
            usd_val = "0.00"

    return float(usd_val.replace(",", "."))


def totales():
    """
    Non-user function:
    Calculate the total amount of money for all accounts
    """
    acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]
    usd_val = precio_dolar()
    total = 0
    ars_total = 0
    usd_total = 0
    for acc in acc_list:
        df_data = pd.read_csv(acc, sep="\t", encoding="latin1")
        try:
            valor_elem = float(df_data["Total"].values[-1])
            if "USD" in acc:
                usd_total += valor_elem
                total += valor_elem * usd_val
            else:
                ars_total += valor_elem
                total += valor_elem
        except IndexError:
            pass
    total = round(total, 2)
    ars_total = round(ars_total, 2)
    usd_total = round(usd_total, 2)
    dic = {"total": total, "total(ARS)": ars_total, "total(USD)": usd_total}
    return dic


def info(verbose=False):
    """List of functions."""
    functions = [
        "info()",
        "precio_dolar()",
        "crear_usuario()",
        "iniciar_sesion()",
        "cerrar_sesion()",
        "crear_cuenta()",
        "datos_cuenta()",
        "ingreso()",
        "gasto()",
        "extraccion()",
        "transferencia()",
        "reajuste()",
        "filtro()",
        "balance_graf()",
        "balances_cta()",
        "balances_totales()",
        "category_spendings",
    ]
    # lista con los nombres de los archivos de cuenta
    accounts_data = account.AccountParser()
    usd_val = precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = []
    for acc in accounts_data.acc_list:
        acc_total = pd.read_csv(acc, sep="\t", encoding="latin1")["Total"]
        # Si la cuenta tiene datos, appendeo el valor
        if len(acc_total) != 0:
            total.append(acc_total.values[-1])
        # Si la cuenta es nueva y no tiene datos, appendeo 0
        else:
            total.append(0)
    # Parrafo con los datos de todas las cuentas
    info_msg = ""
    for i, elem in enumerate(accounts_data.acc_list):
        if "_USD" in elem:
            dolar_tot = total[i]
            pesos_tot = total[i] * usd_val
            info_msg += f"\n{elem}: Saldo u$s {dolar_tot:.2f} (USD), "
            info_msg += f"(${pesos_tot:.2f} ARS)"
        else:
            info_msg += f"\n{elem}: $ {total[i]:.2f} (ARS)"
    # Limpio los strings que molestan
    info_msg = (
        info_msg.replace(".txt", "")
        .replace("_ACC", "")
        .replace("_USD", "")
        .replace("_ARS", "")
    )

    # Calculo todos los totales

    totals_dict = totales()
    # Printeo toda la información
    str_functions = "\n".join(functions)
    if verbose:
        print("Funciones:\n", str_functions)
    print("=" * 79)
    print("Cuentas existentes:\n", info_msg)
    print("=" * 79)
    print(f"Dolares totales: ${totals_dict['total(USD)']:.2f}")
    print("=" * 79)
    print(f"Pesos totales: ${totals_dict['total(ARS)']:.2f}")
    print("=" * 79)
    print(f"Dinero total en cuentas: ${totals_dict['total']:.2f}")
    print("=" * 79)
