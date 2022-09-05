#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 22:53:01 2021

@author: igna
"""

from urllib.request import urlopen  # agregado 11-03-2020
from urllib.error import URLError  # agregado 20-05-2021

from bs4 import BeautifulSoup  # agregado 11-03-2020


class ConversorMoneda:
    """
    Scrapea el valor del dolar (y otros disponibles) en el momento de
    hacer la consulta
    """

    def __init__(self, verbose=False):
        self.urlDOLAR1 = "http://www.bna.com.ar/Personas"
        self.urlDOLAR2 = "https://www.bna.com.ar/Cotizador/MonedasHistorico"
        self.header = []
        self.body = []
        self.verbose = verbose

    def get_urls(self):
        return [self.urlDOLAR1, self.urlDOLAR2]

    def consulta(self):
        try:
            return urlopen(self.urlDOLAR1)
        except URLError as error_url:
            if self.verbose is True:
                print("no se pudo realizar la consulta debido a: ", error_url)

    def urlobj_a_texto(self):
        return BeautifulSoup(self.consulta().read(), "html.parser")

    def formateador(self):
        """
        Busca la tabla de donde sacar la información.
        La parte en encabezado y cuerpo.
        La formatea correctamente
        """
        self.header = (
            self.urlobj_a_texto()
            .find("thead")
            .get_text()
            .strip()
            .replace("\n", "\t")
            .split("\t")
        )

        self.body = (
            self.urlobj_a_texto()
            .find("tbody")
            .get_text()
            .strip()
            .replace("\n", "\t")
            .replace(",", ".")
            .replace("\t\t\t", "\n")
            .split("\n")
        )

    def precio(self):
        self.formateador()
        self.body = [elem.split("\t") for elem in self.body]
        dic = {
            elem[0]: dict(zip(self.header[1:], elem[1:])) for elem in self.body
        }
        return dic
