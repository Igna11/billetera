#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para popular las tablas"""

import os
import time
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
