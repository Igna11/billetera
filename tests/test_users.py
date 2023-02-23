#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:42:17 2022

@author: igna
"""
import os
import unittest
from source.users import log_out


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_DIR = os.path.join(BASE_DIR, "data", "TestUSR")


class TestUser(unittest.TestCase):
    """Test for the functions inside users.py"""

    def test_cerrar_sesion(self):
        """Tests that when closing sesion the final directory is not an USR one"""
        os.chdir(USER_DIR)
        log_out()
        self.assertTrue(os.getcwd() != USER_DIR)


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
