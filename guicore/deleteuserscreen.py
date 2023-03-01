#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 09/02/2023
"""
import os

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLineEdit, QMessageBox, QMainWindow

from source import errors
from guicore import users_gui
from guicore import welcomescreen

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH)


class DeleteUserScreen(QMainWindow):
    """
    UI where the users can delete an existing userwith e-mail, user name, and password
    """

    def __init__(self, parent=None, widget=None):
        super(DeleteUserScreen, self).__init__(parent)
        delete_user_screen = os.path.join(GUI_PATH, "delete_user_screen.ui")
        loadUi(delete_user_screen, self)
        self.widget = widget
        self.password_line.setEchoMode(QLineEdit.Password)
        self.delete_user_button.clicked.connect(self.delete_user)
        self.usr_deleted_msg = QMessageBox()

    def delete_user(self):
        username = self.user_name_line.text()
        useremail = self.email_line.text()
        password = self.password_line.text().encode("utf-8")
        confirmation = self.confirmation_box.isChecked()
        try:
            users_gui.delete_user(username, useremail, password, confirmation)
            popup_message = self.usr_deleted_msg.question(
                self,
                f"User deleted.",
                f"User {username} deleted.\nDo you want to go back?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if popup_message == QMessageBox.Yes:
                self.goback()
            if popup_message == QMessageBox.No:
                pass
            self.delete_label.setText(
                f"<font color='green'>User {username} deleted.</font>"
            )
        except errors.UserDoesNotExistsError:
            self.delete_label.setText(
                f"<font color='red'>User <b>{username}</b> does not exist</font>"
            )
        except errors.WrongPasswordError:
            self.delete_label.setText(
                "<font color='red'>Wrong password</font>"
            )
        except errors.UserCouldNotBeDeletedError:
            self.delete_label.setText(
                f"<font color='red'>Please mark 'I am sure'.</font>"
            )
        except errors.InvalidEmailError:
            self.delete_label.setText(
                f"<font color='red'>Invalid email format.</font>"
            )

    def goback(self):
        welcome = welcomescreen.WelcomeScreen(widget=self.widget)
        self.widget.addWidget(welcome)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            welcome = welcomescreen.WelcomeScreen(widget=self.widget)
            self.widget.addWidget(welcome)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
