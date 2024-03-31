#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para popular las tablas"""

import os
import time
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
    - The number of installments payed and the total number of installments,
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


t0 = time.time()
insert_new_cc(
    connection, "2444", "VISA", "Santander", "09/27", "29/02/2024", "08/03/2024"
)
insert_new_cc(
    connection, "2455", "VISA", "Santander", "09/25", "29/02/2024", "08/03/2024"
)
insert_new_cc(
    connection, "5958", "AMEX", "Santander", "11/29", "29/02/2024", "11/03/2024"
)
insert_new_cc(
    connection, "1234", "DUMMY", "Santander", "11/29", "01/04/2024", "24/03/2024"
)
insert_new_operation(
    connection,
    operation_date="09/01/2024",
    operation_time="18:25",
    operation_amount=13994.64,
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
    operation_time="22:00",
    operation_amount=292899.96,
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
    operation_time="19:00",
    operation_amount=18199.98,
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
    operation_time="22:00",
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
    operation_time="12:00",
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
    operation_time="11:30",
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
    operation_time="20:31",
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
    operation_time="11:51",
    operation_amount=47142.87,
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
    operation_time="12:32",
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
    operation_time="18:39",
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
    operation_time="16:48",
    operation_amount=119998.20,
    operation_category="VISA",
    operation_subcategory="Indumentaria",
    operation_description="Compra de un ambo (saco y pantalon) en mcownes",
    other="Ropa, Saco, Ambo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=6,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="05/03/2024",
    operation_time="19:50",
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
    operation_time="19:50",
    operation_amount=59290.02,
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
    operation_time="15:30",
    operation_amount=17779,
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
    operation_time="18:10",
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
    operation_time="10:33",
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
    operation_time="11:12",
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

insert_new_operation(
    connection,
    operation_date="25/03/2024",
    operation_time="11:12",
    operation_amount=18480,
    operation_category="VISA",
    operation_subcategory="Combustible",
    operation_description="15000 de nafta y 3840 de gas para la renoleta",
    other="Nafta, Gas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="26/03/2024",
    operation_time="12:52",
    operation_amount=14820,
    operation_category="VISA",
    operation_subcategory="Salidas",
    operation_description="Almuerzo con Paui en 'La sede' CFC (cañuelas futbol club)",
    other="Salidas, Restaurant, Almuerzo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

# Dummy case for testing update_is_active function
insert_new_operation(
    connection,
    operation_date="28/03/2024",
    operation_time="12:52",
    operation_amount=11111,
    operation_category="VISA",
    operation_subcategory="Dummy",
    operation_description="Dummy",
    other="Dummy",
    operation_card_id=1234,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

# Dummy for testing
insert_new_operation(
    connection,
    operation_date="15/11/2023",
    operation_time="12:52",
    operation_amount=2211,
    operation_category="VISA",
    operation_subcategory="Dummy",
    operation_description="Dummy",
    other="Dummy",
    operation_card_id=1234,
    operation_card_brand="VISA",
    operation_installments=18,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/03/2023",
    operation_time="12:15",
    operation_amount=20000,
    operation_category="VISA",
    operation_subcategory="Combustible",
    operation_description="Carga gasoil estanciera para ir a buscar el sillon",
    other="Estanciera, Gasoil, Combustible",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/03/2023",
    operation_time="13:22",
    operation_amount=6300,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Cafe nesface instantaneo barato no torrado",
    other="Cafe",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="30/03/2023",
    operation_time="12:49",
    operation_amount=17680,
    operation_category="VISA",
    operation_subcategory="Restaurant",
    operation_description="Hamburguesa en hutch con pauis",
    other="Comida, Hamburguesa, Hutch",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_payed=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="30/03/2023",
    operation_time="17:26",
    operation_amount=9000,
    operation_category="VISA",
    operation_subcategory="Perfumeria",
    operation_description="Compra de 2 repelentes marca pirulo",
    other="Repelente",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=2,
    installments_payed=0,
    is_active=1,
)
t1 = time.time() - t0
print(f"tarde {t1:.2f} en llenar las bases de datos")

query = """
SELECT
  operation_id,
  operation_date,
  operation_time,
  operation_amount,
  installments_payed || '/' || operation_installments as installments,
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
os.remove("operationsDB.sqlite")
print("database deleted")
total = df2.installments_amount.sum()
print("A pagar el proximo vencimiento: ", f"${total:.2f}")


# first = "29/02/2024"
# for i in range(10):
#    due = calc_due_date(first, "AR", "prev")
#    first = calc_closing_date(first, "AR", "prev")
#    print(f"Cierre: {first} -> Vencimiento: {due}")
