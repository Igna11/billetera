#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:16:00 2022

@author: igna
"""
import os
import unittest
from datetime import datetime
from source import errors
from source import operations
from source import account_core as account

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(BASE_DIR, "data", "TestUSR")


class TestUserIncome(unittest.TestCase):
    """Tests for user function income()"""

    def test_account_income_plain(self):
        """Tests that a plain income is performed successfully."""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = 10
        category = subcategory = description = "test"
        optime = datetime.now().time().strftime("%H:%M:%S")
        opdate = datetime.now().date().strftime("%d-%m-%Y")
        # run the function with pre-set values
        test_row = operations.income(
            value,
            name_acc,
            currency_acc,
            category,
            subcategory,
            description,
            test_mode=True,
        )
        # create an Account object to retrieve values to use as patron
        acc = account.Accounts(name_acc, currency_acc)
        acc.get_last_line()
        acc.Total = str(float(acc.Total) + value)
        column_list = [
            opdate,
            optime,
            acc.Total,
            str(value),  # income
            "0.00",  # extraction
            "0.00",  # expense
            "test",  # category
            "test",  # subcategory
            "test",  # description
            "0.00",  # balance
        ]
        patron_row = "\t".join(column_list) + "\n"
        self.assertEqual(test_row, patron_row)

    def test_account_income_account_not_exists(self):
        """
        Tests that AccountNotExistsError is raised when the account does not
        exists.
        """
        os.chdir(TEST_DIR)
        name_acc = "No existo"
        currency_acc = "ARS"
        value = 0
        category = subcategory = description = "test"
        with self.assertRaises(errors.AccountNotExistsError):
            operations.income(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_income_negative_value(self):
        """
        Tests that NegativeOrZeroValueError is raised when a negative value is
        provided.
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = -10
        category = subcategory = description = "test"
        with self.assertRaises(errors.NegativeOrZeroValueError):
            operations.income(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_income_zero_value(self):
        """Tests that NegativeOrZeroValueError is raised when zero is provided."""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = 0
        category = subcategory = description = "test"
        with self.assertRaises(errors.NegativeOrZeroValueError):
            operations.income(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )


class TestUserExpense(unittest.TestCase):
    """Tests for user function expense()"""

    def test_account_income_plain(self):
        """Tests that a plain expense is performed successfully."""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = 10
        category = subcategory = description = "test"
        optime = datetime.now().time().strftime("%H:%M:%S")
        opdate = datetime.now().date().strftime("%d-%m-%Y")
        # run the function with pre-set values
        test_row = operations.expense(
            value,
            name_acc,
            currency_acc,
            category,
            subcategory,
            description,
            test_mode=True,
        )
        # create an Account object to retrieve values to use as patron
        acc = account.Accounts(name_acc, currency_acc)
        acc.get_last_line()
        acc.Total = str(float(acc.Total) - value)
        column_list = [
            opdate,
            optime,
            acc.Total,
            "0.00",  # income
            "0.00",  # extraction
            str(value),  # expense
            "test",  # category
            "test",  # subcategory
            "test",  # description
            "0.00",  # balance
        ]
        patron_row = "\t".join(column_list) + "\n"
        self.assertEqual(test_row, patron_row)

    def test_account_expense_account_not_exists(self):
        """
        Tests that AccountNotExistsError is raised when the account does not
        exists.
        """
        os.chdir(TEST_DIR)
        name_acc = "No existo"
        currency_acc = "ARS"
        value = 0
        category = subcategory = description = "test"
        with self.assertRaises(errors.AccountNotExistsError):
            operations.expense(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_expense_negative_value(self):
        """
        Tests that NegativeOrZeroValueError is raised when a negative value is
        provided.
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = -10
        category = subcategory = description = "test"
        with self.assertRaises(errors.NegativeOrZeroValueError):
            operations.expense(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_expense_zero_value(self):
        """Tests that NegativeOrZeroValueError is raised when zero is provided."""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = 0
        category = subcategory = description = "test"
        with self.assertRaises(errors.NegativeOrZeroValueError):
            operations.expense(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_expense_empty_account(self):
        """Tests that EmptyAccountError is raised when the account is empty."""
        os.chdir(TEST_DIR)
        name_acc = "Empty"
        currency_acc = "ARS"
        value = 30
        category = subcategory = description = "test"
        with self.assertRaises(errors.EmptyAccountError):
            operations.expense(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

    def test_account_expense_negative_total(self):
        """
        Tests that NegativeTotalError is raised when the expense amount is
        greater than the total amount.
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        value = 30
        category = subcategory = description = "test"
        with self.assertRaises(errors.NegativeTotalError):
            operations.expense(
                value,
                name_acc,
                currency_acc,
                category,
                subcategory,
                description,
            )

class TestUserExtraction(unittest.TestCase):
    """The extraction() function is identical to expense function."""

class TestUserTransfer(unittest.TestCase):
    """Tests for user function expense()"""

    def test_account_transfer_plain(self):
        """Tests that a plain transfer is performed successfully."""
        os.chdir(TEST_DIR)
        origin_name_acc = "TEST"
        origin_currency_acc = "ARS"
        dest_name_acc = "TEST2"
        dest_currency_acc = "ARS"
        value = 10
        optime = datetime.now().time().strftime("%H:%M:%S")
        opdate = datetime.now().date().strftime("%d-%m-%Y")
        # run the function with pre-set values
        test_row = operations.transfer(
            value,
            origin_name_acc,
            origin_currency_acc,
            dest_name_acc,
            dest_currency_acc,
            test_mode=True,
        )
        # create an Account object to retrieve values to use as patron for origin
        origin_acc = account.Accounts(origin_name_acc, origin_currency_acc)
        origin_acc.get_last_line()
        origin_acc.Total = str(float(origin_acc.Total) - value)
        origin_column_list = [
            opdate,
            optime,
            origin_acc.Total,
            "0.00",  # income
            str(value),  # extraction
            "0.00",  # expense
            "Transferencia",  # category
            "Tranferencia de salida",  # subcategory
            f"Transferencia a {dest_name_acc}",  # description
            "0.00",  # balance
        ]
        origin_patron_row = "\t".join(origin_column_list) + "\n"
        self.assertEqual(test_row[0], origin_patron_row)
        dest_acc = account.Accounts(dest_name_acc, dest_currency_acc)
        dest_acc.get_last_line()
        dest_column_list = [
            opdate,
            optime,
            str(round(float(dest_acc.Total) + value,2)),
            str(value), # income
            "0.00",  # extraction
            "0.00",  # expense
            "Transferencia",  # category
            "Transferencia de entrada",  # subcategory
            f"Transferencia de {origin_name_acc}",  # description
            "0.00",  # balance
        ]
        dest_patron_row = "\t".join(dest_column_list) + "\n"
        self.assertEqual(test_row[1], dest_patron_row)

    def test_account_transfer_account_not_exists(self):
        pass