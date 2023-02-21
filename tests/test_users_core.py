#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 11:10:00 2022

@author: igna
"""
import os
import unittest
from source import users_core
from source import sqlpasswd as sql
from source import errors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_BASE = os.path.join(BASE_DIR, "data", "passwords.sqlite")


class TestUserDB(unittest.TestCase):
    """Test for the functions inside the class UsersDB"""

    def test_user_name(self):
        """Tests that the user name is correct"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        self.assertEqual(user.user, "Test_User")

    def test_user_not_exists(self):
        """User should not exist yet"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        self.assertEqual(user.user_exists, False)

    def test_user_not_creationstatus(self):
        """User should not be created yet"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        self.assertEqual(user.creation_status, False)

    def test_user_not_passwdvalidation(self):
        """There should not be a passwd yet"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        self.assertEqual(user.passwdvalidation, False)

    def test_user_not_getuserfromdb(self):
        """Test_User should not be in the DB yet"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        self.assertEqual(user.get_user_from_db(), None)

    def test_user_not_valiremail(self):
        """Test that error InvalidEmailError is raised when an invalid email is entered"""
        with self.assertRaises(errors.InvalidEmailError):
            user = users_core.UsersDB(
                user="Test_bad_mail_user", email="badmail"
            )

    def test_user_addedtodb(self):
        """Adds Test_User to the data base and change the creation status to True"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        password = b"test_password"
        user.add_user_to_db(passwd=password)
        self.assertEqual(user.creation_status, True)
        user.get_user_from_db()
        self.assertEqual(user.user_exists, True)

    def test_user_deletedondb(self):
        """Delete Test_User from the data base"""
        user = users_core.UsersDB(user="Test_User", email="test@test.test")
        user.get_user_from_db()
        self.assertEqual(user.user_exists, True)
        if user.user_exists:
            user.delete_user_indb()
            self.assertEqual(user.user_exists, False)
            user.get_user_from_db()
            self.assertEqual(user.user_exists, False)

    def test_user_changepass(self):
        """Test the change of password"""
        user = users_core.UsersDB(
            user="Test_User_changepwd", email="test@test.test"
        )
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
        user = users_core.UsersDB(
            user="Test_User_pwdvalidation", email="test@test.test"
        )
        password = b"test_password"
        user.add_user_to_db(passwd=password)
        self.assertEqual(user.passwdvalidation, False)
        user.passwd_validation_indb(passwd=password)
        self.assertEqual(user.passwdvalidation, True)
        user.delete_user_indb()


class TestUserDirs(unittest.TestCase):
    """Test for the functions inside the class UsersDirs"""

    def test_user_name(self):
        """Tests that the user name is correct"""
        user = users_core.UsersDirs("Test_User")
        self.assertTrue(user.user == "Test_User")

    def test_user_dirname(self):
        """Tests that the name of tht directory follows the given convention"""
        user = users_core.UsersDirs("Test_User")
        self.assertTrue(user.dirname == "Test_UserUSR")

    def test_user_createdir(self):
        """Test the creation of the directory for the user"""
        user = users_core.UsersDirs("Test_User")
        user.create_user_dir()
        self.assertTrue(os.path.isabs(user.absdirname))
        self.assertTrue(os.path.isdir(user.absdirname))

    def test_user_deletedir(self):
        """Test the deletion of the directory for the user"""
        user = users_core.UsersDirs("Test_User")
        self.assertTrue(os.path.isdir(user.absdirname))
        user.delete_user_dir()
        self.assertFalse(os.path.isdir(user.absdirname))

    def test_user_login(self):
        """Test that when login the directory is the correct one"""
        user = users_core.UsersDirs("Test_User")
        user.create_user_dir()
        unloged = user.get_user_cwd()
        user.login()
        loged = user.get_user_cwd()
        self.assertTrue(unloged != user.absdirname)
        self.assertTrue(loged == user.absdirname)

    def test_user_logout(self):
        """Test the when loginout the directory is not the one of the user"""
        user = users_core.UsersDirs("Test_User")
        loged = user.get_user_cwd()
        user.logout()
        unloged = user.get_user_cwd()
        self.assertTrue(loged == user.absdirname)
        self.assertTrue(unloged != user.absdirname)
        user.delete_user_dir()


if __name__ == "__main__":
    unittest.main(argv=[""], exit=False)
