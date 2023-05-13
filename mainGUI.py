#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on 05/02/2023
"""

import sys

from guicore import welcomescreen
from PyQt5.QtWidgets import QApplication, QStackedWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    main_window = welcomescreen.WelcomeScreen(widget=widget)
    widget.addWidget(main_window)
    widget.show()
    app.exec()
