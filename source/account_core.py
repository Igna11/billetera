#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 14:01:51 2022

@author: igna
Core module of accounts and its operations
"""

import os
import re

from source import errors


class Accounts:
    """
    Superclass of AccountsCreator.
    Instantiates an Account Object. This object has information of the object,
    like name, currency, filename, column headers of the file, if the account
    exists or not, the amount of rows in the file and the get_last_line method
    to retrieve as attributes the values of the las line of the file.
    ISO 4217 must be used to define currencies.
    """

    def __init__(self, acc_name: str, acc_currency: str) -> None:
        self.acc_name = acc_name.replace(" ", "_")
        self.acc_currency = acc_currency.upper()
        self.acc_file_name = f"{self.acc_name}_ACC_{self.acc_currency.upper()}.csv"
        self.exists = self.acc_file_name in os.listdir()
        self.acc_data_len = 1
        self.acc_column_headers = [
            "Date",
            "Time",
            "Total",
            "Incomes",
            "Extractions",
            "Expenses",
            "Category",
            "Subcategory",
            "Description",
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
        """
        Creates the account file where all data will be stored as .csv file
        only if there is an user loged.
        """
        if not "USR" in os.getcwd():
            raise errors.NotOpenSessionError
        if "USR" in os.getcwd():
            if self.exists:
                raise errors.AccountAlreadyExistsError(self.acc_name, self.acc_currency)
            header = "\t".join(self.acc_column_headers) + "\n"
            with open(self.acc_file_name, "x", encoding="UTF-8") as account:
                account.write(header)

    def remove_account(self) -> None:
        """Deletes the account file. The information CAN NOT be recovered"""
        if not "USR" in os.getcwd():
            raise errors.NotOpenSessionError
        if "USR" in os.getcwd():
            os.remove(self.acc_file_name)


class AccountParser:
    """
    This class takes care of the parsing of individual accounts as well as all
    accounts in order to obtain data of total values for different currencies.

    The attributes of this class are:
        - pattern: generates de regex patter to extract the name of the
            account and the currency
        - acc_list: List of accounts for a given user
        - acc_data_len: number of lines for a given account, including
            headers.
        - acc_dict: An index to enumerate accounts, e.g. :
            {1: "Dummy_account", 2: "Dummy2_account", ...}
        - ars_total: total value of ARS of a given account.
        - usd_total: total value of USD of a given account.
    """

    def __init__(self):
        self.pattern = r"([a-zA-Z0-9_]*)(_ACC_)([A-Z]*)"
        self.acc_list = [acc for acc in os.listdir() if "_ACC_" in acc]
        self.acc_data_len = 1
        self.acc_dict = {}
        self.ars_total = 0.0
        self.usd_total = 0.0

    def acc_indexer(self) -> dict:
        """
        Associates a number to a given account so it can be selected by typing
        the number and not the name.
        """
        acc_indexator = enumerate(self.acc_list, 1)
        self.acc_dict = dict(acc_indexator)
        return self.acc_dict

    def get_acc_properties(self) -> dict:
        """
        Returns a dictionary with the numerical index of the account, the
        account name and the currency, e.g.
        {
            1: {"acc_name": "DummyAccount", "acc_currency": "ARS"},
            2: {"acc_name": "blelbe", "acc_currency": "USD"}
        }
        """
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

    def get_acc_pretty_names(self):
        """
        Returns a list with pretty names for the existing accounts.
        """
        pretty_list = []
        for acc in self.acc_list:
            pretty_list.append(acc.replace(acc[-12:], " (" + acc[-7:-4] + ")"))
        return pretty_list

    def get_acc_total(self, account):
        """Returns the last line of the balance.csv file."""
        with open(account, "r", encoding="latin-1") as acc:
            account_lines = acc.read().splitlines()
        self.acc_data_len = len(account_lines)
        headers = ["Hora", "Date", "Total", "Total(ARS)", "Total(USD)"]
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
