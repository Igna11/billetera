#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import pandas as pd

from src.portfolios import operations

from db_handlers import execute_read_query


def list_expenses(connection, operation_card_id: int) -> list:
    query = f"""
        SELECT * FROM credit_card_operations
        WHERE operation_card_id = {operation_card_id}"""
    data = execute_read_query(connection, query)
    return data


def list_active_expenses(connection, operation_card_id: int) -> list:
    query = f"""
        SELECT * FROM credit_card_operations
        WHERE operation_card_id = {operation_card_id}
        AND is_active=1"""
    data = execute_read_query(connection, query)
    return data


def expense_writer(
    connection,
    expense_data_tuple: tuple,
    operation_card_id: int,
    acc_name: str,
    acc_currency: str,
    test_mode: bool,
) -> None:
    (
        op_id,
        op_date,
        op_time,
        op_amount,
        op_cat,
        op_subcat,
        op_desc,
        other,
        card_id,
        brand,
        op_installments,
        op_installments_paid,
        op_installments_amount,
        is_active,
    ) = expense_data_tuple
    description = f"""
    {op_desc}: fecha compra: {op_date}, vencimiento: ,cuota: {op_installments_paid+1}/{op_installments}
    """
    category = op_cat
    subcategory = op_subcat
    value = op_installments_amount
    operations.expense(
        value, acc_name, acc_currency, category, subcategory, description, test_mode
    )
