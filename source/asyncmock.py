#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para popular las tablas"""

import os
from datetime import datetime, timedelta
import pandas as pd

from asyncoperations import (
    create_connection,
    insert_new_cc,
    insert_new_operation,
    execute_read_query,
    update_cc,
    update_operation,
)

from ccclosingduedates import update_closing_date, update_due_date

PATH = "./operationsDB.sqlite"
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
    FORMAT = "%d/%m/%Y"
    # A : [(card_id, closing_date, due_date),(card_id, closing_date, due_date),..]
    for tup in A:
        row = list(tup)
        card_id = row[0]
        close_str_date = row[1]
        close_date = datetime.strptime(close_str_date, FORMAT)
        if close_date < datetime.now():
            new_close_date = update_closing_date(close_str_date)
            row[1] = new_close_date
            update_cc(
                connection,
                card_id,
                card_closing_date=new_close_date,
            )
            print(f"new closing date: {new_close_date} for card id: {card_id}")
            tup = tuple(row)


def update_is_active(connection):
    """
    Checks if the operation still active based on:
    - The number of installments payed and the total number of installments,
    - The current date
    - The date the purchase was made
    If the purchase is made in 1 installment and the date of the purchase and
    today are separated by 36 or more days, then the purchase is asumed to be
    already payed (because the maximum difference between due dates is 35 days).
    """
    read_query = """
    SELECT 
      operation_id, operation_date, operation_installments, is_active
    FROM
      credit_card_operations
    WHERE
      is_active = 1;"""
    today = datetime.now()
    FORMAT = "%d/%m/%Y"
    print("checking active operations")
    A = execute_read_query(connection, read_query)
    # A : [(operation_id, operation_date, operation_installments, is_active),..]
    for tup in A:
        row = list(tup)
        id, date, installment, active = row[0], row[1], row[2], row[3]
        date = datetime.strptime(date, FORMAT)
        day_difference = today - date
        if day_difference.days >= 36 and installment == 1:
            active = 0
            update_operation(connection, id, is_active=active)


insert_new_cc(
    connection, "2444", "VISA", "Santander", "09/27", "29/02/2024", "08/03/2024"
)
insert_new_cc(
    connection, "2455", "VISA", "Santander", "09/25", "29/03/2024", "08/04/2024"
)
insert_new_cc(
    connection, "5958", "AMEX", "Santander", "11/29", "29/02/2024", "11/03/2024"
)

insert_new_operation(
    connection,
    operation_date="09/01/2024",
    operation_time="18:25:00",
    operation_amount=13965,
    operation_category="VISA",
    operation_subcategory="Bazar",
    operation_description="Compra de cositas de plástico en colombraro",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_payed=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="11/01/2024",
    operation_time="22:00:00",
    operation_amount=292290,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra de colchon simomns",
    other="MercadoLibre",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=6,
    installments_payed=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/01/2024",
    operation_time="19:00:00",
    operation_amount=18198,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra de cortina para el living",
    other="Compras",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_payed=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="31/01/2024",
    operation_time="22:00:00",
    operation_amount=16616,
    operation_category="VISA",
    operation_subcategory="Servicios",
    operation_description="Pago Claro Daniel y telefonia e internet",
    other="Servicios",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="06/02/2024",
    operation_time="12:00:00",
    operation_amount=21109,
    operation_category="VISA",
    operation_subcategory="MercadoLibre",
    operation_description="Compra de cosas varias de bazar por ML",
    other="MercadoLibre",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="09/02/2024",
    operation_time="11:30:00",
    operation_amount=14984,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="10/02/2024",
    operation_time="20:31:00",
    operation_amount=4580,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de adrogue antes de ir a la isla",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/02/2024",
    operation_time="11:51:00",
    operation_amount=47142.9,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra del set de espejos",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/02/2024",
    operation_time="12:32:00",
    operation_amount=8699.30,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/02/2024",
    operation_time="18:39:00",
    operation_amount=8205,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="03/03/2024",
    operation_time="16:48:49",
    operation_amount=119998,
    operation_category="VISA",
    operation_subcategory="Indumentaria",
    operation_description="Compra de un ambo (saco y pantalon) en mcownes",
    other="Ropa, Saco, Ambo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="05/03/2024",
    operation_time="19:50:43",
    operation_amount=6840,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compra en el dia de atun, mermelada y jugo clight",
    other="Comida",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="09/03/2024",
    operation_time="19:50:43",
    operation_amount=59290,
    operation_category="VISA",
    operation_subcategory="Indumentaria",
    operation_description="Compra en de zapatos de vestir en bleu, caseros",
    other="Zapatos",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="17/03/2024",
    operation_time="15:30:43",
    operation_amount=17000,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="2 hamburguesas de hutch en pedidos ya",
    other="Comida, Hutch",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="17/03/2024",
    operation_time="18:10:43",
    operation_amount=10800,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="Docena y media de facturas en la esperanza y 1/4 de galletitas de miel",
    other="Comida, Merienda, Facturas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="21/03/2024",
    operation_time="10:33:00",
    operation_amount=4400,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="Desayuna en nucha buscando wifi para laburar",
    other="Comida, Desayuno, Cafe, Facturas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="22/03/2024",
    operation_time="11:12:00",
    operation_amount=13050,
    operation_category="VISA",
    operation_subcategory="Farmacia",
    operation_description="Tafirol 1g, ibu 600, te vick",
    other="Remedios, Medicamentos",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)
query = """
SELECT
  operation_id,
  operation_date,
  operation_time,
  operation_amount,
  installments_payed || '/' || operation_installments as installments,
  installments_amount
FROM
  credit_card_operations
WHERE
  (
    operation_card_id = 2455
    AND operation_card_brand = 'VISA'
    AND is_active = 1
  );
"""

df = pd.read_sql_query(query, connection)
update_cc_closingdue_dates_table(connection)
update_is_active(connection)
print(df)
print("=" * 90, "\n", "printing only active operations")
df = pd.read_sql_query(query, connection)
print(df)
os.remove("operationsDB.sqlite")
print("database deleted")
total = df.installments_amount.sum()
print("A pagar el proximo vencimiento: ", f"${total:.2f}")
