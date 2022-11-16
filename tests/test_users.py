#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:42:17 2022

@author: igna
"""
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DIR = os.path.join(BASE_DIR, "data", "TestUSR")
sys.path.append(BASE_DIR)

from source.users import cerrar_sesion


class TestUser(unittest.TestCase):
    """Test for the functions inside users.py"""

    def test_cerrar_sesion(self):
        """Tests that when closing sesion the final directory is not an USR one"""
        os.chdir(USER_DIR)
        cerrar_sesion()
        self.assertTrue(os.getcwd() != USER_DIR)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
