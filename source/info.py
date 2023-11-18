#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:24:19 2022

@author: igna

"""

from source import account_core as account
from source import colorizer as color
from source import currency


def precio_dolar(verbose=False):
    """
    Gets the current dollar price by scrapping from web or inferring it from
    previuos data from Balances.csv
    """
    exchange = currency.currencies_values()
    try:
        usd_value = exchange["Dolar U.S.A"]["Compra"]
    except TypeError as error:
        if verbose is True:
            print("Ocurrio el siguiente error durante la consulta:")
            print(error)
            print("Seguramente se debe a un error urlopen y no de Attribute")
        color.cprint(
            "No se pudo obtener el precio del dolar de internet, se usará la última cotización.",
            "red",
        )
        # Como no pude conseguir el precio de internet, lo infiero de el último
        # balance en la cuenta Balance.csv
        with open("Balance.csv", "r", encoding="UTF-8") as balance_file:
            file_lines = balance_file.read().splitlines()
        headers = file_lines[0].split("\t")
        last_line = file_lines[-1].split("\t")
        balance_data = dict(zip(headers, last_line))
        total = float(balance_data["Total"])
        ars_total = float(balance_data["Total(ARS)"])
        usd_total = float(balance_data["Total(USD)"])
        try:
            usd_value = str(round((total - ars_total) / usd_total, 2))
            color.cprint(f"Última cotización: 1 u$d = $ {usd_value}\n", "green", "bold")
        except ZeroDivisionError:
            print("No hay dolares, asi que no importa cuanto vale")
            usd_value = "0.00"

    return float(usd_value.replace(",", "."))


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
        acc_total = accounts_data.get_acc_total(acc)
        if acc_total == "Total":
            total.append(0)
        elif float(acc_total) >= 0:
            total.append(float(acc_total))
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
        info_msg.replace(".csv", "")
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
        color.cprint(f"Funciones:\n {str_functions}", "blue", "bold")
    color.cprint("=" * 79, "grey", "bold")
    color.cprint(f"Cuentas existentes:\n{info_msg}", "purple", "bold")
    color.cprint("=" * 79, "grey", "bold")
    color.cprint(f"Dolares totales: ${usd_total:.2f}", "green")
    color.cprint("=" * 79, "grey", "bold")
    color.cprint(f"Pesos totales: ${ars_total:.2f}", "cyan")
    color.cprint("=" * 79, "grey", "bold")
    color.cprint(f"Dinero total en cuentas: ${total:.2f}", "blue", "bold")
    color.cprint("=" * 79, "grey", "bold")
