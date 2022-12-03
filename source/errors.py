#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 19:00:00 2022

@author: igna
"""


class EmptyAccountError(Exception):
    """dostring"""

    def __str__(self):
        return "The operation can't be performed because the account is empty."


class NegativeTotalError(Exception):
    """dostring"""

    def __str__(self):
        return "The operation can't be performed because there is not enough money in account."


class NegativeOrZeroValueError(Exception):
    """dostring"""

    def __str__(self):
        return "The value provided is either zero or negative and that's not allowed."


class NotReadjustmentError(Exception):
    """dostrin"""

    def __str__(self):
        return "There is nothing to readjust."


class NotEqualCurrencyError(Exception):
    """dostring"""

    def __init__(self, origin_currency, destination_currency):
        self.origin_currency = origin_currency
        self.destination_currency = destination_currency

    def __str__(self):
        return f"""
        \rCan't tranfer from a {self.origin_currency} account to a {self.destination_currency} account.
        """


class AccountNotExistsError(Exception):
    """dostring"""

    def __init__(self, acc_name, acc_currency):
        self.acc_name = acc_name
        self.acc_currency = acc_currency

    def __str__(self):
        return f"""
        \rThe account {self.acc_name}({self.acc_currency}) does not exists.
        """


class NotOpenSessionError(Exception):
    """dostring"""

    def __str__(self):
        return "Can not create an account without an open session."
