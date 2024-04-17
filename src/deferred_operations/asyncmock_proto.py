#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para popular las tablas"""

import os
import time
from datetime import datetime, timedelta
import pandas as pd

from db_handlers import (
    create_connection,
    insert_new_cc,
    insert_new_operation,
    execute_read_query,
    update_cc,
    update_operation,
)

from ccclosingduedates import calc_closing_date, calc_due_date, closing_date_gen

FORMAT = "%d/%m/%Y"
PATH = "./operationsDB.sqlite"

t0 = time.time()
if "operationsDB.sqlite" in os.listdir():
    print("Data base located")
    connection = create_connection(PATH)
    print("connection with database stablished")
else:
    print("Creating data base")
    connection = create_connection(PATH)
    with open("card_tables.sql", "r") as tables:
        table_query_script = tables.read()
    # creation of the tables
    connection.cursor().executescript(table_query_script)
    print("tables created")
t1 = time.time() - t0
print(f"Tarde {t1:.2f} en crear la base de datos")


def manual_update_cc_closingdue_dates_table(
    connection, id: int, cdate: str = "", ddate: str = ""
) -> None:
    """Manually update the closing and due dates of a credit card"""
    if cdate and ddate:
        update_cc(connection, id=id, card_closing_date=cdate, card_due_date=ddate)
    elif cdate and not ddate:
        update_cc(connection, id=id, card_closing_date=cdate)
    elif not cdate and ddate:
        update_cc(connection, id=id, card_due_date=ddate)


def auto_update_cc_closingdue_dates_table(connection):
    """
    Checks if the closing and due date of the credit cards
    are up to date and, if not, updates it approximately.
    Note: It needs to have the latest correct due a closing date
    to work properly.
    """
    read_query = """
    SELECT 
      card_id, card_closing_date, card_due_date 
    FROM 
      credit_cards;"""
    print("Checking closing and due dates")
    A = execute_read_query(connection, read_query)
    # A : [(card_id, closing_date, due_date),(card_id, closing_date, due_date),..]
    for tup in A:
        row = list(tup)
        card_id, closing_date, due_date = row[0], row[1], row[2]
        close_datetime = datetime.strptime(closing_date, FORMAT)
        due_datetime = datetime.strptime(due_date, FORMAT)
        if close_datetime < datetime.now():
            new_cdate = calc_closing_date(closing_date, prev_or_next="next", region="AR")
            row[1] = new_cdate
            update_cc(
                connection,
                card_id,
                card_closing_date=new_cdate,
            )
            print(f"new closing date: {new_cdate} for card id: {card_id}")
        if due_datetime < datetime.now():
            new_ddate = calc_due_date(closing_date, "AR")
            update_cc(
                connection,
                card_id,
                card_due_date=new_ddate,
            )
            print(f"new due date: {new_ddate} for card id: {card_id}")


def update_is_active(connection):
    """
    Checks if the operation still active based on:
    - The number of installments: N
    - The date the purchase was made: pd
    - The closing dates: cd
    - The due dates: dd
    Case A:
        - cd < dd: This is the most common case
        - N installments
        Then if pd < cd - N => is_active = 0
    Case B:
        - cd > dd: this is the case when the closing date is updated but the due date is
        yet to come so, the new cd y bigger than dd.
        - N installaments
        then if pd < cd - (N + 1) => is_active = 0
    where cd - j means calculating the previus j closing dates and not substracting j days.
    """
    read_query = """
    SELECT 
      operation_id, operation_date, operation_installments, is_active, card_closing_date, card_due_date
    FROM
      credit_card_operations
    JOIN 
      credit_cards
    ON
      credit_card_operations.operation_card_id=credit_cards.card_id
    WHERE
      is_active = 1;"""
    print("checking active operations")
    data = execute_read_query(connection, read_query)
    # A : [(operation_id, operation_date, operation_installments, is_active),..]
    for tup in data:
        row = list(tup)
        id, pdate, installments, active, closing_date, due_date = (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
        )
        pdatetime = datetime.strptime(pdate, FORMAT)
        ddatetime = datetime.strptime(due_date, FORMAT)
        cdatetime = datetime.strptime(closing_date, FORMAT)
        gen_cdate = closing_date_gen(closing_date, "AR")
        print(f"id: {id}")
        for i in range(installments - 1):
            prev_cdate = next(gen_cdate)
            print(prev_cdate)

        # Case A: dd < cd and pd < cd - (N + 1) (prev_cdate == N)
        prev_cdatetime = datetime.strptime(prev_cdate, FORMAT)
        if cdatetime < ddatetime and pdatetime < prev_cdatetime:
            active = 0
            print("Case A")
            print(f"purchase date: {pdate}")
            print(f"previus closing date: {prev_cdate}")
            print(f"current closing date: {closing_date}")

        prev_cdate = next(gen_cdate)
        prev_cdatetime = datetime.strptime(prev_cdate, FORMAT)

        # Case B: cd < dd and pd < cd - N
        if ddatetime < cdatetime and pdatetime < prev_cdatetime:
            active = 0
            print("Case B")
        update_operation(connection, id, is_active=active)


t1 = time.time() - t0
print(f"tarde {t1:.2f} en llenar las bases de datos")

query = """
SELECT
  operation_id,
  operation_date,
  operation_time,
  operation_amount,
  installments_paid || '/' || operation_installments as installments,
  installments_amount,
  card_closing_date,
  operation_description
FROM
  credit_card_operations
JOIN
  credit_cards
ON
  credit_card_operations.operation_card_id = credit_cards.card_id
WHERE
  (
    operation_card_id = 2455
    AND operation_card_brand = 'VISA'
    AND is_active = 1
  );
"""
df = pd.read_sql_query(query, connection)
auto_update_cc_closingdue_dates_table(connection)
# manually update credit card closing date:
# update_cc(connection, id=2455, card_closing_date="27/03/2024")
auto_update_cc_closingdue_dates_table(connection)
update_is_active(connection)
print(df)
print("=" * 140, "\n", "printing only active operations")
df2 = pd.read_sql_query(query, connection)
print(df2)
total = df2.installments_amount.sum()
print("A pagar el proximo vencimiento: ", f"${total:.2f}")
