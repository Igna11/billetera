#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aasd
"""
from datetime import datetime

from ccclosingduedates import calc_closing_date, calc_due_date, closing_date_gen
from db_handlers import update_cc, execute_read_query, update_operation

FORMAT = "%d/%m/%Y"


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
    data = execute_read_query(connection, read_query)
    # A : [(card_id, closing_date, due_date),(card_id, closing_date, due_date),..]
    for tup in data:
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
        for i in range(installments):
            prev_cdate = next(gen_cdate)

        # Case A: cd < dd and pd < cd - N (prev_cdate == N)
        prev_cdatetime = datetime.strptime(prev_cdate, FORMAT)
        if cdatetime < ddatetime and pdatetime < prev_cdatetime:
            active = 0

        prev_cdate = next(gen_cdate)
        prev_cdatetime = datetime.strptime(prev_cdate, FORMAT)

        # Case B: dd < cd and pd < cd - (N + 1)
        if ddatetime < cdatetime and pdatetime < prev_cdatetime:
            active = 0
        update_operation(connection, id, is_active=active)


def update_installments_paid(connection, operation_id: int) -> None:
    """
    Increments the number of installments paid by 1
    """
    read_query = f"""
    SELECT 
      installments_paid 
    FROM 
      credit_card_operations
    WHERE
      operation_id = {operation_id};"""
    data = execute_read_query(connection, read_query)
    data = data[0][0] + 1
    update_operation(connection, operation_id, installments_paid=data)
