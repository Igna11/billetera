#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:42:17 2022

@author: igna
"""
import os
import io
import unittest
from unittest.mock import patch


from Billetera import crear_usuario, eliminar_usuario, iniciar_sesion, cerrar_sesion


class TestUser(unittest.TestCase):
    """ Test the desired functioning of user related functions"""
    
    @patch("builtins.input", lambda *args: "TestDir")
    def test_create(self):
        crear_usuario()
        self.assertTrue(os.path.isdir("TestDirUSR"))
    
    @patch("builtins.input", lambda *args: "TestDir")
    def test_alreadyexists(self):
        crear_usuario()
        self.assert_called_with("Ya existe el usuario 'TestDirUSR'")
        

if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)