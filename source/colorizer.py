#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 12:47:00 2022
"""

PURPLE = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
AMBAR = "\033[93m"
RED = "\033[91m"
GREY = "\033[90m"
ENDC = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"


def color_format(text: str, color: str, style=None) -> str:
    """
    Adds format to text to be printed with colors:
    text: str
        the text to print
    color: str
        the desired color - grey, green, cian, blue, ambar, red, purple
    style: str
        default: None. Bold to print bold text
    """
    color_lookup_dict = {
        "grey": f"{GREY}{text}{ENDC}",
        "green": f"{GREEN}{text}{ENDC}",
        "cyan": f"{CYAN}{text}{ENDC}",
        "blue": f"{BLUE}{text}{ENDC}",
        "ambar": f"{AMBAR}{text}{ENDC}",
        "red": f"{RED}{text}{ENDC}",
        "purple": f"{PURPLE}{text}{ENDC}",
    }
    color_bold_lookup_dict = {
        "grey": f"{BOLD}{GREY}{text}{ENDC}",
        "green": f"{BOLD}{GREEN}{text}{ENDC}",
        "cyan": f"{BOLD}{CYAN}{text}{ENDC}",
        "blue": f"{BOLD}{BLUE}{text}{ENDC}",
        "ambar": f"{BOLD}{AMBAR}{text}{ENDC}",
        "red": f"{BOLD}{RED}{text}{ENDC}",
        "purple": f"{BOLD}{PURPLE}{text}{ENDC}",
    }
    if style is None:
        text = color_lookup_dict.get(color)
    elif style == "bold":
        text = color_bold_lookup_dict.get(color)
    return text


def cprint(text: str, color: str, style=None):
    """Prints text with colors."""
    return print(color_format(text, color, style))
