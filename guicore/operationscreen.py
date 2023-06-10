#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 12/02/2023
"""
import os
from datetime import datetime, timedelta

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QPushButton, QMainWindow, QGraphicsTextItem

from guicore import users_gui
from guicore import loginscreen
from guicore import incomeexpensescreen
from guicore import readjustmentscreen
from guicore import transferscreen
from guicore import createaccountscreen
from guicore import categorypiechart
from guicore import calendardialog
from source import account_core as acc
from source import analysis
from source import errors


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class OperationScreen(QMainWindow):
    """
    Operation screen
    """

    def __init__(self, parent=None, widget=None) -> None:
        super(OperationScreen, self).__init__(parent)
        operation_screen = os.path.join(GUI_PATH, "operation_screen.ui")
        loadUi(operation_screen, self)
        self.widget = widget
        self.operation = None
        self.chart_mode = "monthly"
        self.chart_type = "expenses"
        self.curr_datetime = datetime.now()
        self.selected_datetime = self.curr_datetime
        self.custom_initial_date = None
        self.custom_final_date = None
        self.income_button.clicked.connect(self.pre_income)
        self.expense_button.clicked.connect(self.pre_expense)
        self.transfer_button.clicked.connect(self.pre_transfer)
        self.readjustment_button.clicked.connect(self.pre_readjustment)
        self.create_new_account_button.clicked.connect(self.create_account)

        self.back_button.clicked.connect(self.back)

        self.custom_period_button.clicked.connect(self.custom_date_range)

        self.switch_type_button.clicked.connect(self.switch_chart_type)

        self.previous_month_button.clicked.connect(self.previous_month_chart)

        self.next_month_button.clicked.connect(self.next_month_chart)

        self.reset_month_button.clicked.connect(self.current_month_chart)

        self.text_item = QGraphicsTextItem("0")
        self.chart = categorypiechart.CategoricalPieChart()
        self.chartView = QChartView(self.chart)
        self.current_month_chart()
        self.chartView.setRenderHint(QPainter.Antialiasing)

        # Add the chartView to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chartView)

        # checks if any account exists.
        if not acc.AccountParser().acc_list:
            self.income_button.setEnabled(False)
            self.expense_button.setEnabled(False)
            self.transfer_button.setEnabled(False)
            self.readjustment_button.setEnabled(False)

    def pre_income(self) -> None:
        """Takes the user to the income/expense screen and sets the flag operation to income"""
        self.operation = "income"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_expense(self) -> None:
        """Takes the user to the income/expense screen and sets the flag operation to expense"""
        self.operation = "expense"
        operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
            self.operation, widget=self.widget
        )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_transfer(self) -> None:
        """Takes the user to the transfer screen and sets the flag operation to transfer"""
        self.operation = "transfer"
        operation_inputs = transferscreen.TransferScreen(self.operation, widget=self.widget)
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_readjustment(self) -> None:
        """Takes the user to the readjustment screen and sets the flag operation to readjustment"""
        self.operation = "readjustment"
        operation_inputs = readjustmentscreen.ReadjustmentScreen(self.operation, widget=self.widget)
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def create_account(self) -> None:
        """Takes the user to the CreateAccount screen"""
        create_account_window = createaccountscreen.CreateAccount(widget=self.widget)
        self.widget.addWidget(create_account_window)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def _chart_title_formatter(self, title_type: str, title_month: str) -> str:
        """
        Formats the given string to make it a title for the Chart.
        """
        month = self.selected_datetime.month
        year = self.selected_datetime.year
        try:
            raw_data = analysis.DataAnalyzer()
            raw_data.get_data_per_currency("ARS")
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        if self.chart_type == "expenses":
            total = raw_data.get_month_expenses_by_category(month, year).sum()
        elif self.chart_type == "incomes":
            total = raw_data.get_month_incomes_by_category(month, year).sum()
        title_type = title_type.title()
        title_month = title_month.title()
        total = str(round(total, 2)).replace(".", "<sup>") + "</sup>"
        title = f"<h3><p align='center' style='color:black'><b>{title_type}: ${total}<br>{title_month}</b></p>"
        return title

    def current_month_chart(self) -> None:
        """
        Generates a new piechart of the current month and updates the variable
        self.selected_datetime
        """
        self.selected_datetime = self.curr_datetime
        try:
            raw_data = analysis.DataAnalyzer()
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        self.chart.clear_slices()
        title_type = self.chart_type
        title_month = self.curr_datetime.strftime(format="%B %Y")
        title = self._chart_title_formatter(title_type, title_month)
        self.chart.setTitle(title)
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            mode="monthly",
            month=self.curr_datetime.month,
            year=self.curr_datetime.year,
            curr="ARS",
            type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chartView to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chartView)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"

    def previous_month_chart(self) -> None:
        """
        Generates a new piechart of the previous month and updates the
        variable self.selected_datetime
        """
        try:
            raw_data = analysis.DataAnalyzer()
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        self.chart.clear_slices()
        cur_date = self.selected_datetime.day
        self.selected_datetime = self.selected_datetime - timedelta(days=cur_date)
        title_type = self.chart_type
        title_month = self.selected_datetime.strftime(format="%B %Y")
        title = self._chart_title_formatter(title_type, title_month)
        self.chart.setTitle(title)
        # self.chart.setTitle(self.selected_datetime.strftime(format="%B %Y").title())
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            mode="monthly",
            month=self.selected_datetime.month,
            year=self.selected_datetime.year,
            curr="ARS",
            type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chartView to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chartView)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"

    def next_month_chart(self) -> None:
        """
        Generates a new piechart of the next month and updates the
        variable self.selected_datetime
        """
        try:
            raw_data = analysis.DataAnalyzer()
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        self.chart.clear_slices()
        cur_date = self.selected_datetime.day
        # sets the first day of the mont
        self.selected_datetime = self.selected_datetime - timedelta(days=cur_date - 1)
        # sums 32 days to make sure to get next month
        self.selected_datetime = self.selected_datetime + timedelta(days=32)
        title_type = self.chart_type
        title_month = self.selected_datetime.strftime(format="%B %Y")
        title = self._chart_title_formatter(title_type, title_month)
        self.chart.setTitle(title)
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            mode="monthly",
            month=self.selected_datetime.month,
            year=self.selected_datetime.year,
            curr="ARS",
            type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chartView to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chartView)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"

    def custom_date_range(self) -> None:
        """
        Generates a new piechart of the period of time selected in the calendar.
        First it opens up a calendar widget to select the 2 dates that conform the
        desired period of time. Then uses it to gather the information needed for
        the pie chart.
        """
        calendar_dialog = calendardialog.CalendarDialog()
        ok_button = QPushButton("Ok")
        calendar_dialog.layout.addWidget(ok_button)
        ok_button.clicked.connect(calendar_dialog.get_date_range)
        calendar_dialog.exec_()
        self.widget.addWidget(calendar_dialog)
        if self.custom_initial_date and self.custom_final_date:
            self.custom_initial_date = str(calendar_dialog.initial_d)
            self.custom_final_date = str(calendar_dialog.final_d)
            try:
                raw_data = analysis.DataAnalyzer()
                raw_data.get_data_per_currency("ARS")
                self.chart.clear_slices()
                data_inner, data_outer = self.chart.load_data(
                    raw_data,
                    mode="period",
                    initial=self.custom_initial_date,
                    final=self.custom_final_date,
                    type=self.chart_type,
                )
                self.chart.add_slices(data_inner, data_outer)
                self.chart.update_labels()
                self.central_VR_Layout.addWidget(self.chartView)
                # set the chart mode to period
                self.chart_mode = "period"
            except errors.UserHasNotAccountsError:
                print("No data to display")
                return 0

    def switch_chart_type(self) -> None:
        """
        Changes the chart type to switch between incomes and expenses
        """
        try:
            raw_data = analysis.DataAnalyzer()
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        self.chart.clear_slices()
        if self.chart_type == "expenses":
            self.chart_type = "incomes"
        elif self.chart_type == "incomes":
            self.chart_type = "expenses"
        time = self.selected_datetime
        title_type = self.chart_type
        print(self.chart_mode)
        if self.chart_mode == "monthly":
            title_month = time.strftime(format="%B %Y")
            title = self._chart_title_formatter(title_type, title_month)
            self.chart.setTitle(title)
            data_inner, data_outer = self.chart.load_data(
                raw_data,
                mode=self.chart_mode,
                month=time.month,
                year=time.year,
                curr="ARS",
                type=self.chart_type,
            )
        elif self.chart_mode == "period":
            title_period = f"Period: {self.custom_initial_date} -- {self.custom_final_date}"
            title = self._chart_title_formatter(title_type, title_period)
            self.chart.setTitle(title)
            data_inner, data_outer = self.chart.load_data(
                raw_data,
                mode=self.chart_mode,
                initial=self.custom_initial_date,
                final=self.custom_final_date,
                curr="ARS",
                type=self.chart_type,
            )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chartView to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chartView)

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
