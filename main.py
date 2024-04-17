#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019 -> Billetera.py
Refactored on Sat Sep  3 19:17:37 2022 -> main.py

@author: igna
Billetera V2.0

Cosas que quisiera ir agregándole al script:


TODO    Editor de entradas:
        Alguna manera para editar un gasto, un ingreso, o algo que fue mal
        ingresado (puede que haga falta usar archivos temporales y librerias
        afines) -> esto se puede hacer migrando todo a sql

TODO    Graficos:
        Alguna forma fácil de ver gastos/ingresos/whatever por día, por semana
        por mes, por año.

TODO    Interfaz Gráfica y ejectuable:
        09/03/2023 In progress

TODO    Implementación de presupuestos: Una función con la cual setear el
        presupuesto máximo que se quiere gastar por y/o por categoria y
        subcategoria por mes. Y que con cada gasto en esa dada categoria avise
        cuánto queda de presupuesto

TODO    Encriptación de datos con sesión cerrada.
"""

import os

import pandas as pd

from src.info import info
from src.info import precio_dolar

from src.users import log_in
from src.users import log_out
from src.users import create_user
from src.users import delete_user
from src.users import change_password

from src.accounts.accounts import create_account
from src.accounts.accounts import delete_account

from src.operations.operations import income
from src.operations.operations import expense
from src.operations.operations import extraction
from src.operations.operations import transfer
from src.operations.operations import readjustment

from src.analysis import data_filter
from src.analysis import account_balances
from src.analysis import balance_graf
from src.analysis import account_data
from src.analysis import total_balances
from src.analysis import category_spendings
from src.analysis import monthly_categorical_spendings


pd.set_option("display.max_columns", 11)

if __name__ == "__main__":
    users_list = [user for user in os.listdir() if "USR" in user]
    if len(users_list) == 0:
        crear_usuario = create_user
        eliminar_usuario = delete_user
        cambiar_password = change_password
        iniciar_sesion = log_in
        cerrar_sesion = log_out

        crear_cuenta = create_account
        eliminar_cuenta = delete_account

        ingreso = income
        gasto = expense
        extraccion = extraction
        transferencia = transfer
        reajuste = readjustment

        print(
            "Bienvenide!\nNo hay ningún usuario creado todavía.",
            "Para crear un usuario ejecute 'crear_usuario()' y siga las instrucciones.",
            "Para iniciar sesión con el usuario ejecute 'iniciar_sesion()'",
        )
    else:
        crear_usuario = create_user
        eliminar_usuario = delete_user
        cambiar_password = change_password
        iniciar_sesion = log_in
        cerrar_sesion = log_out

        crear_cuenta = create_account
        eliminar_cuenta = delete_account

        ingreso = income
        gasto = expense
        extraccion = extraction
        transferencia = transfer
        reajuste = readjustment
        iniciar_sesion()
