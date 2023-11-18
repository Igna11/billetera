#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 06/04/2023
"""
from datetime import datetime

import pandas as pd
from PyQt5 import QtChart

from source import errors


class CategoricalPieChart(QtChart.QChart):
    """
    class to create pie charts with expenses and incomes with slices for categories
    and subcategories.
    data_inner: a pandas data frame with data to fill the inner pie chart
    data_outer: a pandas data frame with data to fill the outer pie chart
    period: a dictionary containing day, month ander to define the period (month) of the data to be displayed
    """

    def __init__(self, parent=None) -> None:
        super(CategoricalPieChart, self).__init__(parent)

        self.month = datetime.now().month
        self.year = datetime.now().year

        self.series_outer = QtChart.QPieSeries()
        self.series_inner = QtChart.QPieSeries()

        self.series_outer.setHoleSize(0.45)
        self.series_inner.setHoleSize(0.30)
        self.series_inner.setPieSize(0.45)

        self.addSeries(self.series_outer)
        self.addSeries(self.series_inner)

        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.setBackgroundRoundness(20)

    def load_data(
        self,
        raw_data: pd.DataFrame,
        chart_mode: str,
        time_period_object: datetime,
        curr: str = "ARS",
        chart_type: str = "expenses",
    ) -> tuple:
        """
        Loads the raw data in the given currency and for the given filters
        in order to create the desired piechart
        """
        raw_data.get_data_per_currency(curr)
        if chart_type == "expenses":
            chart_type = "Gasto"
        if chart_type == "incomes":
            chart_type = "Ingresos"
        if chart_mode == "monthly":
            month, year = time_period_object.month, time_period_object.year
            data_outer = raw_data.get_monthly_operations(month, year, chart_type, "category")
            data_inner = raw_data.get_monthly_operations(month, year, chart_type, "subcategory")
        elif chart_mode == "period":
            ci_date, cf_date = time_period_object.values()
            data_outer = raw_data.get_period_operations(ci_date, cf_date, chart_type, "category")
            data_inner = raw_data.get_period_operations(ci_date, cf_date, chart_type, "subcategory")
        else:
            raise ValueError("Valid modes: 'expenses', 'incomes'. Valid types: 'monthly', 'period'")
        return data_inner, data_outer

    def clear_slices(self):
        """
        Clear all slices in the pie chart
        """
        for pie_slice in self.series_outer.slices():
            self.series_outer.take(pie_slice)

        for pie_slice in self.series_inner.slices():
            self.series_inner.take(pie_slice)

    def add_slices(self, data_inner: pd.DataFrame, data_outer: pd.DataFrame) -> None:
        """
        Loops through the data to the create each slice of the inner and
        the outer series of the pie chart.
        """
        outer_idx = data_outer.index
        outer_val = data_outer.values
        for idx_outer, val_outer in zip(outer_idx, outer_val):
            slice_outer = QtChart.QPieSlice(idx_outer, val_outer)
            self.series_outer.append(slice_outer)
            for idx_inner, val_inner in zip(
                data_inner[idx_outer].index, data_inner[idx_outer].values
            ):
                slice_inner = QtChart.QPieSlice(idx_inner, val_inner)
                slice_inner.hovered.connect(
                    lambda is_hovered, slice_=slice_inner: slice_.setLabelVisible(is_hovered)
                )
                slice_inner.hovered.connect(
                    lambda is_hovered, slice_=slice_inner: slice_.setExploded(is_hovered)
                )
                slice_inner.setExplodeDistanceFactor(0.05)
                label = f"<p align='center' style='color:black'>{idx_inner}<br><b>${val_inner:.2f}</b></p>"
                slice_inner.setLabel(label)
                self.series_inner.append(slice_inner)

    def update_labels(self):
        """
        Updates the labels of the outer slices:
            If the percentage of a given slice is less or equal than 30%
            then the label is invisible unless the user hovers over the
            slcie.
            If the percentage of a given slice is greater than 30%, then
            the label is visible all the time.
        """
        for pie_slice in self.series_outer.slices():
            slice_lbl = pie_slice.label()
            slice_val = pie_slice.value()
            label = (
                f"<p align='center' style='color:black'>{slice_lbl}<br><b>${slice_val:.2f}</b></p>"
            )
            if pie_slice.percentage() > 0.05:
                pie_slice.setLabelVisible()
            elif pie_slice.percentage() <= 0.05:
                pie_slice.hovered.connect(
                    lambda is_hovered, slice_=pie_slice: slice_.setLabelVisible(is_hovered)
                )
            pie_slice.setLabel(label)

    def update_title(
        self,
        raw_data: pd.DataFrame,
        chart_mode: str,
        chart_type: str,
        time_period_object,
        ci_date=None,
        cf_date=None,
    ) -> str:
        """
        Creates the format for the title of the chart and updates it every time a chart
        is instantiated.
        chart_mode: monthly or period
        chart_type: incomes or expenses
        title_type
        """
        try:
            raw_data.get_data_per_currency("ARS")
        except errors.UserHasNotAccountsError:
            print("No data to display")
            return 0
        if chart_type == "expenses":
            chart_type = "Gasto"
        if chart_type == "incomes":
            chart_type = "Ingresos"
        if chart_mode == "monthly":
            selected_period = time_period_object.strftime(format="%B %Y").capitalize()
            month, year = time_period_object.month, time_period_object.year
            total = raw_data.get_monthly_operations(month, year, chart_type, "category").sum()
        elif chart_mode == "period":
            ci_date, cf_date = time_period_object.values()
            selected_period = f"Period: {ci_date} -- {cf_date}"
            total = raw_data.get_period_operations(ci_date, cf_date, chart_type, "category").sum()
        title_type = chart_type.capitalize()
        total = str(round(total, 2)).replace(".", "<sup>") + "</sup>"
        title = f"<h3><p align='center' style='color:black'><b>{title_type}: ${total}<br>{selected_period}</b></p>"
        self.setTitle(title)
