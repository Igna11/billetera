#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 05/02/2023 18:10

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


class IncomeExpenseScreen(QMainWindow):
    """
    Screen where inputs for the operations are managed
    """

    def __init__(self, operation_flag: str, parent=None, widget=None):
        super(IncomeExpenseScreen, self).__init__(parent)
        operation_incomeexpense_screen = os.path.join(
            GUI_PATH, "operation_incomeexpense_screen.ui"
        )
        loadUi(operation_incomeexpense_screen, self)
        self.widget = widget
        self.operation_flag = operation_flag

        self.index = None
        self.acc_name = None
        self.acc_currency = None
        self.acc_items_list = account.AccountParser().get_acc_pretty_names()
        self.acc_list = [acc for acc in os.listdir() if "ACC" in acc]

        self.accounts_comboBox.addItems(self.acc_items_list)
        self.set_acc_data(self.accounts_comboBox.currentIndex())
        self.accounts_comboBox.currentIndexChanged.connect(self.set_acc_data)
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.cancel)

    def set_acc_data(self, i: int) -> None:
        """Sets the values of acc_name, acc_currency and the value of total label."""
        account_dict = account.AccountParser().get_acc_properties()
        self.index = i + 1
        self.acc_name = account_dict[self.index]["acc_name"]
        self.acc_currency = account_dict[self.index]["currency"]
        print(self.acc_list[i])
        account_total = account.AccountParser().get_acc_total(self.acc_list[i])
        self.total_label.setText(f"Total: {account_total}")

    def save(self):
        """Saves the operation into the .txt account"""
        value = self.quantity_line.text()
        category = self.category_line.text()
        subcategory = self.subcategory_line.text()
        description = self.description_line.text()
        if self.operation_flag == "income":
            try:
                value = float(value)
                operations.income(
                    value,
                    self.acc_name,
                    self.acc_currency,
                    category,
                    subcategory,
                    description,
                )
                self.status_label.setText(
                    f"<font color='green'>Operation successfull</font>"
                )
            except ValueError:
                self.status_label.setText(
                    f"<font color='red'>Invalid value entered.</font>"
                )
            except errors.NegativeOrZeroValueError:
                self.status_label.setText(
                    f"<font color='red'>Quantity must be greater than 0!</font>"
                )
        elif self.operation_flag == "expense":
            try:
                value = float(value)
                operations.expense(
                    value,
                    self.acc_name,
                    self.acc_currency,
                    category,
                    subcategory,
                    description,
                )
                self.status_label.setText(
                    f"<font color='green'>Operation successfull</font>"
                )
            except ValueError:
                self.status_label.setText(
                    f"<font color='red'>Invalid value entered.</font>"
                )
            except errors.NegativeOrZeroValueError:
                self.status_label.setText(
                    f"<font color='red'>Quantity must be greater than 0!</font>"
                )
            except errors.NegativeTotalError:
                self.status_label.setText(
                    f"<font color='red'>The account has not enough balance.</font>"
                )
            except errors.EmptyAccountError:
                self.status_label.setText(
                    f"<font color='red'>Quantity must be greater than 0!</font>"
                )
        print(
            self.acc_name,
            self.acc_currency,
            value,
            category,
            subcategory,
            description,
        )
        # Updates the total value of the account in the label "total_label"
        self.set_acc_data(self.accounts_comboBox.currentIndex())

    def cancel(self) -> None:
        """Returns to the OperationScreen Menu"""
        operation_screen = operationscreen.OperationScreen(widget=self.widget)
        self.widget.addWidget(operation_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, e):
        """Returns to the OperationScreen Menu when Esc key is pressed."""
        if e.key() == QtCore.Qt.Key_Escape:
            operation_screen = operationscreen.OperationScreen(
                widget=self.widget
            )
            self.widget.addWidget(operation_screen)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
