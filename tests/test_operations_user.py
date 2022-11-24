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
        """Tests that a plain income is performed successfully"""
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
            str(value),
            "0.00",
            "0.00",
            "test",
            "test",
            "test",
            "0.00",
        ]
        patron_row = "\t".join(column_list) + "\n"
        self.assertEqual(test_row, patron_row)

    def test_account_income_negative_value(self):
        """Tests that NegativeOrZeroValueError is raised when a negative value is provided"""
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
        """Tests that NegativeOrZeroValueError is raised when zero is provided"""
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
