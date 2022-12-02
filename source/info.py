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


def info(verbose=False):
    """List of functions."""
    functions = [
        "info()",
        "precio_dolar()",
        "crear_usuario()",
        "eliminar_usuario()",
        "cambiar_password()",
        "iniciar_sesion()",
        "cerrar_sesion()",
        "crear_cuenta()",
        "eliminar_cuenta()",
        "ingreso()",
        "gasto()",
        "extraccion()",
        "transferencia()",
        "reajuste()",
        "datos_cuenta()",
        "filtro()",
        "balances_cta()",
        "balances_totales()",
        "category_spendings",
        "balance_graf()",
    ]
    # lista con los nombres de los archivos de cuenta
    accounts_data = account.AccountParser()
    usd_value = precio_dolar()
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
            pesos_tot = total[i] * usd_value
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
    accounts_data.get_totals()
    total = accounts_data.ars_total + accounts_data.usd_total * usd_value
    ars_total = accounts_data.ars_total
    usd_total = accounts_data.usd_total
    # Printeo toda la información
    str_functions = "\n".join(functions)
    if verbose:
        print("Funciones:\n", str_functions)
    print("=" * 79)
    print("Cuentas existentes:\n", info_msg)
    print("=" * 79)
    print(f"Dolares totales: ${usd_total:.2f}")
    print("=" * 79)
    print(f"Pesos totales: ${ars_total:.2f}")
    print("=" * 79)
    print(f"Dinero total en cuentas: ${total:.2f}")
    print("=" * 79)
