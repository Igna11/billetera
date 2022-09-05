#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sept 03 19:21:22 2022

@author: igna
Módulo para condensar las funciones relacionadas con cuentas

crear_usuario()
eliminar_usuario()
iniciar_sesion()
cerrar_sesion()
"""
import os

import pandas as pd

from source.info import info
from source.misc import extra_char_cleaner

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
os.chdir(DATA_PATH)
pd.set_option("display.max_columns", 11)


def crear_usuario():
    """Creates the user's directory where all accounts will be stored"""
    if os.getcwd() != DATA_PATH:
        print(
            "No se puede crear usuario si está iniciada una sesión",
            "Asegúrese de haber deslogueado y vuelva a intentar.",
        )
    elif os.getcwd() == DATA_PATH:
        folder_name = input("\nIngrese el nombre de usuario\n") + "USR"
        user_name = extra_char_cleaner(folder_name)
        if os.path.isdir(folder_name):
            print(f"\nYa existe el usuario '{user_name}'\n")
        else:
            os.makedirs(folder_name)
            print(f"\nSe creo el usuario '{user_name}'\n")


def eliminar_usuario():
    """
    Delets the directory of the given user, including all data stored in it
    """
    if os.getcwd() != DATA_PATH:
        print("Debes cerrar sesion para eliminar un usuario.")
    elif os.getcwd() == DATA_PATH:
        folder_name = (
            input("\nIngrese el nombre de usuario a borrar\n") + "USR"
        )
        user_name = extra_char_cleaner(folder_name)
        if os.path.isdir(folder_name):
            advertencia = (
                f"¿Seguro que queres eliminar el usuario '{user_name}'?\n\n"
                "todos los datos contenidos en él se perderán para siempre.\n\n"
                "Ingrese '1', 'si' o 'y' para borrar\n"
                "Ingrese cualquier otra cosa para cancelar\n"
            )
            respuesta = input(advertencia)
            posibles_respuestas = ["1", "si", "y"]
            if respuesta in posibles_respuestas:
                try:
                    os.rmdir(folder_name)
                    print(f"\nSe eliminó el usuario {user_name}\n")
                except OSError:
                    from shutil import rmtree

                    rmtree(folder_name)
                    print(
                        f"\nSe eliminó el usr. {user_name} y todos sus datos."
                    )
            else:
                print(f"\nNo se eliminó el usuario {user_name}\n")
        else:
            print(f"\nNo existe el usuario {user_name}\n")


def iniciar_sesion():
    """Changes the current working directory to the user's directory"""
    if "USR" in os.getcwd():
        print("Ya hay una sesión iniciada")
    else:
        folder_name = input("\nNombre de usuario\n") + "USR"
        user_name = extra_char_cleaner(folder_name)
        if os.path.isdir(folder_name):
            path = os.path.join(DATA_PATH, folder_name)
            os.chdir(path)
            print(f"\nInicio de sesion de {user_name}\n")
            info(verbose=True)
        else:
            print(f"\nNo existe el usuario '{user_name}'\n")


def cerrar_sesion():
    """Changes the current working directory to the base directory"""
    if "USR" not in os.getcwd():
        print("No hay ninguna sesión iniciada.")
    else:
        os.chdir(DATA_PATH)
        print("\nSe ha cerrado sesión\n")
