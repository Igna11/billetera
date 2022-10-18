#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 23:28:50 2022

@author: igna
"""

import sqlite3 as sql
from sqlite3 import Error


def create_connection(path: str, verbose=False) -> sql.connect:
    """Creates the connection to the data base"""
    connection = None
    try:
        connection = sql.connect(path)
        if verbose:
            print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection: sql.connect, query: str, verbose=False) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if verbose:
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection: sql.connect, query: str) -> None:
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def add_new_user_query(user: str, pwhash: str) -> str:
    query = f"""
    INSERT INTO 
      users (name, passwd)
    VALUES
      ('{user}', '{pwhash}')
    """
    return query


def remove_user_query(user: str) -> str:
    query = f"""
    DELETE FROM 
      users
    WHERE name = '{user}'; 
    """
    return query


def change_pass_query(user: str, new_pass: str) -> str:
    query = f"""
    UPDATE users
    SET passwd = '{new_pass}'
    WHERE name = '{user}';
    """
    return query
