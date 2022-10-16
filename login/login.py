#!/usr/bin/env python3
# login# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:17:33 2022

@author: igna

refactor: Sun Oct 16 16:00:00
"""

import os
from hashlib import sha256

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


class UsersDB:
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
        query_result = execute_read_query(connection, query)
        print(query_result)
        if len(query_result) == 1:
            self.user_exists = True

    def add_user_to_db(self, passwd: bytes) -> None:
        """
        Adds the user and hashed passwd to the sql table.
        Returns False if conditions don't match and True if they do
        """
        # Encryptation of the password using sha256 algorithm
        encrypted_passwd = sha256(passwd).hexdigest()
        # Saving the user and password in the sqlite table
        query = add_new_user_query(self.user, encrypted_passwd)
        execute_query(connection, query, verbose=True)
        self.creation_status = True

    def delete_user_indb(self) -> None:
        """
        Deletes the row in the sql table that stores that user
        """
        query = f"DELETE FROM users WHERE name = '{self.user}';"
        execute_query(connection, query)
        self.user_exists = False

    def change_pass_indb(self, new_passwd: bytes) -> None:
        """
        Changes the password hash of a given user
        """
        hash = sha256(new_passwd).hexdigest()
        query = (
            f"UPDATE users SET passwd = '{hash}' WHERE name = '{self.user}';"
        )
        execute_query(connection, query)

    def passwd_validation_indb(self, passwd: bytes) -> bool:
        """
        Checks if the given passwd is correct
        """
        query = f"SELECT passwd FROM users WHERE name = '{self.user}';"
        query_result = execute_read_query(connection, query)[0][0]
        # Password to validate is hashed in order to be compared with the
        # one in passwd_list.key file.
        hash_pass = sha256(passwd).hexdigest()
        # The password hashed and given as input is compared with the hashed
        # stored one, if they match, a True flag is returned
        if query_result == hash_pass:
            self.passwdvalidation = True


class UsersDirs:    
    def __init__(self, user):
        self.user = user
        self.dirname = user + "USR"
        self.absdirname = DATA_PATH + "/" + self.dirname

    def get_user_cwd(self) -> None:
        return os.getcwd()

    def create_user_dir(self) -> None:
        """creates the directory for the user's accounts"""
        os.makedirs(self.absdirname)
    
    def delete_user_dir(self) -> None:
        """Deletes the directory and all its content"""
        try:
            os.rmdir(self.absdirname)
        except OSError:
            from shutil import rmtree
            rmtree(self.absdirname)
    
    def login(self) -> None:
        """Changes the current working directory to the one of the user"""
        os.chdir(self.absdirname)
    
    def logout(self) -> None:
        """Chages the current working directory to tha data directory"""
        os.chdir(DATA_PATH)