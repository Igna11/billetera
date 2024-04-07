#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para popular las tablas"""

import os
import time
from datetime import datetime, timedelta
import pandas as pd

from src.deferred_operations.db_handlers import (
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


def update_cc_closingdue_dates_table(connection):
    """
    Checks if the closing and due date of the credit cards
    are up to date and, if not, updates it approximately.
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
        if due_datetime < datetime.now() and close_datetime > datetime.now():
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
    - The number of installments paid and the total number of installments,
    - The current date
    - The date the purchase was made
    - The closing dates
    - The due dates
    Case 1. The purchase is made today, with or without installments and the closing date
    may be or may be not today: Then is active.
    Case 2. The purchase is made today, with or without installments and the closing date
    has been updated to the next one, while the due date is yet to come. So this purchase
    belongs to the following card cycle: Then is not active until the due date is updated.
    Case 3. The purchase was made in the past, before the last close date and without
    installments. Then is not active
    Case 4. The purchase was made in the past, before the last close date and with more
    than 1 installments. Then is active
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
    today = datetime.now()
    print("checking active operations")
    A = execute_read_query(connection, read_query)
    # A : [(operation_id, operation_date, operation_installments, is_active),..]
    for tup in A:
        row = list(tup)
        id, date, installments, active, closing_date, due_date = (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
        )
        date = datetime.strptime(date, FORMAT)
        current_due_datetime = datetime.strptime(due_date, FORMAT)
        current_closing_datetime = datetime.strptime(closing_date, FORMAT)
        gen_cdate = closing_date_gen(closing_date, "AR")

        # day_difference = today - date
        # if day_difference.days >= 36 and installment == 1:
        #    active = 0
        prev_cdate = next(gen_cdate)
        prev_ddate = calc_due_date(prev_cdate, "AR")
        prev_cdatetime = datetime.strptime(prev_cdate, FORMAT)
        prev_ddatetime = datetime.strptime(prev_ddate, FORMAT)
        # case 3
        if date < prev_cdatetime and installments == 1 and date < current_due_datetime:
            active = 0
            update_operation(connection, id, is_active=active)
            print(f"Compra Id: {id} inactivada por case 3")
        # case 2
        elif date < current_due_datetime < current_closing_datetime and installments == 1:
            print(id)
            active = 0
            update_operation(connection, id, is_active=active)
            print(f"Compra Id: {id} inactivada case 2")


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
update_cc_closingdue_dates_table(connection)
# manually update credit card closing date:
# update_cc(connection, id=2455, card_closing_date="27/03/2024")
update_cc_closingdue_dates_table(connection)
update_is_active(connection)
print(df)
print("=" * 140, "\n", "printing only active operations")
df2 = pd.read_sql_query(query, connection)
print(df2)
print("database deleted")
total = df2.installments_amount.sum()
print("A pagar el proximo vencimiento: ", f"${total:.2f}")


# first = "29/02/2024"
# for i in range(10):
#    due = calc_due_date(first, "AR", "next")
#    first = calc_closing_date(first, "AR", "next")
#    print(f"Cierre: {first} -> Vencimiento: {due}")
