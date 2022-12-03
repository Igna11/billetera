#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 14:01:51 2022

@author: igna
Core module of accounts and its operations
"""

import os
import re


class Accounts:
    """
    Superclass of AccountsCreator.
    Instantiates an Account Object. This object has information of the object,
    like name, currency, filename, column headers of the file, if the account
    exists or not, the amount of rows in the file and the get_last_line method
    to retrieve as attributes the values of the las line of the file.
    """

    def __init__(self, acc_name: str, acc_currency: str) -> None:
        self.acc_name = acc_name
        self.acc_currency = acc_currency.upper()
        self.acc_file_name = f"{acc_name}_ACC_{acc_currency.upper()}.txt"
        self.exists = self.acc_file_name in os.listdir()
        self.acc_data_len = 1
        self.acc_column_headers = [
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

    def __str__(self):
        """Information about the account."""
        return f"""
        \rName: {self.acc_name}
        \rCurrency: {self.acc_currency}
        \rFile Name: {self.acc_file_name}"""

    def __repr__(self):
        """returns the instantiation form of the object."""
        return f"Accounts({self.acc_name}, {self.acc_currency})"

    def get_last_line(self) -> dict:
        """
        Opens the account and set all values from the last line as attributes
        with their corresponding column name.
        """
        with open(self.acc_file_name, "r", encoding="UTF-8") as account:
            account_lines = account.read().splitlines()
        self.acc_data_len = len(account_lines)
        last_acc_line = account_lines[-1].split("\t")
        last_line_dict = dict(zip(self.acc_column_headers, last_acc_line))
        for key, val in last_line_dict.items():
            self.__setattr__(key, val)


class AccountsCreator(Accounts):
    """
    Subclass of Accounts.
    Inherits the necessary attributes of superclass Accounts to be usede as
    template to create or delete account files.
    """

    def add_account(self) -> None:
        """Creates the account file where all data will be stored as .txt file"""
        header = "\t".join(self.acc_column_headers) + "\n"
        with open(self.acc_file_name, "x", encoding="UTF-8") as account:
            account.write(header)

    def remove_account(self) -> None:
        """Deletes the account file. The information CAN NOT be recovered"""
        os.remove(self.acc_file_name)


class AccountParser:
    """Work in progress"""

    def __init__(self):
        """docstring pendiente"""
        self.pattern = r"([a-zA-Z0-9_]*)(_ACC_)([A-Z]*)"
        self.acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]
        self.acc_data_len = 1
        self.acc_dict = {}
        self.ars_total = 0.0
        self.usd_total = 0.0

    def acc_indexer(self):
        """
        Account selector in a numerical way: Associates a number to a given account
        so it can be selected by typing the number and not the name
        """
        acc_indexator = enumerate(self.acc_list, 1)
        self.acc_dict = dict(acc_indexator)
        return self.acc_dict

    def get_acc_properties(self):
        """docstring pendiente"""
        acc_index_dict = self.acc_indexer()
        for key, val in acc_index_dict.items():
            re_matches = re.match(self.pattern, val).groups()
            acc_name = re_matches[0]
            acc_currency = re_matches[2]
            acc_index_dict[key] = {
                "acc_name": acc_name,
                "currency": acc_currency,
            }
        return acc_index_dict

    def get_acc_total(self, account):
        """Returns the last line of the balance.txt file."""
        with open(account, "r", encoding="UTF-8") as acc:
            account_lines = acc.read().splitlines()
        self.acc_data_len = len(account_lines)
        headers = ["Hora", "Fecha", "Total", "Total(ARS)", "Total(USD)"]
        last_acc_line = account_lines[-1].split("\t")
        last_line_dict = dict(zip(headers, last_acc_line))
        return last_line_dict["Total"]

    def get_totals(self):
        """Sets the values for ars_total, usd_total."""
        for acc in self.acc_list:
            value = self.get_acc_total(acc)
            if "ARS" in acc and self.acc_data_len > 1:
                self.ars_total += float(value)
            elif "USD" in acc and self.acc_data_len > 1:
                self.usd_total += float(value)
