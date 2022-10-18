#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sept 03 19:21:22 2022

@author: igna
Módulo para condensar las funciones relacionadas con cuentas

crear_usuario()
eliminar_usuario()
cambiar_contraseña()
iniciar_sesion()
cerrar_sesion()

refactor: Sun Oct 16 16:00:00
"""
import os

import pandas as pd
from pwinput import pwinput

from source import info
from login import login

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
os.chdir(DATA_PATH)
pd.set_option("display.max_columns", 11)


def crear_usuario() -> None:
    """
    Creates an user with its directories and entries in the data base.
    Uses inputs for name of the user and password.
    Won't allow you to create an user if it already existis or if you are
    logged in with another users.s
    """
    if os.getcwd() == DATA_PATH:
        username = input("\nIngrese el nombre de usuario\n")
        user_dir = login.UsersDirs(username)
        user_db = login.UsersDB(username)
        if not os.path.isdir(user_dir.absdirname):
            # Password input and encode to utf-8
            password = pwinput(prompt="Ingrese una password: ").encode("utf-8")
            password_check = pwinput(
                prompt="Ingrese la password otra vez: "
            ).encode("utf-8")
            if password == password_check:
                user_dir.create_user_dir()
                user_db.add_user_to_db(passwd=password)
                if user_db.creation_status:
                    print(f"\nSe creo el usuario '{username}'\n")
                else:
                    print(
                        "\nFalló la creación del usuario en la base de datos\n"
                    )
            else:
                print("Las contraseñas no coinciden, vuelva a intentarlo.")
        else:
            print(f"\nYa existe el usuario '{username}'\n")
    else:
        print(
            "No se puede crear usuario si está iniciada una sesión",
            "Asegúrese de haber deslogueado y vuelva a intentar.",
        )


def eliminar_usuario() -> None:
    """
    Deletes an user and all its information stored in its directories and
    data base.
    Ues inputs for name of the user and password.
    Won't allow you to delete an user if you are logged in with that or
    another user.
    """
    if os.getcwd() == DATA_PATH:
        username = input("\nIngrese el nombre de usuario a borrar\n")
        user_dir = login.UsersDirs(username)
        user_db = login.UsersDB(username)
        if os.path.isdir(user_dir.absdirname):
            password = pwinput("Enter password: ").encode("utf-8")
            user_db.passwd_validation_indb(passwd=password)
            if user_db.passwdvalidation:
                warning = (
                    f"¿Seguro que queres eliminar el usuario '{username}'?\n\n"
                    "todos los datos contenidos en él se perderán para siempre.\n\n"
                    "Ingrese '1', 'si' o 'y' para borrar\n"
                    "Ingrese cualquier otra cosa para cancelar\n"
                )
                user_answer = input(warning)
                valid_answers = ["1", "si", "y"]
                if user_answer in valid_answers:
                    user_dir.delete_user_dir()
                    user_db.delete_user_indb()
                else:
                    print(f"\nNo se eliminó el usuario {username}\n")
            else:
                print("\nPassword incorrecta\n")
        else:
            print(f"\nNo existe el usuario {username}\n")
    else:
        print("Debes cerrar sesion para eliminar un usuario.")


def cambiar_contraseña() -> None:
    """
    Changes the password of a given user.
    Uses inputs for name of the user, old password and new password.
    """
    if os.getcwd() == DATA_PATH:
        username = input(
            "\nIngrese el nombre de usuario para cambiar passwd.\n"
        )
        user_dir = login.UsersDirs(username)
        user_db = login.UsersDB(username)
        if os.path.isdir(user_dir.absdirname):
            old_password = pwinput("\nIngrese la contraseña actual: ").encode(
                "utf-8"
            )
            user_db.passwd_validation_indb(passwd=old_password)
            if user_db.passwdvalidation:
                new_password = pwinput(
                    "\nIngrese la nueva contraseña: "
                ).encode("utf-8")
                check_new_password = pwinput(
                    "\nIngrese nuevamente la nueva contraseña: "
                ).encode("utf-8")
                if new_password == check_new_password:
                    user_db.change_pass_indb(new_passwd=new_password)
                    print("\nLa contraseña fue cambiada con exito\n")
                else:
                    print(
                        "\nLas contraseñas no coinciden! Vuelva a intentar.\n"
                    )
            else:
                print("\nPassword incorrecta, vuelva a intentarlo\n")
        else:
            print(f"\nNo existe el usuario {username}\n")
    else:
        print("\nDebes cerrar sesion para cambiar una contraseña.\n")


def iniciar_sesion(verbose=True) -> None:
    """Changes the current working directory to the user's directory"""
    if os.getcwd() == DATA_PATH:
        username = input("\nNombre de usuario\n")
        user_dir = login.UsersDirs(username)
        user_db = login.UsersDB(username)
        if os.path.isdir(user_dir.absdirname):
            password = pwinput("Enter password: ").encode("utf-8")
            user_db.passwd_validation_indb(password)
            if user_db.passwdvalidation:
                os.chdir(user_dir.absdirname)
                print(f"\nInicio de sesion de {username}\n")
                info.info(verbose=verbose)
            else:
                print("Contraseña incorrecta")
        else:
            print(f"\nNo existe el usuario '{username}'\n")
    elif "USR" in os.getcwd():
        print("\nYa hay una sesión iniciada.\n")
    else:
        print(f"\nUbicación inválida: {os.getcwd()}\n")


def cerrar_sesion():
    """Changes the current working directory to the base directory"""
    if "USR" in os.getcwd():
        os.chdir(DATA_PATH)
        print("\nSe ha cerrado sesión\n")
    else:
        print("\nNo hay ninguna sesión iniciada.\n")
