#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sqlite3 as sql
from asyncoperations import (
    create_connection,
    execute_query,
    execute_read_query,
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


#
#
## first credit card testing querie
# card_query = """
# INSERT INTO
#  credit_cards (card_id, card_brand, card_issuer, card_expiration, card_closing_date, card_due_date)
# VALUES
#  (2444, 'VISA', 'Santander', '09-29', '29-02-2024', '05-03-2024');
# """
#
## creation of the tables
# execute_query(connection=connection, query=card_query)
# print("firts credit card saved")
#
# operation_dict = {
#    "date": "2024-02-15",
#    "time": "09:35:30",
#    "card": "VISA",
#    "card_id": 2444,
#    "repetitions": 6,
#    "amount": 5640.43,
#    "category": "Pagos",
#    "subcategory": "VISA",
#    "description": "motor nuevo para la renoletá",
#    "other": "Auto-Repuestos",
# }
#
# data1, data2 = data_split(operation_dict)
#
# insert_operation(connection, data1, data2)
#
# query = """SELECT * FROM credit_card_operations WHERE is_active=1;"""
#
# df = pd.read_sql_query(query, connection)
# print(df)
#
# result = execute_read_query(connection, query)
#
# df["date"] = pd.to_datetime(df["date"])
# df["time"] = pd.to_datetime(df["time"])
#
# total = df["amount"].sum()
# date = df["date"][0].strftime("%d/%m/%Y")
# print(f"El total a pagar el {date} es {total:.2f}")
