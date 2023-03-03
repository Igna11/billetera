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
GUI_PATH = os.path.join(BASE_PATH)


class TransferScreen(QMainWindow):
    """
    Screen where the user can make transfers between accounts
    """

    def __init__(self, operation_flag: str, parent=None, widget=None):
        super(TransferScreen, self).__init__(parent)
        operation_transfer_screen = os.path.join(
            GUI_PATH, "operation_transfer_screen.ui"
        )
        loadUi(operation_transfer_screen, self)
        self.widget = widget
        self.acc_list = [acc for acc in os.listdir() if "ACC" in acc]
        # origin account info
        self.origin_acc_name = None
        self.origin_acc_currency = None
        self.origin_acc_total = None
        # destination account info
        self.dest_acc_name = None
        self.dest_acc_currency = None
        self.dest_acc_total = None

        self.operation_flag = operation_flag
        self.acc_pretty_names_list = (
            account.AccountParser().get_acc_pretty_names()
        )
        # origin accounts comboBox
        self.accounts_origin_comboBox.addItems(self.acc_pretty_names_list)
        self.accounts_origin_comboBox.currentIndexChanged.connect(
            self.origin_account_index
        )
        # dest accounts comboBox
        self.accounts_dest_comboBox.addItems(self.acc_pretty_names_list)
        self.accounts_dest_comboBox.currentIndexChanged.connect(
            self.dest_account_index
        )
        self.save_button.clicked.connect(self.save)

    def origin_account_index(self, i: int):
        """
        Called when user switchs items in the comboBox in order to update the
        total value of the origin account
        """
        account_dict = account.AccountParser().get_acc_properties()
        index = i + 1
        self.origin_acc_name = account_dict[index]["acc_name"]
        self.origin_acc_currency = account_dict[index]["currency"]
        print(self.acc_list[i])
        self.origin_acc_total = account.AccountParser().get_acc_total(
            self.acc_list[i]
        )
        self.total_origin_label.setText(
            f"<b>Total</b>: {self.origin_acc_total}"
        )

    def dest_account_index(self, i: int):
        """
        Called when user switchs items in the comboBox in order to update the
        total value of the destination account
        """
        account_dict = account.AccountParser().get_acc_properties()
        index = i + 1
        self.dest_acc_name = account_dict[index]["acc_name"]
        self.dest_acc_currency = account_dict[index]["currency"]
        print(self.acc_list[i])
        self.dest_acc_total = account.AccountParser().get_acc_total(
            self.acc_list[i]
        )
        self.total_dest_label.setText(f"<b>Total</b>: {self.dest_acc_total}")

    def save(self):
        """Function called by the save_button to perform the transfer."""
        try:
            value = float(self.quantity_line.text())
            if self.operation_flag == "transfer":
                try:
                    operations.transfer(
                        value,
                        self.origin_acc_name,
                        self.origin_acc_currency,
                        self.dest_acc_name,
                        self.dest_acc_currency,
                    )
                    self.status_label.setText(
                        "<font color='green'>Transfer successful!</font>"
                    )
                    # Display the new totals in the origin account
                    origin_index = self.accounts_origin_comboBox.currentIndex()
                    self.origin_acc_total = (
                        account.AccountParser().get_acc_total(
                            self.acc_list[origin_index]
                        )
                    )
                    self.total_origin_label.setText(
                        f"<b>Total</b>: {self.origin_acc_total}"
                    )

                    # Display the new totals in the destination account
                    origin_index = self.accounts_dest_comboBox.currentIndex()
                    self.dest_acc_total = (
                        account.AccountParser().get_acc_total(
                            self.acc_list[origin_index]
                        )
                    )
                    self.total_dest_label.setText(
                        f"<b>Total</b>: {self.dest_acc_total}"
                    )
                except errors.SameAccountTransferError:
                    self.status_label.setText(
                        "<font color='red'>Origin and destination accounts can't be the same.</font>"
                    )
                except errors.NotEqualCurrencyError:
                    self.status_label.setText(
                        "<font color='red'>Can not transfer between accounts with different currencies.</font>"
                    )
                except errors.EmptyAccountError:
                    self.status_label.setText(
                        "<font color='red'>Origin account is empty."
                    )
                except errors.NegativeOrZeroValueError:
                    self.status_label.setText(
                        "<font color='red'>Quantity to transfer must be greater that 0."
                    )
                print("trasnfer successfull")
        except ValueError:
            self.status_label.setText(
                "<font color='red'>Quantity field must not be empty."
            )

    def keyPressEvent(self, e):
        """Returns to previous screen when the Esc key is pressed"""
        if e.key() == QtCore.Qt.Key_Escape:
            operation_screen = operationscreen.OperationScreen(
                widget=self.widget
            )
            self.widget.addWidget(operation_screen)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
