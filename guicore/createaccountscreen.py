#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 02/03/2023
"""
import os

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

from guicore import users_gui
from guicore import operationscreen

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH)


class CreateAccount(QMainWindow):
    """
    Operation screen
    """

    def __init__(self, parent=None, widget=None):
        super(CreateAccount, self).__init__(parent)
        operation_screen = os.path.join(GUI_PATH, "create_account_screen.ui")
        loadUi(operation_screen, self)
        self.widget = widget
        self.save_button.clicked.connect(self.create_account)
        self.currency_comboBox.addItems(["ARS", "USD"])

    def create_account(self):
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            login_screen = operationscreen.OperationScreen(widget=self.widget)
            self.widget.addWidget(login_screen)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
