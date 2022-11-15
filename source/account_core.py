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
    """Esto es un docstring para pylint"""

    def __init__(self, acc_name: str, acc_currency: str) -> None:
        self.acc_file_name = f"{acc_name}_ACC_{acc_currency}.txt"
        self.exists = self.acc_file_name in os.listdir()
        self.acc_columns = [
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

    def get_last_line(self) -> dict:
        """docstring"""
        with open(self.acc_file_name, "r") as account:
            self.account_raw = account.read()
        last_acc_line = self.account_raw.splitlines()[-1].split("\t")
        last_line_dict = dict(zip(self.acc_columns, last_acc_line))
        for key, val in last_line_dict.items():
            self.__setattr__(key, val)

    def add_account(self) -> None:
        """Otro docstring"""
        header = "\t".join(self.acc_columns) + "\n"
        with open(self.acc_file_name, "x") as account:
            account.write(header)

    def remove_account(self) -> None:
        """Otro docstring"""
        os.remove(self.acc_file_name)


class AccountParser:
    """docstring"""

    def __init__(self):
        """docstring pendiente"""
        self.PATTERN = r"([a-zA-Z0-9]*)(_ACC_)([A-Z]*)"
        self.acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]

    def get_acc_index(self):
        """
        Account selector in a numerical way: Associates a number to a given account
        so it can be selected by typing the number and not the name
        """
        acc_indexator = enumerate(self.acc_list)
        self.acc_dict = dict(acc_indexator)
        return self.acc_dict

    def get_acc_properties(self):
        """docstring pendiente"""
        acc_index_dict = self.get_acc_index()
        for key, val in acc_index_dict.items():
            re_matches = re.match(self.PATTERN, val).groups()
            acc_name = re_matches[0]
            acc_currency = re_matches[2]
            acc_index_dict[key] = {
                "acc_name": acc_name,
                "currency": acc_currency,
            }
        return acc_index_dict
