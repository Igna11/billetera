#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 19:00:00 2022

@author: igna
"""


class EmptyAccountError(Exception):
    """Raised when an operation is trying to be performed in an empty account."""

    def __str__(self):
        return "The operation can't be performed because the account is empty."


class NegativeTotalError(Exception):
    """Raised when the result of an operation is negative."""

    def __str__(self):
        return "The operation can't be performed because there is not enough money in account."


class NegativeOrZeroValueError(Exception):
    """Raised when the input value is negative or zero."""

    def __str__(self):
        return "The value provided is either zero or negative and that's not allowed."


class NotReadjustmentError(Exception):
    """Raised when the readjustment value is the same as the current value."""

    def __str__(self):
        return "There is nothing to readjust."


class NotEqualCurrencyError(Exception):
    """Raised when a transfer is trying to be performed between accounts with different currency."""

    def __init__(self, origin_currency, destination_currency):
        self.origin_currency = origin_currency
        self.destination_currency = destination_currency

    def __str__(self):
        return f"""
        \rCan't tranfer from a {self.origin_currency} account to a {self.destination_currency} account.
        """


class AccountDoesNotExistError(Exception):
    """Raised when an operation is trying to be made in a not existing account."""

    def __init__(self, acc_name, acc_currency):
        self.acc_name = acc_name
        self.acc_currency = acc_currency

    def __str__(self):
        return f"""
        \rThe account {self.acc_name}({self.acc_currency}) does not exists.
        """


class AccountAlreadyExistsError(Exception):
    """Raised when an account is trying be created with the name of an existing account."""

    def __init__(self, acc_name, acc_currency):
        self.acc_name = acc_name
        self.acc_currency = acc_currency

    def __str__(self):
        return f"""
        \rCan not create account {self.acc_name}({self.acc_currency}) because it already exists.
        """


class NoConfirmationToDeleteAccountError(Exception):
    """Raised when an account is trying to be deleted with no confirmation from user"""

    def __init__(self, acc_name, acc_currency):
        self.acc_name = acc_name
        self.acc_currency = acc_currency

    def __str__(self):
        return f"Account {self.acc_name}_{self.acc_currency.upper()} can't be deleted without confirmation."


class NotOpenSessionError(Exception):
    """Raised when an account is trying to be created without being logged in."""

    def __str__(self):
        return "Can not create an account without an open session."


class UserAlreadyExistsError(Exception):
    """Raised when trying to create an user with a name that already exists."""

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
    """Raised when an operation is trying to be performed in an user that does not existi."""

    def __init__(self, user):
        self.user = user

    def __str__(self):
        return f"User {self.user} does not exist."


class WrongDirectoryError(Exception):
    """Raised when the current working directory is no /data. This error should not be raised."""

    def __str__(self):
        return "Make sure you are inside '/data' directory before continuing."


class WrongPasswordError(Exception):
    """Raised when the input password is wrong."""

    def __str__(self):
        return "Invalid password."


class PasswdsDontMatchError(Exception):
    """Raised when the two input passwords does not match when creating an user."""

    def __str__(self):
        return "Password do not match."


class InvalidEmailError(Exception):
    """
    Raised when an email without standard format is entered being:
    standard: something@other.thing
    """

    def __str__(self, input_mail):
        return f"{input_mail} is not a valid format of mail."


class InvalidNameError(Exception):
    """Raised when a name is and empty string ''"""

    def __str__(self):
        return "An empty string '' is not a valid name for account or user."


class SameAccountTransferError(Exception):
    """Raised when a transfer where the destination account and the origina account are the same"""

    def __str__(self):
        return "Transfer with same origin and destination account can't be processed."


class UserHasNotAccountsError(Exception):
    """Raised when DataAnalyzer class try to parse an user with no accounts"""

    def __str__(self):
        return "User has no accounts yet to gather data to analyze."
