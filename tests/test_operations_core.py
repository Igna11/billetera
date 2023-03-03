#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:16:00 2022

@author: igna
"""
import os
import unittest
from source import errors
from source import operations_core as oper

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(BASE_DIR, "data", "TestUSR")


class TestIncomeOperations(unittest.TestCase):
    """Tests for income_operations method of the class Operations"""

    def test_account_income_not_exists(self):
        """Tests that AccountDoesNotExistError is raised when the account does not exists"""
        name_acc = "AccTest"
        currency_acc = "ARS"
        income = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.AccountDoesNotExistError):
            income.income_operation()

    def test_account_income_negative_value(self):
        """Tests that NegativeOrZeroValueError is raised when a negative value is provided"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        income = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=-500
        )
        with self.assertRaises(errors.NegativeOrZeroValueError):
            income.income_operation()

    def test_account_income_new_total_equals_value(self):
        """Tests that when an account is empty the new_total and income are equal"""
        os.chdir(TEST_DIR)
        name_acc = "Empty"
        currency_acc = "ARS"
        income = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=100
        )
        income.income_operation()
        self.assertEqual(income.new_total, str(income.value))

    def test_account_income_new_total_equals_value_plus_total(self):
        """
        Tests that when an account is not empty, the new_total equals the sum of the Total
        and the income value
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        income = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=100
        )
        income.income_operation()
        total = str(float(income.value) + float(income.Total))
        self.assertEqual(income.new_total, total)


class TestExpenseOperations(unittest.TestCase):
    """Tests for expense_operations method of the class Operations"""

    def test_account_expense_not_exists(self):
        """Tests that AccountDoesNotExistError is raised when the account does not exists"""
        name_acc = "AccTest"
        currency_acc = "ARS"
        expense = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.AccountDoesNotExistError):
            expense.expense_operation()

    def test_account_expense_negative_value(self):
        """Tests that NegativeOrZeroValueError is raised when a negative value is provided"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        expense = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=-500
        )
        with self.assertRaises(errors.NegativeOrZeroValueError):
            expense.expense_operation()

    def test_account_expense_empty_acc(self):
        """Tests that EmptyAccountError ir raised when the account is empty"""
        os.chdir(TEST_DIR)
        name_acc = "Empty"
        currency_acc = "ARS"
        expense = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.EmptyAccountError):
            expense.expense_operation()

    def test_account_expense_negative_total(self):
        """Tests that a NegativeTotalError is raised when the total is negative"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        expense = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=5000000000000
        )
        with self.assertRaises(errors.NegativeTotalError):
            expense.expense_operation()

    def test_account_expense_new_total_equals_total_less_value(self):
        """Tests that when the account is not empty, the new_total equals the substraction of the
        value to the previuos total"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        expense = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=10
        )
        expense.expense_operation()
        total = str(float(expense.Total) - float(expense.value))
        self.assertEqual(expense.new_total, total)


class TestExtractionOperation(unittest.TestCase):
    """Extraction is identical to expense."""


class TestTransferOperation(unittest.TestCase):
    """Tests for transfer_operation method of class Operations"""

    def test_account_origin_transfer_not_exists(self):
        """Tests that AccountDoesNotExistError is raised when the account does not exists"""
        name_acc = "AccTest"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.AccountDoesNotExistError):
            transfer.transfer_operation(
                dest_acc="dest_acc", dest_currency="ARS"
            )

    def test_same_origin_destination_account(self):
        """
        Test that SameAccountTransferError is raised when the same account is used as
        origin and destination
        """
        name_acc = "TEST"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=400
        )
        with self.assertRaises(errors.SameAccountTransferError):
            transfer.transfer_operation(
                dest_acc=name_acc, dest_currency=currency_acc
            )

    def test_account_transfer_negative_value(self):
        """Tests that NegativeOrZeroValueError is raised when a negative value is provided"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=-500
        )
        with self.assertRaises(errors.NegativeOrZeroValueError):
            transfer.transfer_operation(
                dest_acc="dest_acc", dest_currency="ARS"
            )

    def test_account_transfer_empty_acc(self):
        """Tests that EmptyAccountError is raised when the origin account is empty"""
        os.chdir(TEST_DIR)
        name_acc = "Empty"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=50
        )
        with self.assertRaises(errors.EmptyAccountError):
            transfer.transfer_operation(
                dest_acc="dest_acc", dest_currency="ARS"
            )

    def test_account_transfer_negative_total(self):
        """Tests that NegativeTotalError is raised when the total is negative"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=5000000000
        )
        with self.assertRaises(errors.NegativeTotalError):
            transfer.transfer_operation(
                dest_acc="dest_acc", dest_currency="ARS"
            )

    def test_account_transfer_not_equal_currency(self):
        """Tests that NotEqualCurrencyError is raised when a transfer from an
        ARS account to a USD account is trying to be performed"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=10
        )
        with self.assertRaises(errors.NotEqualCurrencyError):
            transfer.transfer_operation(dest_acc="TEST", dest_currency="USD")

    def test_account_transfer_new_totals_destination_empty(self):
        """Tests that the new totals of the origin and destination accounts
        are correct"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        transfer = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=10.0
        )
        dest_acc = transfer.transfer_operation(
            dest_acc="Empty", dest_currency="ARS"
        )
        origin_total = str(float(transfer.Total) - transfer.value)
        destination_total = str(float(dest_acc.Total))
        self.assertEqual(transfer.new_total, origin_total)
        self.assertEqual(dest_acc.Total, destination_total)


class TestReadjustmentOperation(unittest.TestCase):
    """Tests readjustment_operation method of class Operations"""

    def test_account_readjusment_not_exists(self):
        """Tests that AccountDoesNotExistError is raised when account not exists."""
        name_acc = "AccTest"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.AccountDoesNotExistError):
            readjustment.readjustment_operation()

    def test_account_readjustment_negative_value(self):
        """Tests that NegativeOrZeroValueError is raised when a negative value is provided."""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=-500
        )
        with self.assertRaises(errors.NegativeOrZeroValueError):
            readjustment.readjustment_operation()

    def test_account_readjustment_empty_acc(self):
        """Tests that EmptyAccountError is raised when account is empty."""
        os.chdir(TEST_DIR)
        name_acc = "Empty"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=500
        )
        with self.assertRaises(errors.EmptyAccountError):
            readjustment.readjustment_operation()

    def test_account_readjustment_not_readjustment(self):
        """Tests that NotReadjustmentError is raised when value and total are the same"""
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=19.00
        )
        with self.assertRaises(errors.NotReadjustmentError):
            readjustment.readjustment_operation()

    def test_account_readjustment_positive(self):
        """
        Tests that when a new total is grater than the previous one:
           1. a new income greater than 0 is generated,
           2. the new income is the difference between the new one and the previous one.
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=39.00
        )
        readjustment.readjustment_operation()
        self.assertGreater(float(readjustment.new_income), 0)
        self.assertEqual(
            float(readjustment.new_income),
            readjustment.value - float(readjustment.Total),
        )

    def test_account_readjustment_negative(self):
        """
        Tests that when a new total is lower than the previous one:
           1. a new extraction greater than 0 is generated,
           2. the new extraction is the difference between the previous one and the new one.
        """
        os.chdir(TEST_DIR)
        name_acc = "TEST"
        currency_acc = "ARS"
        readjustment = oper.Operations(
            acc_name=name_acc, acc_currency=currency_acc, value=9.00
        )
        readjustment.readjustment_operation()
        self.assertGreater(float(readjustment.new_extraction), 0)
        self.assertEqual(
            float(readjustment.new_extraction),
            float(readjustment.Total) - readjustment.value,
        )


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
