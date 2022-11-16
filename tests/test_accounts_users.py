#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 20:00:05 2022

@author: igna
"""
import os
import sys
import unittest
from unittest.mock import patch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DIR = os.path.join(BASE_DIR, "data", "TestUSR")
sys.path.append(BASE_DIR)

from source import accounts as acc

inputs_pesos = ["CuentaTest", "ARS"]
inputs_dolar = ["CuentaTest", "USD"]


class TestCreateAccounts(unittest.TestCase):
    """Test the creation of accounts"""

    @patch("builtins.input", lambda _: inputs_pesos.pop(0))
    def test_crear_cuenta_pesos(self):
        os.chdir(USER_DIR)
        acc.crear_cuenta()
        self.assertTrue(os.path.isfile("CuentaTest_ACC_ARS.txt"))

    @patch("builtins.input", lambda _: inputs_dolar.pop(0))
    def test_crear_cuenta_dolar(self):
        os.chdir(USER_DIR)
        acc.crear_cuenta()
        self.assertTrue(os.path.isfile("CuentaTest_ACC_USD.txt"))


inputs_noeliminar_pesos = ["1", "cualquiercosaparanoeliminar"]
inputs_noeliminar_dolar = ["2", "cualquiercosaparanoeliminar"]


class TestNotDeleteAccounts(unittest.TestCase):
    """Test that the accounts won't be deleted"""

    @patch("builtins.input", lambda _: inputs_noeliminar_pesos.pop(0))
    def test_eliminar_cuenta_pesos_no(self):
        os.chdir(USER_DIR)
        acc.eliminar_cuenta()
        self.assertTrue(os.path.isfile("CuentaTest_ACC_ARS.txt"))

    @patch("builtins.input", lambda _: inputs_noeliminar_dolar.pop(0))
    def test_no_eliminar_cuenta_dolar_no(self):
        os.chdir(USER_DIR)
        acc.eliminar_cuenta()
        self.assertTrue(os.path.isfile("CuentaTest_ACC_USD.txt"))


inputs_eliminar_pesos = ["CuentaTest", "ARS", "1"]
inputs_eliminar_dolar = ["CuentaTest", "USD", "1"]


class TestDeleteAccounts(unittest.TestCase):
    """Tests the deletion of the accounts"""

    @patch("builtins.input", lambda _: inputs_eliminar_pesos.pop(0))
    def test_eliminar_cuenta_pesos_si(self):
        os.chdir(USER_DIR)
        acc.eliminar_cuenta()
        self.assertFalse(os.path.isfile("CuentaTest_ACC_ARS.txt"))

    @patch("builtins.input", lambda _: inputs_eliminar_dolar.pop(0))
    def test_eliminar_cuenta_dolar_si(self):
        os.chdir(USER_DIR)
        acc.eliminar_cuenta()
        self.assertFalse(os.path.isfile("CuentaTest_ACC_USD.txt"))


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
