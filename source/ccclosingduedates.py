#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculates approximately the time when the card period closes and the due date. 
it depends on holidays too so it is not perfect"""

import datetime


def update_closing_date(last_closing_date: str):
    """
    input
    last_closing_date: str
        date of the format: DD/MM/YYYY
    returns the next closing date in the same format
    note: The last_closing_date should be the correct date
    """
    last_thursday = datetime.datetime.strptime(last_closing_date, "%d/%m/%Y")
    next_thursday = last_thursday + datetime.timedelta(days=28)
    if next_thursday.day < 26:
        next_thursday = last_thursday + datetime.timedelta(days=35)
    return next_thursday.strftime("%d/%m/%Y")


def update_due_date(last_closing_date: str):
    """
    input
    last_closing_date: str
        date of the format: DD/MM/YYYY
    returns the closing date in the same format
    note: The last_closing_date should be the correct date
    """
    last_thursday = datetime.datetime.strptime(last_closing_date, "%d/%m/%Y")
    due_date = last_thursday + datetime.timedelta(days=8)
    return due_date.strftime("%d/%m/%Y")
