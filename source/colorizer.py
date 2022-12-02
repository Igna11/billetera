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
    if style is None:
        if color == "grey":
            text = f"{GREY}{text}{ENDC}"
        elif color == "green":
            text = f"{GREEN}{text}{ENDC}"
        elif color == "cyan":
            text = f"{CYAN}{text}{ENDC}"
        elif color == "blue":
            text = f"{BLUE}{text}{ENDC}"
        elif color == "ambar":
            text = f"{AMBAR}{text}{ENDC}"
        elif color == "red":
            text = f"{RED}{text}{ENDC}"
        elif color == "purple":
            text = f"{PURPLE}{text}{ENDC}"
    elif style == "bold":
        if color == "grey":
            text = f"{BOLD}{GREY}{text}{ENDC}"
        elif color == "green":
            text = f"{BOLD}{GREEN}{text}{ENDC}"
        elif color == "cian":
            text = f"{BOLD}{CYAN}{text}{ENDC}"
        elif color == "blue":
            text = f"{BOLD}{BLUE}{text}{ENDC}"
        elif color == "ambar":
            text = f"{BOLD}{AMBAR}{text}{ENDC}"
        elif color == "red":
            text = f"{BOLD}{RED}{text}{ENDC}"
        elif color == "purple":
            text = f"{BOLD}{PURPLE}{text}{ENDC}"
    return text


def cprint(text: str, color: str, style=None):
    """Prints text with colors."""
    return print(color_format(text, color, style))
