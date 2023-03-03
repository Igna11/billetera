#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:00:00 2022

@author: igna
"""
from datetime import datetime
from source import errors
from source import account_core as account


class Operations(account.Accounts):
    """
    Core class of operations, subclass of account_core:
    -Income
    -Expense
    -Extraction
    -Transfer
    -readjustment
    inherits: acc_name, currency, acc_file_name, exists, acc_column_headers
    """

    def __init__(self, acc_name: str, acc_currency: str, value: float) -> None:
        super().__init__(acc_name, acc_currency)
        self.value = round(value, 2)
        self.new_income = "0.00"
        self.new_expense = "0.00"
        self.new_extraction = "0.00"
        self.new_total = "0.00"
        self.new_balance = "0.00"
        self.optime = datetime.now().time().strftime("%H:%M:%S")
        self.opdate = datetime.now().date().strftime("%d-%m-%Y")

    def __repr__(self) -> str:
        return (
            f"Operations({self.acc_name}, {self.acc_currency}, {self.value})"
        )

    def income_operation(self) -> None:
        """Defines the logic behind the income operation."""
        if not self.exists:
            raise errors.AccountDoesNotExistError(
                self.acc_name, self.acc_currency
            )
        if self.value <= 0:
            raise errors.NegativeOrZeroValueError
        self.get_last_line()
        if self.acc_data_len == 1:
            self.new_total = self.new_income = str(self.value)
        elif self.acc_data_len > 1:
            total = round(float(self.Total) + self.value, 2)
            self.new_total = str(total)
            self.new_income = str(self.value)

    def expense_operation(self) -> None:
        """Defines the logic behind the expense operation."""
        if not self.exists:
            raise errors.AccountDoesNotExistError(
                self.acc_name, self.acc_currency
            )
        if self.value <= 0:
            raise errors.NegativeOrZeroValueError
        self.get_last_line()
        if self.acc_data_len == 1:
            raise errors.EmptyAccountError
        if self.acc_data_len > 1:
            total = round(float(self.Total) - self.value, 2)
            if total < 0:
                raise errors.NegativeTotalError
            if total >= 0:
                self.new_total = str(total)
                self.new_expense = str(self.value)

    def extraction_operation(self) -> None:
        """
        Defines the logic behind the extraction operation.
        Same as expense operation.
        """
        if not self.exists:
            raise errors.AccountDoesNotExistError(
                self.acc_name, self.acc_currency
            )
        if self.value <= 0:
            raise errors.NegativeOrZeroValueError
        self.get_last_line()
        if self.acc_data_len == 1:
            raise errors.EmptyAccountError
        if self.acc_data_len > 1:
            total = round(float(self.Total) - self.value, 2)
            if total < 0:
                raise errors.NegativeTotalError
            if total >= 0:
                self.new_total = str(total)
                self.new_extraction = str(self.value)

    def transfer_operation(
        self, dest_acc: str, dest_currency: str
    ) -> account.Accounts:
        """
        Defines the logic of the transfer operation.
        arguments:
            dest_acc: str
            Destination account for the transfer.
            dest_currency: str
            Currency used by the destination account.
        """
        if not self.exists:
            raise errors.AccountDoesNotExistError(
                self.acc_name, self.acc_currency
            )
        if self.value <= 0:
            raise errors.NegativeOrZeroValueError
        self.get_last_line()
        if self.acc_name == dest_acc and self.acc_currency == dest_currency:
            raise errors.SameAccountTransferError
        if self.acc_data_len == 1:
            raise errors.EmptyAccountError
        if self.value > float(self.Total):
            raise errors.NegativeTotalError
        dest_acc = account.Accounts(dest_acc, dest_currency)
        dest_acc.get_last_line()
        if self.acc_currency != dest_acc.acc_currency:
            raise errors.NotEqualCurrencyError(
                self.acc_currency, dest_acc.acc_currency
            )
        self.new_total = str(round(float(self.Total) - self.value, 2))
        self.new_extraction = str(self.value)
        if dest_acc.acc_data_len == 1:
            dest_acc.Total = dest_acc.income = str(self.value)
        elif dest_acc.acc_data_len > 1:
            dest_acc.Total = str(round(float(dest_acc.Total) + self.value, 2))
            dest_acc.income = str(self.value)
        return dest_acc

    def readjustment_operation(self) -> None:
        """Defines the logic behind the readjustment operation."""
        if not self.exists:
            raise errors.AccountDoesNotExistError(
                self.acc_name, self.acc_currency
            )
        if self.value < 0:
            raise errors.NegativeOrZeroValueError
        self.get_last_line()
        if self.acc_data_len == 1:
            raise errors.EmptyAccountError
        if self.value == float(self.Total):
            raise errors.NotReadjustmentError
        self.new_total = str(self.value)
        if self.value > float(self.Total):
            self.new_income = str(round(self.value - float(self.Total), 2))
        if self.value < float(self.Total):
            self.new_extraction = str(round(float(self.Total) - self.value, 2))
