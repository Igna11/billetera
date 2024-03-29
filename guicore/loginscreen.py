#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 08/02/2023
"""
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

from source import errors
from guicore import users_gui
from guicore import welcomescreen
from guicore import operationscreen

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class LoginScreen(QMainWindow):
    """
    UI where the users can log in with their accounts using their credentials.
    """

    def __init__(self, parent=None, widget=None):
        super(LoginScreen, self).__init__(parent)
        login_screen = os.path.join(GUI_PATH, "login_screen.ui")
        loadUi(login_screen, self)
        self.widget = widget
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.returnPressed.connect(self.login)
        self.user_name_line.returnPressed.connect(self.login)
        self.login_button.clicked.connect(self.login)
        self.back_button.clicked.connect(self.back)

    def login(self):
        """Logs in the user and takes them to the OperationScreen menu."""
        user_name = self.user_name_line.text()
        password = self.password_line.text().encode("utf-8")
        try:
            users_gui.login(user_name, password)
            self.login_label.setText("<font color='green'>Log in successfull</font>")
            self.widget.user_name = user_name
            operation_screen = operationscreen.OperationScreen(widget=self.widget)
            self.widget.addWidget(operation_screen)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except errors.InvalidNameError:
            self.login_label.setText("<font color='red'>Invalid username.</font>")
        except errors.WrongPasswordError:
            self.login_label.setText("<font color='red'>Wrong password.</font>")
        except errors.UserDoesNotExistsError:
            self.login_label.setText(
                f"<font color='red'>Username <b>{user_name}</b> does not exist.</font>"
            )

    def back(self):
        """Returns to the WelcomeScreen menu"""
        welcome = welcomescreen.WelcomeScreen(widget=self.widget)
        self.widget.addWidget(welcome)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        """Returns to the WelcomeScreen menu when Esc Key is pressed."""
        if e.key() == QtCore.Qt.Key_Escape:
            welcome = welcomescreen.WelcomeScreen(widget=self.widget)
            self.widget.addWidget(welcome)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
