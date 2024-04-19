#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 20:00:05 2022

@author: igna
"""
import os
import unittest
from unittest.mock import patch
from src.portfolios import accounts as acc

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DIR = os.path.join(BASE_DIR, "data", "UnitTestingUSR")
TEST_ACC_NAME = "Test_Account"
DUMMY_ACC_NAME = "Dummy_Name"
TEST_CURRENCY_1 = "ARS"
TEST_CURRENCY_2 = "USD"


class TestCreateAccounts(unittest.TestCase):
    """
    Test the creation of accounts. If for any reason the account file already exists
    it deletes to ensure that the test runs correctly."""

    def test_create_account_currency_1(self):
        """Tests that the account file (ARS) is created. If the file already exists, it deletes it."""
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_1}.csv"
        if acc_filename in os.listdir():
            os.remove(acc_filename)
        acc.create_account(name_acc=TEST_ACC_NAME, currency_acc=TEST_CURRENCY_1)
        self.assertTrue(os.path.isfile(acc_filename))

    def test_create_account_currency_2(self):
        """Tests that the account file (USD) is created"""
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_2}.csv"
        if acc_filename in os.listdir():
            os.remove(acc_filename)
        acc.create_account(name_acc=TEST_ACC_NAME, currency_acc=TEST_CURRENCY_2)
        self.assertTrue(os.path.isfile(acc_filename))


class TestNotDeleteAccounts(unittest.TestCase):
    """Test that the accounts won't be deleted"""

    def test_not_delete_account_currency_1(self):
        """
        Tests that an account (ARS) still exists after trying to delete it with a wrong name
        """
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_1}.csv"
        acc.delete_account(name_acc=DUMMY_ACC_NAME, currency_acc=TEST_CURRENCY_1)
        self.assertTrue(os.path.isfile(acc_filename))

    def test_not_delete_account_currency_2(self):
        """
        Tests that an account (USD) still exists after trying to delete it with a wrong name
        """
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_2}.csv"
        acc.delete_account(name_acc=DUMMY_ACC_NAME, currency_acc=TEST_CURRENCY_2)
        self.assertTrue(os.path.isfile(acc_filename))


class TestDeleteAccounts(unittest.TestCase):
    """Tests the deletion of the accounts"""

    def test_delete_account_currency_1(self):
        """Test that an account (ARS) file does not exists after deletion"""
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_1}.csv"
        acc.delete_account(
            name_acc=TEST_ACC_NAME, currency_acc=TEST_CURRENCY_1, confirmation=True
        )
        self.assertFalse(os.path.isfile(acc_filename))

    def test_delete_account_currency_2(self):
        """Test that an account (USD) file does not exists after deletion"""
        os.chdir(USER_DIR)
        acc_filename = f"{TEST_ACC_NAME}_ACC_{TEST_CURRENCY_2}.csv"
        acc.delete_account(
            name_acc=TEST_ACC_NAME, currency_acc=TEST_CURRENCY_2, confirmation=True
        )
        self.assertFalse(os.path.isfile(acc_filename))


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
