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


class AccountAlreadyExistsError(Exception):
    """dostring"""

    def __init__(self, acc_name, acc_currency):
        self.acc_name = acc_name
        self.acc_currency = acc_currency

    def __str__(self):
        return f"""
        \rCan not create account {self.acc_name}({self.acc_currency}) because it already exists.
        """


class NotOpenSessionError(Exception):
    """dostring"""

    def __str__(self):
        return "Can not create an account without an open session."


class UserAlreadyExistsError(Exception):
    """dostring"""

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return f"User {self.user} already exists."


class UserCouldNotBeDeletedError(Exception):
    """Raised when a given user could be deleted from database"""

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return f"User {self.user} could not be removed from database"


class UserDoesNotExistsError(Exception):
    """dostring"""

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return f"User {self.user} does not exist."


class WrongDirectoryError(Exception):
    """dostring"""

    def __str__(self):
        message = """
        Make sure you are inside '/data' directory before continuing.
        """
        return message


class WrongPasswordError(Exception):
    """dostring"""

    def __str__(self):
        return "Invalid password."


class PasswdsDontMatchError(Exception):
    """dostring"""

    def __str__(self):
        return "Password do not match"
