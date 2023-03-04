#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 12/02/2023 18:10

@author: igna
"""
import os
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

from source import account_core as account
from source import operations
from source import errors
from guicore import operationscreen


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class ReadjustmentScreen(QMainWindow):
    """
    Screen where the user can make readjustment in accounts
    """

    def __init__(self, operation_flag: str, parent=None, widget=None):
        super(ReadjustmentScreen, self).__init__(parent)
        operation_readjustment_screen = os.path.join(
            GUI_PATH, "operation_readjustment_screen.ui"
        )
        loadUi(operation_readjustment_screen, self)
        self.widget = widget
        self.index = 0
        self.acc_name = None
        self.acc_currency = None
        self.operation_flag = operation_flag
        self.acc_items_list = (
            account.AccountParser().get_acc_pretty_names()
        )
        self.acc_list = [acc for acc in os.listdir() if "ACC" in acc]
        self.accounts_comboBox.addItems(self.acc_items_list)
        self.set_acc_data(self.accounts_comboBox.currentIndex())
        self.accounts_comboBox.currentIndexChanged.connect(self.set_acc_data)
        self.save_button.clicked.connect(self.save)

    def set_acc_data(self, i: int):
        """Sets the values of acc_name, acc_currency and the value of total label."""
        account_dict = account.AccountParser().get_acc_properties()
        self.index = i + 1
        self.acc_name = account_dict[self.index]["acc_name"]
        self.acc_currency = account_dict[self.index]["currency"]
        print(self.acc_list[i])
        account_total = account.AccountParser().get_acc_total(self.acc_list[i])
        self.total_label.setText(f"Total: {account_total}")

    def save(self):
        value = float(self.quantity_line.text())
        if self.operation_flag == "readjustment":
            operations.readjustment(
                value,
                self.acc_name,
                self.acc_currency,
            )

        print(
            self.acc_name,
            self.acc_currency,
            value,
        )
        # Updates the total value of the account in the label "total_label"
        self.set_acc_data(self.accounts_comboBox.currentIndex())

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            operation_screen = operationscreen.OperationScreen(
                widget=self.widget
            )
            self.widget.addWidget(operation_screen)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
