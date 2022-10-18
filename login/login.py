#!/usr/bin/env python3
# login# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:17:33 2022

@author: igna

refactor: Sun Oct 16 16:00:00
"""

import os
from hashlib import sha256

from login import sqlpasswd as sql

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
DATA_BASE = os.path.join(DATA_PATH, "passwords.sqlite")

connection = sql.create_connection(DATA_BASE)

CREATE_USER_TABLE = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  passwd TEXT NOT NULL
);
"""

sql.execute_query(connection, CREATE_USER_TABLE)


class UsersDB:
    """
    All necessary operation in database to create users and store passwords,
    modify passwords and delete users and passwords.
    """
    def __init__(self, user):
        self.user = user
        self.user_exists = False
        self.creation_status = False
        self.passwdvalidation = False

    def get_user_from_db(self) -> bool:
        """
        Checks if the given user already exists in the sql table.
        """
        query = f"SELECT name FROM users WHERE name = '{self.user}';"
        query_result = sql.execute_read_query(connection, query)
        print(query_result)
        if len(query_result) == 1:
            self.user_exists = True

    def add_user_to_db(self, passwd: bytes) -> None:
        """
        Adds the user and hashed passwd to the sql table.
        Returns False if conditions don't match and True if they do
        """
        encrypted_passwd = sha256(passwd).hexdigest()
        query = sql.add_new_user_query(self.user, encrypted_passwd)
        sql.execute_query(connection, query, verbose=True)
        self.creation_status = True

    def delete_user_indb(self) -> None:
        """
        Deletes the row in the sql table that stores that user
        """
        query = f"DELETE FROM users WHERE name = '{self.user}';"
        sql.execute_query(connection, query)
        self.user_exists = False

    def change_pass_indb(self, new_passwd: bytes) -> None:
        """
        Changes the password hash of a given user
        """
        hash = sha256(new_passwd).hexdigest()
        query = (
            f"UPDATE users SET passwd = '{hash}' WHERE name = '{self.user}';"
        )
        sql.execute_query(connection, query)

    def passwd_validation_indb(self, passwd: bytes) -> bool:
        """
        Checks if the given passwd is correct
        """
        query = f"SELECT passwd FROM users WHERE name = '{self.user}';"
        query_result = sql.execute_read_query(connection, query)[0][0]
        hash_pass = sha256(passwd).hexdigest()
        if query_result == hash_pass:
            self.passwdvalidation = True


class UsersDirs:
    """
    All necessary methods to create the needed directories to store the users's
    account information.
    """
    def __init__(self, user):
        self.user = user
        self.dirname = user + "USR"
        self.absdirname = DATA_PATH + "/" + self.dirname

    def get_user_cwd(self) -> None:
        """Gets the current working directory."""
        return os.getcwd()

    def create_user_dir(self) -> None:
        """Creates the directory for the user's accounts."""
        os.makedirs(self.absdirname)

    def delete_user_dir(self) -> None:
        """Deletes the directory and all its content."""
        try:
            os.rmdir(self.absdirname)
        except OSError:
            from shutil import rmtree

            rmtree(self.absdirname)

    def login(self) -> None:
        """Changes the current working directory to the one of the user."""
        os.chdir(self.absdirname)

    def logout(self) -> None:
        """Chages the current working directory to tha data directory."""
        os.chdir(DATA_PATH)
