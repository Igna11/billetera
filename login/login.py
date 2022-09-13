#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:17:33 2022

@author: igna
"""

import os
from hashlib import sha256
from pwinput import pwinput

if "passwd_list.key" not in os.listdir():
    with open("passwd_list.key", "w") as passwd_file:
        passwd_file.write("user\tpasswd\n")
        print("passwd_list.key created.")


def key_file_manipulator() -> dict:
    """Orders the data in the passwd_list.key in a simple way to manipulate."""
    # Open the file a check if the user is in the list
    with open("passwd_list.key", "r") as file:
        data = file.read()
    # Manipulates the data order it in a simple way
    data_list = data.split("\n")
    data_list.pop()
    dic = {
        "users": [elem.split("\t")[0] for elem in data_list],
        "passwd": [elem.split("\t")[1] for elem in data_list],
    }
    return dic


def check_user(user: str) -> bool:
    """
    Checks if the given user already exists in the passwd_list.key file
    """
    dic = key_file_manipulator()
    if user in dic["users"]:
        return True


def create_user() -> None:
    """
    Creates a password and saves it encrypted in the password_list.key file.
    """
    user = input("Introduce UserName:\n")
    # Checking users existance
    flag = check_user(user)
    if flag:
        print("User already exists.")
        return
    # Password input and encode to utf-8
    passwd = pwinput(prompt="Password: ").encode("utf-8")
    # Encryptation of the password using sha256 algorithm
    encrypted_passwd = sha256(passwd).hexdigest()
    # Saving the password in a plain text file
    with open("passwd_list.key", "a") as file:
        text = f"{user}\t{encrypted_passwd}\n"
        file.write(text)


def passwd_validation(user: str, passwd: bytes) -> bool:
    """
    Checks if the given passwd is correct comparing its hash with the one saved
    in the passwd_list.key file
    """
    dic = key_file_manipulator()
    # Password to validate is hashed in order to be compared with the
    # one in passwd_list.key file.
    hash_pass = sha256(passwd).hexdigest()
    # Numerical index of the given user is retrieved to be used when
    # calling the adecuated hashed password in the file
    user_idx = dic["users"].index(user)
    # The password hashed and given as input is compared with the hashed
    # stored one, if they match, a True flag is returned
    if dic["passwd"][user_idx] == hash_pass:
        return True


def login() -> None:
    """dummy login function"""
    user = input("Enter user name: ")
    if not check_user(user):
        print("User does not exists")
        return
    password = pwinput("Enter password: ").encode("utf-8")

    if passwd_validation(user, password):
        print("Login successfuly")
    else:
        print("wrong password, try again using login() function")


if __name__ == "__main__":

    login()
