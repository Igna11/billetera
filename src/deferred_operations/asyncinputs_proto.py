#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3 as sql
from src.deferred_operations.db_handlers import (
    insert_new_cc,
    update_cc,
    delete_cc,
    insert_new_operation,
)


def new_cc(connection: sql.connect) -> None:
    card_id = int(input("Credit card last 4 digits: "))
    card_brand = input("Credit card brand: ")
    card_issuer = input("Credit card issuer bank or entity: ")
    card_expiration = input("Credit card expiration date in format DD/MM: ")
    card_cdate = input(
        "Credit card closing date, in format DD/MM/YYYY (the correct way): "
    )
    card_ddate = input("Credit card due date, in format DD/MM/YYYY: ")
    insert_new_cc(
        connection,
        card_id,
        card_brand,
        card_issuer,
        card_expiration,
        card_cdate,
        card_ddate,
    )


def edit_cc(connection: sql.connect) -> None:
    card_id = int(input("Credit card last 4 digits: "))
    card_brand = input("Credit card brand: ")
    card_issuer = input("Credit card issuer bank or entity: ")
    card_expiration = input("Credit card expiration date in format DD/MM: ")
    card_cdate = input(
        "Credit card closing date, in format DD/MM/YYYY (the correct way): "
    )
    card_ddate = input("Credit card due date, in format DD/MM/YYYY: ")
    update_cc(
        connection,
        card_id,
        card_brand,
        card_issuer,
        card_expiration,
        card_cdate,
        card_ddate,
    )


def remove_cc(connection: sql.connect) -> None:
    card_id = int(input("Credit card last 4 digits: "))
    card_brand = input("Credit card brand: ")
    card_issuer = input("Credit card issuer bank or entity: ")
    delete_cc(
        connection,
        card_id,
        card_brand,
        card_issuer,
    )


def new_cc_operation(connection: sql.connect) -> None:
    operation_date = input("Date: ")
    operation_time = input("Time: ")
    operation_card_name = input("Card brand: ")
    operation_card_id = input("Card id: ")
    operation_repetitions = input("Cuotas?: ")
    operation_amount = float(input("Amount spent: "))
    operation_category = input("Category: ")
    operation_subcategory = input("Subcategory: ")
    operation_description = input("Description: ")
    other = input("Other relevant data or tag?: ")
    is_active = int(bool(input("Is active?: ")))
    remaining_repetitions = operation_repetitions
    insert_new_operation(
        connection,
        operation_date,
        operation_time,
        operation_card_name,
        operation_card_id,
        operation_repetitions,
        remaining_repetitions,
        operation_amount,
        operation_category,
        operation_subcategory,
        operation_description,
        other,
        is_active,
    )
