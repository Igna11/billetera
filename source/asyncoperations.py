#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue 13 Feb 15:35 2024

@author: igna

idea: Este modulo debería poder generarme un "Informe" de los gastos diferidos
que haga, ya sea con tarjeta o que sean fijos.
Ejemplo: Gasto diferido sería un pago con tarjeta de crédito en un pago o varias cuotas
Ejemplo: Gasto fijo sería el alquiler que todos los meses tengo que pagar

Problema: Como los gastos diferidos no impactan de inmediato, es dificil llevar un control
de los mismos: Anoto el gasto en el momento aunque en el banco no se haya debitado? Lo anoto
recién cuando se me debita? Eso hace que me sea dificil recordar en qué gaste.
Además, los gastos diferidos representan EN LA VIDA REAL un problema de control de dinero
gastado. Es decir: No es claro cuánto llevo gastado este mes, el que viene, o dentro de 
dos meses (si es que use cuotas).

Este modulo deberia poder venir a solucionar eso llevando el tracking de todos mis gastos
fijos y diferidos y avisarme cuánto llevo acumulado de gasto para pagar en las fechas de
vencimiento.

Para el caso de las tarjetas de crédito, que es el principal problema a solucionar ahora
voy a necesitar guardar de alguna manera la fecha en la que realizo la compra de algo,
la fecha de vencimiento de la tarjeta, que sería cuándo se realiza el pago, la cantidad
de cuotas, el monto y la descripción del gasto.

El resultado final deberia ser ALGO que me sepa decir: 
    "Hasta ahora llevas acumulado $XXXXX a vencer xx/xx/2024"
y tener la opción de poder ver todos los meses siguientes hasta donde siga teniendo los
gastos.

Ademnás, superado el día de vencimiento deberia poder "consumar" el gasto de forma
semiautomatica. Algo asi como un cartel que diga "ayer vencio tu tarjeta visa y tenias que
pagar tanto por esto. Pagado, No Pagado. Si es Pagado, se guarda en los csvs la data, si
es No pagado, sigue quedando pendiente. En ese caso necesitaria una UI donde pueda ver 
los pendientes vencidos y por vencer de forma de poder pagarlos antes o después si es
necesario.
"""
import os
import sqlite3 as sql
from sqlite3 import Error


def create_connection(path: str) -> sql.connect:
    """Creates the connection to the data base"""
    connection = None
    try:
        connection = sql.connect(path)
    except Error as e:
        print(f"The error {e} ocurred")
    return connection


def execute_query(connection: sql.connect, query: str, verbose=False) -> None:
    """Function to execute different queries into the data base."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if verbose:
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection: sql.connect, query: str) -> list[tuple]:
    """
    Executes a read query and returns a list of tuples for every line in the table.
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def insert_new_cc(
    connection: sql.connect,
    id: int,
    brand: str,
    issuer: str,
    expdate: str,
    cdate: str,
    ddate: str,
) -> None:
    """Executes a query into the database to add a new credit card"""
    cursor = connection.cursor()
    query = """
    INSERT INTO 
      credit_cards (card_id, card_brand, card_issuer, card_expiration, card_closing_date, card_due_date)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        cursor.execute(query, (id, brand, issuer, expdate, cdate, ddate))
        connection.commit()
    except Error as e:
        print(f"The error '{e}' ocurred.")


def update_cc(connection: sql.connect, id: int, **kwargs):
    """
    Updates the table credit_cards based on the card id and kwargs.
    """
    headers = list(kwargs.keys())
    values = tuple(kwargs.values())
    set_clause = ", ".join([f"{header} = ?" for header in headers])
    query = f"""
    UPDATE credit_cards
    SET {set_clause}
    WHERE card_id = {id}
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' ocurred.")


def delete_cc(connection: sql.connect, id: int, brand: str, issuer: str) -> None:
    cursor = connection.cursor()
    query = """
    DELETE FROM 
      credit_cards
    WHERE card_id = ? AND card_brand = ? AND card_issuer = ?;
    """
    try:
        cursor.execute(query, (id, brand, issuer))
        connection.commit()
    except Error as e:
        print(f"The error '{e}' ocurred.")


def insert_new_operation(
    connection: sql.connect,
    operation_date: str,
    operation_time: str,
    operation_amount: float,
    operation_category: str,
    operation_subcategory: str,
    operation_description: str,
    other: str,
    operation_card_id: int,
    operation_card_brand: str,
    operation_installments: int,
    installments_payed: int,
    is_active: int,
):
    """docstring"""
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO
          credit_card_operations (operation_date, operation_time, operation_amount, operation_category, operation_subcategory, operation_description, other, operation_card_id, operation_card_brand, operation_installments, installments_payed, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            operation_date,
            operation_time,
            operation_amount,
            operation_category,
            operation_subcategory,
            operation_description,
            other,
            operation_card_id,
            operation_card_brand,
            operation_installments,
            installments_payed,
            is_active,
        ),
    )
    connection.commit()


def update_operation(connection: sql.connect, operation_id: int, **kwargs):
    """
    Updates the table credit_card_operations based on operation_id and kwargs.
    """
    headers = list(kwargs.keys())
    values = tuple(kwargs.values())
    set_clause = ", ".join([f"{header} = ?" for header in headers])
    query = f"""
    UPDATE credit_card_operations
    SET {set_clause}
    WHERE operation_id = {operation_id}
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' ocurred.")
