#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 18:14:01 2022

@author: igna
"""
from mock import patch

def greet(name):
    print('Hello ', name)

@patch('builtins.print')
def test_greet(mock_print):
    # The actual test
    greet('John')
    mock_print.assert_called_with('Hello ', 'John')
    greet('Eric')
    mock_print.assert_called_with('Hello ', 'Eric')