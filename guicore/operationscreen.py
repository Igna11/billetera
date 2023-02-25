#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 12/02/2023
"""
import os

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

from guicore import users_gui
from guicore import loginscreen
from guicore import incomeexpensescreen
from guicore import readjustmentscreen
from guicore import transferscreen

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH)


class OperationScreen(QDialog):
    """
    Operation screen
    """

    def __init__(self, parent=None, widget=None):
        super(OperationScreen, self).__init__(parent)
        operation_screen = os.path.join(GUI_PATH, "operation_menu.ui")
        loadUi(operation_screen, self)
        self.widget = widget
        self.operation = None
        self.income_button.clicked.connect(self.pre_income)
        self.expense_button.clicked.connect(self.pre_expense)
        self.transfer_button.clicked.connect(self.pre_transfer)
        self.readjustment_button.clicked.connect(self.pre_readjustment)

    def pre_income(self):
        self.operation = "income"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_expense(self):
        self.operation = "expense"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_transfer(self):
        self.operation = "transfer"
        operation_inputs = transferscreen.TransferScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_readjustment(self):
        self.operation = "readjustment"
        operation_inputs = readjustmentscreen.ReadjustmentScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            login_screen = loginscreen.LoginScreen(widget=self.widget)
            self.widget.addWidget(login_screen)
            users_gui.logout()
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
