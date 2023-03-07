#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 12/02/2023
"""
import os

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

from guicore import users_gui
from guicore import loginscreen
from guicore import incomeexpensescreen
from guicore import readjustmentscreen
from guicore import transferscreen
from guicore import createaccountscreen
from source import account_core as acc

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class OperationScreen(QMainWindow):
    """
    Operation screen
    """

    def __init__(self, parent=None, widget=None):
        super(OperationScreen, self).__init__(parent)
        operation_screen = os.path.join(GUI_PATH, "operation_screen.ui")
        loadUi(operation_screen, self)
        self.widget = widget
        self.operation = None
        self.income_button.clicked.connect(self.pre_income)
        self.expense_button.clicked.connect(self.pre_expense)
        self.transfer_button.clicked.connect(self.pre_transfer)
        self.readjustment_button.clicked.connect(self.pre_readjustment)
        self.create_new_account_button.clicked.connect(self.create_account)
        self.back_button.clicked.connect(self.back)
        # checks if any account exists.
        if not acc.AccountParser().acc_list:
            self.income_button.setEnabled(False)
            self.expense_button.setEnabled(False)
            self.transfer_button.setEnabled(False)
            self.readjustment_button.setEnabled(False)



    def pre_income(self):
        """Takes the user to the income/expense screen and sets the flag operation to income"""
        self.operation = "income"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_expense(self):
        """Takes the user to the income/expense screen and sets the flag operation to expense"""
        self.operation = "expense"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_transfer(self):
        """Takes the user to the transfer screen and sets the flag operation to transfer"""
        self.operation = "transfer"
        operation_inputs = transferscreen.TransferScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_readjustment(self):
        """Takes the user to the readjustment screen and sets the flag operation to readjustment"""
        self.operation = "readjustment"
        operation_inputs = readjustmentscreen.ReadjustmentScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def create_account(self):
        """Takes the user to the CreateAccount screen"""
        create_account_window = createaccountscreen.CreateAccount(
            widget=self.widget
        )
        self.widget.addWidget(create_account_window)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def back(self) -> None:
        """Returns to the LoginScreen Menu"""
        login_screen = loginscreen.LoginScreen(widget=self.widget)
        self.widget.addWidget(login_screen)
        users_gui.logout()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        """Returns to the LoginScreen Menu when Esc key is pressed."""
        if e.key() == QtCore.Qt.Key_Escape:
            login_screen = loginscreen.LoginScreen(widget=self.widget)
            self.widget.addWidget(login_screen)
            users_gui.logout()
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
