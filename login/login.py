#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:17:33 2022

@author: igna
"""

import os
from hashlib import sha256
from pwinput import pwinput

from login.sqlpasswd import create_connection
from login.sqlpasswd import execute_query
from login.sqlpasswd import execute_read_query
from login.sqlpasswd import add_new_user_query

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")

DATA_BASE = os.path.join(DATA_PATH, "passwords.sqlite")

connection = create_connection(DATA_BASE)

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  passwd TEXT NOT NULL
);
"""

execute_query(connection, create_users_table)


def check_user_indb(user: str) -> bool:
    """
    Checks if the given user already exists in the sql table.
    """
    query = f"""
    SELECT name FROM users WHERE name = '{user};'
    """
    query_result = execute_read_query(connection, query)
    if len(query_result) == 1:
        return True


def create_user_indb(user: str) -> bool:
    """
    Creates a password and saves it encrypted in sql table.
    Returns False if conditions don't match and True if they do
    """
    # Checking users existance
    flag = check_user_indb(user)
    if flag:
        print(f"User {user} already exists.")
        return False
    # Password input and encode to utf-8
    passwd = pwinput(prompt="Ingrese una password: ").encode("utf-8")
    passwd_check = pwinput(prompt="Ingrese la password otra vez: ").encode(
        "utf-8"
    )
    if passwd != passwd_check:
        print("Las contraseñas no coinciden, vuelva a intentarlo.")
        return False
    else:
        # Encryptation of the password using sha256 algorithm
        encrypted_passwd = sha256(passwd).hexdigest()
        # Saving the password in the sqlite table
        query = add_new_user_query(user, encrypted_passwd)
        execute_query(connection, query, verbose=True)
        return True


def delete_user_indb(user: str) -> None:
    """
    Deletes the row in the sql table that stores that user
    """
    query = f"DELETE FROM users WHERE name = '{user}';"
    execute_query(connection, query)


def passwd_validation_indb(user: str, passwd: bytes) -> bool:
    """
    Checks if the given passwd is correct
    """
    query = f"""
    SELECT passwd FROM users WHERE name = '{user}';
    """
    query_result = execute_read_query(connection, query)[0][0]
    # Password to validate is hashed in order to be compared with the
    # one in passwd_list.key file.
    hash_pass = sha256(passwd).hexdigest()
    # The password hashed and given as input is compared with the hashed
    # stored one, if they match, a True flag is returned
    if query_result == hash_pass:
        return True
