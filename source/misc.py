#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:06:08 2022

@author: igna
"""

from datetime import datetime


def date_gen():
    """
    Non-user function:
    Generates a dictionary with date an time in a latin-format: d-m-y
    """
    time = datetime.now()
    date = time.strftime("%d-%m-%Y")
    hour = time.strftime("%H:%M:%S")
    return {"Fecha": date, "hora": hour}


def extra_char_cleaner(charchain: str):
    """
    Non-user function:
    Strips all chars from the account string name except of its name
    returns the name cleaned
    """
    charchain = (
        charchain.replace("CUENTA", "")
        .replace("_DOL", "")
        .replace(".txt", "")
        .replace("USR", "")
    )
    return charchain
