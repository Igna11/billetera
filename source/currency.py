#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 22:53:01 2021

@author: igna
"""

from urllib.request import urlopen
from urllib.error import URLError

from bs4 import BeautifulSoup


def currencies_values(verbose=False) -> dict:
    """
    Scraps the value in ARS of USD from the bna home page. If for any reason
    the first URL is not working, it will try with the second one.
    Returns a dictionary with all currencies and their value in ARS for
    buying and selling.
    """
    url_1 = "http://www.bna.com.ar/Personas"
    url_2 = "https://www.bna.com.ar/Cotizador/MonedasHistorico"
    try:
        text_response = urlopen(url_1).read()
    except URLError:
        try:
            text_response = urlopen(url_2).read()
        except URLError:
            if verbose:
                print(
                    "There was an error with 2 different URLs. Check internet connection."
                )
            return
    bs4_object = BeautifulSoup(text_response, "html.parser")
    # cleaning of the bs4 object to form headers and body:
    header = (
        bs4_object.find("thead")
        .get_text()
        .strip()
        .replace("\n", "\t")
        .split("\t")
    )
    body = (
        bs4_object.find("tbody")
        .get_text()
        .strip()
        .replace("\n", "\t")
        .replace(",", ".")
        .replace("\t\t\t", "\n")
        .split("\n")
    )
    # header and body are lists, but body can be converted into a list of lists
    body = [currency.split("\t") for currency in body]
    currency_dict = {
        currency[0]: dict(zip(header[1:], currency[1:])) for currency in body
    }
    return currency_dict
