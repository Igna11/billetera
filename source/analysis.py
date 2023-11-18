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

from source import errors


def account_data(acc_name: str, acc_currency: str) -> pd.DataFrame:
    """
    Analysis function:
    Return a pandas DataFrame with data of a given account
    """
    acc_file_name = f"{acc_name}_ACC_{acc_currency.upper()}.csv"
    data = pd.read_csv(acc_file_name, sep="\t", encoding="latin1")
    return data


def account_balances(account: str, month: int, year: int):
    """
    Analysis function:
    Easy way to get the monthly balance of a given account: Incomes, expenses
    and balance: income - expenses
    Inputs:
        account: str
        Acccount name as file or path, ej: MercadoPagoCUENTA.csv
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


def total_balances(month: int, year: int, verbose=False):
    """
    Analysis function:
    Easy way to see the total balance of the sum all over the accounts, given
    a month and a year:  Total incomes, total expenses and total balances.
    It uses balances()
    Inputs:
        month: int
        Month number to check balance: Valid values from 1 to 12
        year: int
        Year number to check balance: Valid values 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por usuario: float
    """
    total_incomes = total_expenses = total_balance = 0
    for acc in os.listdir():
        if "_ACC_" in acc and "_USD" not in acc:
            try:
                balances_dict = account_balances(acc, month, year)
            except AttributeError as error:
                if verbose is True:
                    print("Error en la cuenta: ", acc)
                    print(error)
            total_incomes += balances_dict["Ingresos_m"]
            total_expenses += balances_dict["Gasto_m"]
            total_balance += balances_dict["Balance_m"]

    return {
        "total_incomes": round(total_incomes, 2),
        "total_expenses": round(total_expenses, 2),
        "total_balances": round(total_balance, 2),
    }


def balance_graf():
    """
    Makes a plot with all data from the balance file. It includes:
        Total amount,
        Total pesos only,
        Total dollars only,
    """
    data = pd.read_csv("Balance.csv", sep="\t")
    # Armo un string con la fecha y la hora en el formato del .csv
    str_time = data["Date"] + "-" + data["Time"]
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
        label=f"Total: ${data['Total'].values[-1]:.2f}",
    )
    plt.plot(
        time,
        data["Total(ARS)"],
        "o-",
        alpha=0.5,
        fillstyle="none",
        markersize=3,
        label=f"Total de pesos: {data['Total(ARS)'].values[-1]:.2f}",
    )
    plt.plot(
        time,
        data["Total(USD)"],
        "-",
        alpha=0.5,
        fillstyle="none",
        label=f"Total de dolares: u$s{data['Total(USD)'].values[-1]:.2f}",
    )
    plt.grid(which="both", alpha=0.5)
    plt.legend()
    plt.xticks(rotation=25)
    plt.show()


def data_filter(acc_name: str, acc_currency: str) -> pd.DataFrame:
    """
    Analysis function:
    Easy way to filter data from a given account by category and subcategory
    """
    acc_file_name = f"{acc_name}_ACC_{acc_currency.upper()}.csv"
    data = pd.read_csv(acc_file_name, sep="\t", encoding="latin1")
    categoria = input("\nIngrese la categoría\n")
    data = data[data["Categoria"] == categoria]
    print(data)
    user_answer = input("\n\nSeguir filtrando?\n\nsi/no\n\n")
    if user_answer == "si":
        subcategory = input("\nIngrese la subcategoría\n")
        data = data[data["Subcategoria"] == subcategory]
        return data
    return data


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
    acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]
    for account in acc_list:
        if "USD" not in account:
            df_data = pd.read_csv(
                account,
                sep="\t",
                index_col=("Fecha"),
                parse_dates=True,
                dayfirst=True,
                encoding="latin1",
            )
            df_data["Account"] = account

            if not subcat:
                df_ = df_data[df_data["Categoria"] == cat]
            elif subcat:
                df_ = df_data[
                    (df_data["Categoria"] == cat) & (df_data["Subcategoria"] == subcat)
                ]

            if len(df_):
                df_final = pd.concat([df_final, df_])
    return df_final.sort_index()


def monthly_categorical_spendings(month: int, year: int, cat: str, subcat="", desc=""):
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


class DataAnalyzer:
    """
    Class with several analysis methods to get insights of the data and get
    value from it.
    Loads data from all accounts of the user, including all different currencies
    """

    def __init__(self):
        """Get the list of accounts and its currencies"""
        self.acc_list = [acc for acc in os.listdir() if "ACC" in acc]
        if not self.acc_list:
            raise errors.UserHasNotAccountsError
        self.acc_currencies = set(acc.strip(".csv")[-3:] for acc in self.acc_list)
        # Loading data
        df_list = []
        for acc in self.acc_list:
            df_raw = pd.read_csv(acc, sep="\t")
            df_raw["account"] = acc.replace(".csv", "").replace("_ACC", "")
            df_list.append(df_raw)
        self.main_df = pd.concat(df_list, axis=0, ignore_index=True)
        # add a column with datetime type to the dataframe
        self.main_df["datetime"] = pd.to_datetime(
            self.main_df["Fecha"] + " " + self.main_df["hora"],
            format="%d-%m-%Y %H:%M:%S",
        )
        # drop of unnecesary columns
        self.main_df.drop(columns=["Fecha", "hora", "Balance"], inplace=True)
        # sort data by datetime
        self.main_df.sort_values(by="datetime", inplace=True)

    def get_data_per_currency(self, currency):
        """Generates a new dataframe containing only the desired type of currency"""
        mask = self.main_df["account"].str.upper().str.contains(currency)
        self.main_df = self.main_df[mask]

    def monthly_mask(self, month: int, year: int, operation: str) -> pd.DataFrame:
        """
        Creates the mask that will be used by:
        get_month_incomes_by_category, get_month_incomes_by_subcategory,
        get_month_expenses_by_category, get_month_expenses_by_subcategory
        """
        mask = (
            (self.main_df["datetime"].dt.month == month)
            & (self.main_df["datetime"].dt.year == year)
            & (self.main_df["Categoria"] != "Transferencia")
            & (self.main_df[operation] != 0)
        )
        return mask

    def period_mask(
        self, initial_time: datetime, final_time: datetime, operation: str
    ) -> pd.DataFrame:
        """
        Creates the mask that will be used by:
        get_period_expenses_by_category, get_period_expenses_by_subcategory,
        get_period_incomes_by_category, get_period_incomes_by_subcategory
        """
        mask = (
            self.main_df["datetime"].between(initial_time, final_time)
            & (self.main_df["Categoria"] != "Transferencia")
            & (self.main_df[operation] != 0)
        )
        return mask

    # data of a given arbitrary period of time
    def get_period_operations(self, initial_datetime: datetime, final_datetime: datetime, operation: str, type: str):
        """
        Returns a dataframe with the incomes or expenses in every category and/or subcategory
        for a given custom period of time
        """
        mask = self.period_mask(initial_datetime, final_datetime, operation)
        filtered_df = self.main_df[mask].copy()
        if type == "category":
            return filtered_df.groupby(["Categoria"])[operation].sum()
        elif type == "subcategory":
            return filtered_df.groupby(["Categoria", "Subcategoria"])[operation].sum()
        
    # data of a given month and year
    def get_monthly_operations(self, month: int, year: int, operation:str, type:str) -> pd.DataFrame:
        """
        Returns a dataframe with the incomes or expenses in every category and/or subcategory
        for a given month and year.
        """
        mask = self.monthly_mask(month, year, operation)
        filtered_df = self.main_df[mask].copy()
        if type=="category":
            return filtered_df.groupby(["Categoria"])[operation].sum()
        elif type=="subcategory":
            return filtered_df.groupby(["Categoria", "Subcategoria"])[operation].sum()