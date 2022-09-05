#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:04:41 2022

@author: igna

Modulo para funciones que realizan analisis de los datos

datos_cuenta()
balances()
balances_cta()
balances_totales()
balance_graf()
filtro()
category_spendings()
monthlycategorical_spendings
"""
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from source.misc import date_gen
from source.misc import lista_cuentas
from source.misc import asignador_cuentas
from source.misc import extra_char_cleaner
from source.info import totales


def datos_cuenta():
    """
    Analysis function:
    Return a pandas DataFrame with data of a given account
    """
    file_name = asignador_cuentas()
    data = pd.read_csv(file_name, sep="\t", encoding="latin1")
    return data


def balances():
    """
    Non-user function:
    Appends one row to the balance file everytime an account operation that
    modifies the balance is done.
    If the balance file exists, appends data. If the balance file does not
    exists, it creates it and appends the data.
    --------------------------------------------------------------------------
    Do not use this function manually, it is only intended to be used by other
    functions.
    """
    total, total_pesos, total_dolares = list(totales().values())
    fecha = date_gen()["Fecha"]
    hora = date_gen()["hora"]
    if not os.path.isfile("Balance.txt"):
        with open("Balance.txt", "x") as balance:
            balance.write("Hora\tFecha\tTotal\tTotal_pesos\tTotal_dolares\n")
            balance.write(
                f"{hora}\t{fecha}\t{total}\t{total_pesos}\t{total_dolares}\n"
            )
    elif os.path.isfile("Balance.txt"):
        with open("Balance.txt", "a") as balance:
            balance.write(
                f"{hora}\t{fecha}\t{total}\t{total_pesos}\t{total_dolares}\n"
            )


def balances_cta(account: str, month: int, year: int):
    """
    Analysis function:
    Easy way to get the monthly balance of a given account: Incomes, expenses
    and balance: income - expenses
    Inputs:
        account: str
        Acccount name as file or path, ej: MercadoPagoCUENTA.txt
        month: int
        Month number to check balance: Valids from 1 to 12
        year: int
        Year numberto check balance: Valids 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por cuenta: float
    """
    df_data = pd.read_csv(
        account,
        sep="\t",
        index_col=("Fecha"),
        parse_dates=True,
        dayfirst=True,
        encoding="latin1",
    )
    monthly_src = df_data[
        (df_data.index.month == month)
        & (df_data.index.year == year)
        & (df_data["Categoria"] != "Transferencia")
    ]
    monthly_spend = monthly_src["Gasto"].sum()
    monthly_spend += monthly_src["Extracciones"].astype("float32").sum()
    monthly_earn = monthly_src["Ingresos"].astype("float32").sum()
    balance = monthly_earn - monthly_spend

    return {
        "Ingresos_m": round(monthly_earn, 2),
        "Gasto_m": round(monthly_spend, 2),
        "Balance_m": round(balance, 2),
    }


def balances_totales(month: int, year: int, verbose=False):
    """
    Analysis function:
    Easy way to see the total balance of the sum all over the accounts, given
    a month and a year:  Total incomes, total expenses and total balances.
    It uses balances()
    Inputs:
        month: int
        Month number to check balance: Valids from 1 to 12
        year: int
        Year numberto check balance: Valids 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por usuario: float
    """
    ingresos_tot = gastos_tot = balances_tot = 0
    for cuenta in os.listdir():
        if "CUENTA" in cuenta and "DOL" not in cuenta:
            try:
                dic_c = balances_cta(cuenta, month, year)
            except AttributeError as error:
                if verbose is True:
                    print("Error en la cuenta: ", cuenta)
                    print(error)
            ingresos_tot += dic_c["Ingresos_m"]
            gastos_tot += dic_c["Gasto_m"]
            balances_tot += dic_c["Balance_m"]

    return {
        "Ingresos_tot": round(ingresos_tot, 2),
        "Gasto_tot": round(gastos_tot, 2),
        "Balance_tot": round(balances_tot, 2),
    }


def balance_graf():
    """
    Makes a plot with all data from the balance file. It includes:
        Total amount,
        Total pesos only,
        Total dollars only,
    """
    data = pd.read_csv("Balance.txt", sep="\t")
    # Armo un string con la fecha y la hora en el formato del .txt
    str_time = data["Fecha"] + "-" + data["Hora"]
    # Especifico ese formato acá, para usarlo en la funcion strptime
    formato = "%d-%m-%Y-%H:%M:%S"
    # transformo el string a un objeto datetime usando el formato dado
    time = [datetime.strptime(i, formato) for i in str_time]
    plt.plot(
        time,
        data["Total"],
        "o-",
        alpha=0.5,
        fillstyle="full",
        markersize=5,
        label="Total: $%.2f" % data["Total"].values[-1],
    )
    plt.plot(
        time,
        data["Total_pesos"],
        "o-",
        alpha=0.5,
        fillstyle="none",
        markersize=3,
        label="Total de pesos: $%.2f" % data["Total_pesos"].values[-1],
    )
    plt.plot(
        time,
        data["Total_dolares"],
        "-",
        alpha=0.5,
        fillstyle="none",
        label="Total de dolares: u$s%.2f" % data["Total_dolares"].values[-1],
    )
    plt.grid(which="both", alpha=0.5)
    plt.legend()
    plt.xticks(rotation=25)
    plt.show()


def filtro():
    """
    Analysis function:
    Easy way to filter data from a given account by category and subcategory
    """
    nombre = asignador_cuentas()
    # Abre y lee los datos de la cuenta
    datos = pd.read_csv(nombre, sep="\t", encoding="latin1")
    categoria = input("\nIngrese la categoría\n")
    datos = datos[datos["Categoria"] == categoria]
    print(datos)
    respuesta = input("\n\nSeguir filtrando?\n\nsi/no\n\n")
    if respuesta == "si":
        subcategoria = input("\nIngrese la subcategoría\n")
        datos = datos[datos["Subcategoria"] == subcategoria]
        return datos
    return datos


def category_spendings(cat: str, subcat="", desc=""):
    """
    Analysis function:
    Easy way to filter all entries with the same category and subcategory from
    all accounts.
        For future implementations: A filter that checks in the description of
        the entry for a match word or phrase.
    Parameters
    ----------
    cat : str
        Category
    subcat : TYPE, optional
        Subcategory. The default is "".
    desc : TYPE, optional
        NOT IMPLEMENTED.

    Returns
    -------
    Pandas DataFrame Object.
        the DataFrame of the filtered information
    """
    df_final = pd.DataFrame()
    for account in lista_cuentas():
        if "DOL" not in account:
            df_data = pd.read_csv(
                account,
                sep="\t",
                index_col=("Fecha"),
                parse_dates=True,
                dayfirst=True,
                encoding="latin1",
            )
            df_data["Account"] = extra_char_cleaner(account)

            if not subcat:
                df_ = df_data[df_data["Categoria"] == cat]
            elif subcat:
                df_ = df_data[
                    (df_data["Categoria"] == cat)
                    & (df_data["Subcategoria"] == subcat)
                ]

            if len(df_):
                df_final = pd.concat([df_final, df_])
    return df_final.sort_index()


def monthly_categorical_spendings(
    month: int, year: int, cat: str, subcat="", desc=""
):
    """
    Analysis function:
        Easy way to get the total expenses for a given category and/or subcat.
        for all accounts in a given month.
    Parameters
    ----------
    month : int
        Month
    year : int
        Year
    cat : str
        Categry
    subcat : TYPE, optional
        Subcategory. The default is "".
    desc : TYPE, optional
        NOT IMPLEMENTED.

    Returns
    -------
    float
        The total expenses of that category.
    """
    df = category_spendings(cat=cat, subcat=subcat, desc=desc)
    total = df[(df.index.month == month) & (df.index.year == year)].Gasto.sum()
    return round(total, 2)
