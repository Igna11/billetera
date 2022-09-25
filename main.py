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
        nada, eso, a futuro (lejano)

TODO    Implementación de presupuestos: Una función con la cual setear el
        presupuesto máximo que se quiere gastar por y/o por categoria y
        subcategoria por mes. Y que con cada gasto en esa dada categoria avise
        cuánto queda de presupuesto

TODO    Modulo de inicio de sesión con contraseña. -> done
                Implementar base de datos para guardar contraseñas -> done
                Implementar cambio de contraseña -> done

TODO    Encriptación de datos con sesión cerrada.

TODO    Tests automaticos

"""
from source.info import info

from source.misc import users_list

from source.users import iniciar_sesion
from source.users import cerrar_sesion
from source.users import crear_usuario
from source.users import eliminar_usuario
from source.users import cambiar_contraseña

from source.accounts import crear_cuenta
from source.accounts import eliminar_cuenta

from source.operations import gasto
from source.operations import ingreso
from source.operations import transferencia
from source.operations import reajuste

from source.analysis import filtro
from source.analysis import balances_cta
from source.analysis import balance_graf
from source.analysis import datos_cuenta
from source.analysis import balances_totales
from source.analysis import category_spendings

if __name__ == "__main__":

    if len(users_list()) == 0:
        print(
            "Bienvenide!\nNo hay ningún usuario creado todavía.",
            "Para crear un usuario ejecute 'crear_usuario()' y siga las instrucciones.",
            "Para iniciar sesión con el usuario ejecute 'iniciar_sesion()'",
        )
    else:
        iniciar_sesion()
