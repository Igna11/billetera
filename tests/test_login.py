#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 11:10:00 2022

@author: igna
"""
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_BASE = os.path.join(BASE_DIR, "data", "passwords.sqlite")

sys.path.append(BASE_DIR)

from login import login
from login import sqlpasswd as sql


class TestUserDB(unittest.TestCase):
    """Test for the functions inside the class UsersDB"""

    def test_user_name(self):
        user = login.UsersDB("Test_User")
        self.assertTrue(user.user == "Test_User")

    def test_user_not_exists(self):
        """User should not exist yet"""
        user = login.UsersDB("Test_User")
        self.assertTrue(user.user_exists == False)

    def test_user_not_creationstatus(self):
        """User should not be created yet"""
        user = login.UsersDB("Test_User")
        self.assertTrue(user.creation_status == False)

    def test_user_not_passwdvalidation(self):
        """There should not be a passwd yet"""
        user = login.UsersDB("Test_User")
        self.assertTrue(user.passwdvalidation == False)

    def test_user_not_getuserfromdb(self):
        """Test_User should not be in the DB yet"""
        user = login.UsersDB("Test_User")
        self.assertTrue(user.get_user_from_db() == None)

    def test_user_addedtodb(self):
        """Adds Test_User to the data base and change the creation status to True"""
        user = login.UsersDB("Test_User")
        password = b"test_password"
        # The user is added to the db
        user.add_user_to_db(passwd=password)
        # Checks creation status (does make sense to test this?)
        self.assertTrue(user.creation_status == True)
        # Checks if the user is actually in the DB
        user.get_user_from_db()
        self.assertTrue(user.user_exists == True)

    def test_user_deletedondb(self):
        """Delete Test_User from the data base"""
        user = login.UsersDB("Test_User")
        # Checks that the user is in the DB
        user.get_user_from_db()
        self.assertTrue(user.user_exists == True)
        # If it is, then delete the user
        if user.user_exists:
            user.delete_user_indb()
            self.assertTrue(user.user_exists == False)
            # Checks that the user is not in DB anymore using get_user_from_db
            user.get_user_from_db()
            self.assertTrue(user.user_exists == False)

    def test_user_changepass(self):
        """Test the change of password"""
        user = login.UsersDB("Test_User_changepwd")
        first_password = b"test_password"
        user.add_user_to_db(passwd=first_password)
        connection = sql.create_connection(DATA_BASE)
        query = f"SELECT passwd FROM users WHERE name = '{user.user}';"
        first_hash = sql.execute_read_query(connection, query)
        second_password = b"test_password_2"
        user.change_pass_indb(new_passwd=second_password)
        second_hash = sql.execute_read_query(connection, query)
        user.delete_user_indb()
        self.assertTrue(first_hash != second_hash)

    def test_user_passwdvalidation(self):
        """Test the validation of the passwd"""
        user = login.UsersDB("Test_User_pwdvalidation")
        password = b"test_password"
        user.add_user_to_db(passwd=password)
        # Check that validation don't match
        self.assertTrue(user.passwdvalidation == False)
        # Check that validation do match
        user.passwd_validation_indb(passwd=password)
        self.assertTrue(user.passwdvalidation == True)
        # Removes the user from db
        user.delete_user_indb()


class TestUserDirs(unittest.TestCase):
    """Test for the functions inside the class UsersDirs"""

    def test_user_name(self):
        user = login.UsersDirs("Test_User")
        self.assertTrue(user.user == "Test_User")

    def test_user_dirname(self):
        user = login.UsersDirs("Test_User")
        self.assertTrue(user.dirname == "Test_UserUSR")

    def test_user_createdir(self):
        """Test the creation of the directory for the user"""
        user = login.UsersDirs("Test_User")
        user.create_user_dir()
        # Checks that the path is an absolute path
        self.assertTrue(os.path.isabs(user.absdirname))
        # Checks if the absolute path exists
        self.assertTrue(os.path.isdir(user.absdirname))

    def test_user_deletedir(self):
        """Test the deletion of the directory for the user"""
        user = login.UsersDirs("Test_User")
        # Checks that the directory still exists
        self.assertTrue(os.path.isdir(user.absdirname))
        # Once deleted, check that the directory doesn't exist anymore
        user.delete_user_dir()
        self.assertFalse(os.path.isdir(user.absdirname))

    def test_user_login(self):
        """Test that when login the directory is the correct one"""
        user = login.UsersDirs("Test_User")
        user.create_user_dir()
        unloged = user.get_user_cwd()
        user.login()
        loged = user.get_user_cwd()
        # Checks the unloged state:
        self.assertTrue(unloged != user.absdirname)
        # Checks the loged state:
        self.assertTrue(loged == user.absdirname)

    def test_user_logout(self):
        """Test the when loginout the directory is not the one of the user"""
        user = login.UsersDirs("Test_User")
        loged = user.get_user_cwd()
        user.logout()
        unloged = user.get_user_cwd()
        # Checks the loged state:
        self.assertTrue(loged == user.absdirname)
        # Checks the unloged state:
        self.assertTrue(unloged != user.absdirname)
        user.delete_user_dir()


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
