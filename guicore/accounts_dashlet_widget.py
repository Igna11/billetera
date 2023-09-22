#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 29/07/2023
"""
import os
import sys


from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class AccountDashletWidget(QWidget):
    def __init__(self, account):
        super().__init__()
        dashlet_widget = os.path.join(GUI_PATH, "account_dashlet_widget.ui")
        loadUi(dashlet_widget, self)
        # variables
        self.acc_index = 0
        self.acc_object = account
        self.acc_list = account.acc_list
        self.acc_name_list = account.get_acc_pretty_names()
        self.acc_object.get_totals()
        # buttons
        self.acc_next_button.clicked.connect(self.next_acc)
        self.acc_prev_button.clicked.connect(self.prev_acc)
        self.set_labels()

    def set_labels(self):
        """Sets the values of acc_name, acc_currency and the value of total label."""
        if not self.acc_list:
            self.acc_label.setText("None")
        else:
            self.acc_label.setText(self.acc_name_list[self.acc_index])
            self.total_label.setText(
                f"Total: <b>{self.acc_object.get_acc_total(self.acc_list[self.acc_index])}</b>"
            )
            self.acc_total_label.setText(f"<b>Totals: ${self.acc_object.ars_total:.2f} </b>")

    def next_acc(self):
        """Increments the index number that determines which account data will be displayed"""
        if self.acc_index < len(self.acc_list) - 1:
            self.acc_index += 1
        else:
            self.acc_index = 0
        self.set_labels()

    def prev_acc(self):
        """Decreases the index number that determines which account data will be displayed"""
        if self.acc_index > 0:
            self.acc_index -= 1
        else:
            self.acc_index = len(self.acc_list) - 1
        self.set_labels()
