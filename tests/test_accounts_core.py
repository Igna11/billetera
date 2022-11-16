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
    """Test for the functions inside the class UsersDB"""

    def test_add_account(self):
        acc_name = os.path.join(TEST_DIR, "Test_Account")
        account = account_core.Accounts(acc_name=acc_name, acc_currency="ARS")
        account.add_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(os.path.isfile(final_acc_name))

    def test_remove_account(self):
        acc_name = os.path.join(TEST_DIR, "Test_Account")
        account = account_core.Accounts(acc_name=acc_name, acc_currency="ARS")
        account.remove_account()
        final_acc_name = f"{acc_name}_ACC_ARS.txt"
        self.assertTrue(not os.path.isfile(final_acc_name))


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
