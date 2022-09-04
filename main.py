#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 19:17:37 2022

@author: igna
Billetera V2.0

Cosas que quisiera ir agregándole al script:


TODO    Editor de entradas:
        Alguna manera para editar un gasto, un ingreso, o algo que fue mal
        ingresado (puede que haga falta usar archivos temporales y librerias
        afines)

TODO    Graficos:
        Alguna forma fácil de ver gastos/ingresos/whatever por día, por semana
        por mes, por año.

TODO    Interfaz Gráfica y ejectuable:
        nada, eso, a futuro (lejano)

TODO    Que no se pueda crear usuario estando logueado en algún usuario

TODO    Separar todo este script en módulos. -> EN PROCESO 03/09/2022

TODO    Que no se puedan hace transferencias de cuentas de distintos tipos
        (de pesos a dolares o dolares a pesos)

TODO    Implementación de presupuestos: Una función con la cuál setear el
        presupuesto máximo que se quiere gastar por y/o por categoria y
        subcategoria por mes. Y que con cada gasto en esa dada categoria avise
        cuánto queda de presupuesto

"""


from source.users import iniciar_sesion

if __name__ == "__main__":
    iniciar_sesion()
