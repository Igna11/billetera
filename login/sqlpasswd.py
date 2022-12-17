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
    """Function to execute different queries into the data base."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        if verbose:
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection: sql.connect, query: str) -> list[tuple]:
    """
    Executes a read query and returns a list of tuples for every line in the table.
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def add_new_user_query(user: str, email: str, pwhash: str) -> str:
    """
    Generates the query to be executed to add a new user to the data base.
    Inputs:
        user: str the user name
        email: str the user email
        pwhash: str the password transformed into a hash with sha256
    returns:
        query: str of the query.
    """
    query = f"""
    INSERT INTO 
      users (name, email, passwd)
    VALUES
      ('{user}','{email}', '{pwhash}')
    """
    return query


def remove_user_query(user: str) -> str:
    """
    Generates the query to be executed to remove a user of the data base.
    This function does not make any validation so be careful when removing
    users from the data base.
    Inputs:
        user: str the user name
    returns:
        query: str of the query.
    """
    query = f"""
    DELETE FROM 
      users
    WHERE name = '{user}'; 
    """
    return query


def change_pass_query(user: str, new_pass: str) -> str:
    """
    Generates the query to be executed when a change of password is needed.
    This function does not make any validation so be careful when changing
    password.
    Inputs:
        user: str the user name
        new_pass: the hashed new password (with sha256 algorithm)
    returns:
        query: str of the query.
    """
    query = f"""
    UPDATE users
    SET passwd = '{new_pass}'
    WHERE name = '{user}';
    """
    return query
