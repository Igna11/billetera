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
from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from guicore import (
    users_gui,
    loginscreen,
    incomeexpensescreen,
    readjustmentscreen,
    createaccountscreen,
    categorypiechart,
    calendardialog,
    transferscreen,
    accounts_dashlet_widget,
)
from source import analysis, errors, account_core as acc


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "data")
GUI_PATH = os.path.join(BASE_PATH, "uis")


class OperationScreen(QMainWindow):
    """
    Operation screen
    """

    def __init__(self, widget=None) -> None:
        super().__init__()
        self.widget = widget
        self.setup_ui()
        self.initialize_variables()
        self.setup_buttons()
        self.disable_operation_buttons()

        # transition for accounts
        self.account_dashlet = accounts_dashlet_widget.AccountDashletWidget(acc.AccountParser())
        self.acc_totals_widget = QStackedWidget()
        self.acc_totals_widget.addWidget(self.account_dashlet)
        self.central_VL_Layout.insertWidget(0, self.acc_totals_widget)
        # Modifiers
        # self.text_item = QGraphicsTextItem("0")
        self.chart = categorypiechart.CategoricalPieChart()
        self.chart_view = QChartView(self.chart)
        self.current_month_chart()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Add the chart_view to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chart_view)

    def setup_ui(self) -> None:
        """Loads the ui file"""
        operation_screen = os.path.join(GUI_PATH, "operation_screen.ui")
        loadUi(operation_screen, self)

    def initialize_variables(self) -> None:
        """Set up the initial variables"""
        self.operation = None
        self.chart_mode = "monthly"
        self.chart_type = "expenses"
        self.curr_datetime = datetime.now()
        self.selected_datetime = self.curr_datetime
        self.custom_initial_date = None
        self.custom_final_date = None
        self.username_label.setText(f"<b>Hello {self.widget.user_name}!</b>")
        self.acc_items_list = acc.AccountParser().get_acc_pretty_names()
        self.acc_list = [acc for acc in os.listdir() if "ACC" in acc]

    def setup_buttons(self) -> None:
        """Sets the signals for the buttons of the window."""
        buttons_function_pairs = [
            (self.income_button, self.pre_income),
            (self.expense_button, self.pre_expense),
            (self.transfer_button, self.pre_transfer),
            (self.readjustment_button, self.pre_readjustment),
            (self.create_new_account_button, self.create_account),
            (self.back_button, self.back),
            (self.custom_period_button, self.custom_date_range),
            (self.switch_type_button, self.switch_chart_type),
            (self.previous_month_button, self.previous_month_chart),
            (self.next_month_button, self.next_month_chart),
            (self.reset_month_button, self.current_month_chart),
        ]
        for button, function in buttons_function_pairs:
            button.clicked.connect(function)

    def disable_operation_buttons(self):
        """checks if any account exists"""
        if not acc.AccountParser().acc_list:
            self.income_button.setEnabled(False)
            self.expense_button.setEnabled(False)
            self.transfer_button.setEnabled(False)
            self.readjustment_button.setEnabled(False)

    def pre_operation(self, operation) -> None:
        """Sets the UIs according to the operation value"""
        self.operation = operation
        if operation == "income":
            operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
                self.operation, widget=self.widget
            )
        elif operation == "expense":
            operation_inputs = incomeexpensescreen.IncomeExpenseScreen(
                self.operation, widget=self.widget
            )
        elif operation == "transfer":
            operation_inputs = transferscreen.TransferScreen(self.operation, widget=self.widget)
        elif operation == "readjustment":
            operation_inputs = readjustmentscreen.ReadjustmentScreen(
                self.operation, widget=self.widget
            )
        self.widget.addWidget(operation_inputs)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def pre_income(self) -> None:
        """Takes the user to the income/expense screen and sets the flag operation to income"""
        self.pre_operation("income")

    def pre_expense(self) -> None:
        """Takes the user to the income/expense screen and sets the flag operation to expense"""
        self.pre_operation("expense")

    def pre_transfer(self) -> None:
        """Takes the user to the transfer screen and sets the flag operation to transfer"""
        self.pre_operation("transfer")

    def pre_readjustment(self) -> None:
        """Takes the user to the readjustment screen and sets the flag operation to readjustment"""
        self.pre_operation("readjustment")

    def create_account(self) -> None:
        """Takes the user to the CreateAccount screen"""
        create_account_window = createaccountscreen.CreateAccount(widget=self.widget)
        self.widget.addWidget(create_account_window)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

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
        self.chart.update_title(
            raw_data,
            chart_mode="monthly",
            chart_type=self.chart_type,
            time_period_object=self.curr_datetime,
        )
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            chart_mode="monthly",
            time_period_object=self.curr_datetime,
            curr="ARS",
            chart_type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chart_view to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chart_view)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"
        return 0

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
        self.chart.update_title(
            raw_data,
            chart_mode="monthly",
            chart_type=self.chart_type,
            time_period_object=self.selected_datetime,
        )
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            chart_mode="monthly",
            time_period_object=self.selected_datetime,
            curr="ARS",
            chart_type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chart_view to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chart_view)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"
        return 0

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
        # sets the first day of the month
        self.selected_datetime = self.selected_datetime - timedelta(days=cur_date - 1)
        # sums 32 days to make sure to get next month
        self.selected_datetime = self.selected_datetime + timedelta(days=32)
        self.chart.update_title(
            raw_data,
            chart_mode="monthly",
            chart_type=self.chart_type,
            time_period_object=self.selected_datetime,
        )
        data_inner, data_outer = self.chart.load_data(
            raw_data,
            chart_mode="monthly",
            time_period_object=self.selected_datetime,
            curr="ARS",
            chart_type=self.chart_type,
        )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chart_view to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chart_view)
        # reset the chart mode in case the period mode was activated
        self.chart_mode = "monthly"
        return 0

    def custom_date_range(self) -> None:
        """
        Generates a new piechart of the period of time selected in the calendar.
        First it opens up a calendar widget to select the 2 dates that conform the
        desired period of time. Then uses it to gather the information needed for
        the pie chart.
        """
        calendar_dialog = calendardialog.CalendarDialog()
        calendar_dialog.select_button.clicked.connect(calendar_dialog.get_date_range)
        calendar_dialog.exec_()
        self.custom_initial_date = calendar_dialog.initial_d
        self.custom_final_date = calendar_dialog.final_d
        if self.custom_initial_date and self.custom_final_date:
            # set the chart mode to period
            self.chart_mode = "period"
            self.custom_initial_date = str(calendar_dialog.initial_d)
            self.custom_final_date = str(calendar_dialog.final_d)
            period_dict = {"initial": self.custom_initial_date, "final": self.custom_final_date}
            try:
                raw_data = analysis.DataAnalyzer()
                raw_data.get_data_per_currency("ARS")
                self.chart.clear_slices()
                data_inner, data_outer = self.chart.load_data(
                    raw_data,
                    chart_mode="period",
                    time_period_object=period_dict,
                    chart_type=self.chart_type,
                )
                self.chart.update_title(
                    raw_data,
                    chart_mode=self.chart_mode,
                    chart_type=self.chart_type,
                    time_period_object=period_dict,
                )
                self.chart.add_slices(data_inner, data_outer)
                self.chart.update_labels()
                self.central_VR_Layout.addWidget(self.chart_view)
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
        if self.chart_mode == "monthly":
            self.chart.update_title(
                raw_data,
                chart_mode=self.chart_mode,
                chart_type=self.chart_type,
                time_period_object=time,
            )
            data_inner, data_outer = self.chart.load_data(
                raw_data,
                chart_mode=self.chart_mode,
                time_period_object=time,
                curr="ARS",
                chart_type=self.chart_type,
            )
        elif self.chart_mode == "period":
            period_dict = {"initial": self.custom_initial_date, "final": self.custom_final_date}
            self.chart.update_title(
                raw_data,
                chart_mode=self.chart_mode,
                chart_type=self.chart_type,
                time_period_object=period_dict,
            )
            data_inner, data_outer = self.chart.load_data(
                raw_data,
                chart_mode=self.chart_mode,
                time_period_object=period_dict,
                curr="ARS",
                chart_type=self.chart_type,
            )
        self.chart.add_slices(data_inner, data_outer)
        self.chart.update_labels()
        # Add the chart_view to the central_VR_layout
        self.central_VR_Layout.addWidget(self.chart_view)

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
