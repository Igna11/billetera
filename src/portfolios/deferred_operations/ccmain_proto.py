#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd

from db_handlers import create_connection, insert_new_operation
from data_updaters import (
    auto_update_cc_closingdue_dates_table,
    update_is_active,
)
from asyncinputs_proto import new_cc, edit_cc, remove_cc, new_cc_operation

# from operations_saver import list_expenses, list_active_expenses, expense_writer

FORMAT = "%d/%m/%Y"
PATH = "./operationsDB.sqlite"


def print_active_operations(connection, cc_id: int = 2455) -> pd.DataFrame:
    """
    docstring
    """
    query = f"""
    SELECT
      operation_id, operation_date, operation_time, operation_amount,
      installments_paid || '/' || operation_installments as installments,
      installments_amount, card_closing_date, operation_description
    FROM
      credit_card_operations
    JOIN
      credit_cards
    ON
      credit_card_operations.operation_card_id = credit_cards.card_id
    WHERE
    (
      operation_card_id = {cc_id}
      AND operation_card_brand = 'VISA'
      AND is_active = 1
    );
    """
    return pd.read_sql_query(query, connection)


def print_next_payment(connection, cc_id: int = 2455) -> float:
    """
    docstring
    """
    df = print_active_operations(connection, cc_id)
    return round(df.installments_amount.sum(), 2)


if __name__ == "__main__":
    if "operationsDB.sqlite" in os.listdir():
        print("Data base located")
        connection = create_connection(PATH)
        print("connection with database stablished")

        auto_update_cc_closingdue_dates_table(connection)
        update_is_active(connection)
