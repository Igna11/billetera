#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 09/02/2023
"""
import os

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QMainWindow
from source import errors
from guicore import users_gui
from guicore import welcomescreen
from guicore import operationscreen

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class CreateUserScreen(QMainWindow):
    """
    UI where the users can create a new account with an e-mail, user name, and password
    """

    def __init__(self, parent=None, widget=None):
        super(CreateUserScreen, self).__init__(parent)
        create_user_screen = os.path.join(GUI_PATH, "create_user_screen.ui")
        loadUi(create_user_screen, self)
        self.widget = widget
        self.password_line.setEchoMode(QLineEdit.Password)
        self.confirm_password_line.setEchoMode(QLineEdit.Password)
        self.signup_button.clicked.connect(self.sign_up)
        self.back_button.clicked.connect(self.back)
        self.usr_created_msg = QMessageBox()

    def sign_up(self):
        """Creates the user: saves it into the database and creates the directories"""
        username = self.user_name_line.text()
        useremail = self.email_line.text()
        password = self.password_line.text().encode("utf-8")
        password_check = self.confirm_password_line.text().encode("utf-8")
        print(type(password))
        try:
            users_gui.create_user(username, useremail, password, password_check)
            self.create_user_label.setText(
                f"<font color='green'>User {username} successfully created.</font>"
            )
            popup_message = self.usr_created_msg.question(
                self,
                f"User created!.",
                f"User {username} successfully created!\nDo you want to log in?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if popup_message == QMessageBox.Yes:
                self.login(username, password)

            if popup_message == QMessageBox.No:
                self.back()
        except errors.PasswdsDontMatchError:
            self.create_user_label.setText(f"<font color='red'>Passwords do not match.</font>")
        except errors.UserAlreadyExistsError:
            self.create_user_label.setText(
                f"<font color='red'>User {username} already exists.</font>"
            )
        except errors.InvalidEmailError:
            self.create_user_label.setText(
                f"<font color='red'>Invalid format email: <b>{useremail}</b></font>"
            )

    def login(self, username, password):
        """Logs in and takes the user to the OperationScreen menu."""
        users_gui.login(username, password)
        operation_screen = operationscreen.OperationScreen(widget=self.widget)
        self.widget.addWidget(operation_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def back(self):
        """Returns to the WelcomeScreen."""
        welcome = welcomescreen.WelcomeScreen(widget=self.widget)
        self.widget.addWidget(welcome)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        """Returns to the WelcomeScreen when Esc Key is pressed."""
        if e.key() == QtCore.Qt.Key_Escape:
            welcome = welcomescreen.WelcomeScreen(widget=self.widget)
            self.widget.addWidget(welcome)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
