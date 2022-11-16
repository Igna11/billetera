#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:16:00 2022

@author: igna
"""
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DIR = os.path.join(BASE_DIR, "tests")

from source import account_core


class TestAccount(unittest.TestCase):
    """Test for the functions inside the class Accounts"""

    def test_add_account(self):
        """Tests that the account file is correctly created"""
        acc_name = os.path.join(TEST_DIR, "Test_Account")
        account = account_core.Accounts(acc_name=acc_name, acc_currency="ARS")
        account.add_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(os.path.isfile(final_acc_name))
    
    def test_add_account2(self):
        """
        Tests that a FileExistsError raises when trying to create an account
        with the same name as an existing one
        """
        acc_name = os.path.join(TEST_DIR, "Test_Account")
        account = account_core.Accounts(acc_name=acc_name, acc_currency="ARS")
        with self.assertRaises(FileExistsError):
            account.add_account()

    def test_remove_account(self):
        """Tests that the account file is correctly deleted"""
        acc_name = os.path.join(TEST_DIR, "Test_Account")
        account = account_core.Accounts(acc_name=acc_name, acc_currency="ARS")
        account.remove_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(not os.path.isfile(final_acc_name))


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
