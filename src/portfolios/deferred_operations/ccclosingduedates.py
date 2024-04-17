#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculates approximately the time when the card period closes and the due date.
it depends on holidays too so it is not perfect.

NOTES: Santander - VISA:
    All closing dates are thursdays with rare exceptions for holidays.
    All due dates are generally fridays with exceptions on holidays, then they are mondays
"""
from typing import Generator
import datetime
import holidays

FORMAT = "%d/%m/%Y"


def validate_businessday(date: datetime.datetime, region: str) -> bool:
    """
    date: datetime object
    region: str in the ISO 3166 alpha-2 format
    Returns True for non holidays
    """
    region_holidays = holidays.country_holidays(region)
    return bool(date not in region_holidays)


def calc_closing_date(closing_date: str, region: str, prev_or_next: str = "next") -> str:
    """
    input
    closing_date: str, current closing date
        date format needed: DD/MM/YYYY
    returns the previus or next closing date in the same format
    """
    if prev_or_next == "prev":
        delta_days = -35
    elif prev_or_next == "next":
        delta_days = 28
    else:
        raise ValueError(f"Invalid value: {prev_or_next}.")

    closing_date = datetime.datetime.strptime(closing_date, FORMAT)

    new_closing_date = closing_date + datetime.timedelta(days=delta_days)
    if new_closing_date < closing_date and new_closing_date.day <= 25:
        new_closing_date += datetime.timedelta(days=7)
        if not validate_businessday(new_closing_date, region):
            # assumming that closing dates are always thursdays, it is
            # safer to assume the new closing day would be wed instead
            # of friday
            new_closing_date -= datetime.timedelta(days=1)
    elif new_closing_date > closing_date and new_closing_date.day <= 25:
        new_closing_date += datetime.timedelta(days=7)
        if not validate_businessday(new_closing_date, region):
            new_closing_date -= datetime.timedelta(days=1)
    elif not validate_businessday(new_closing_date, region):
        new_closing_date -= datetime.timedelta(days=1)
    return new_closing_date.strftime(FORMAT)


def calc_due_date(closing_date: str, region: str, prev_or_next: str = "next") -> str:
    """
    input
    closing_date: str
        date of the format: DD/MM/YYYY
    returns the previus or the next closing date in the same format
    """
    if prev_or_next == "prev":
        closing_date = calc_closing_date(closing_date, region, "prev")
    elif prev_or_next == "next":
        pass
    else:
        raise ValueError(f"Invalid value: {prev_or_next}.")

    closing_date = datetime.datetime.strptime(closing_date, FORMAT)
    due_date = closing_date + datetime.timedelta(days=8)
    if not validate_businessday(due_date, region):
        # assumming that due dates are always fridays, it is safer
        # to assume the new closing day would be the next monday
        due_date += datetime.timedelta(days=3)
        if not validate_businessday(due_date, region):
            due_date += datetime.timedelta(days=1)
    return due_date.strftime(FORMAT)


def closing_date_gen(closing_date: str, region: str) -> Generator[str, None, None]:
    """
    input
    closing_date: str
        date of the format: DD/MM/YYYY
    Generator of previus closing dates
    """
    while True:
        closing_date = calc_closing_date(closing_date, region, "prev")
        yield closing_date
