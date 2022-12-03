#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:16:00 2022

@author: igna
"""
import os
import unittest
from source import account_core as core

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(BASE_DIR, "data", "TestUSR")


class TestAccount(unittest.TestCase):
    """Test for the functions inside the class Accounts"""

    def test_add_account(self):
        """Tests that the account file is correctly created"""
        os.chdir(TEST_DIR)
        acc_name = "Test_Account"
        account = core.AccountsCreator(acc_name=acc_name, acc_currency="ARS")
        account.add_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(os.path.isfile(final_acc_name))

    def test_add_account2(self):
        """
        Tests that a FileExistsError raises when trying to create an account
        with the same name as an existing one
        """
        os.chdir(TEST_DIR)
        acc_name = "Test_Account"
        account = core.AccountsCreator(acc_name=acc_name, acc_currency="ARS")
        with self.assertRaises(FileExistsError):
            account.add_account()

    def test_remove_account(self):
        """Tests that the account file is correctly deleted"""
        os.chdir(TEST_DIR)
        acc_name = "Test_Account"
        account = core.AccountsCreator(acc_name=acc_name, acc_currency="ARS")
        account.remove_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(not os.path.isfile(final_acc_name))


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
