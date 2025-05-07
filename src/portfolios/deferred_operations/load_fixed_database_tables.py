#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Script para popular las tablas."""

import os

from db_handlers import (
    create_connection,
    insert_new_cc,
    insert_new_operation,
    execute_read_query,
    update_cc,
    update_operation,
)

PATH = "./operationsDB.sqlite"

if "operationsDB.sqlite" in os.listdir():
    print("Data base located")
    connection = create_connection(PATH)
    print("connection with database stablished")
else:
    print("Creating data base")
    connection = create_connection(PATH)
    with open("card_tables.sql", "r") as tables:
        table_query_script = tables.read()
    # creation of the tables
    connection.cursor().executescript(table_query_script)
    print("tables created")

insert_new_cc(
    connection, "2444", "VISA", "Santander", "09/27", "29/02/2024", "08/03/2024"
)
insert_new_cc(
    connection, "2455", "VISA", "Santander", "09/25", "29/02/2024", "08/03/2024"
)
insert_new_cc(
    connection, "5958", "AMEX", "Santander", "11/29", "29/02/2024", "11/03/2024"
)
insert_new_cc(
    connection, "1234", "DUMMY", "Santander", "11/29", "01/04/2024", "24/03/2024"
)
insert_new_operation(
    connection,
    operation_date="09/01/2024",
    operation_time="18:25",
    operation_amount=13994.64,
    operation_category="VISA",
    operation_subcategory="Bazar",
    operation_description="Compra de cositas de plástico en colombraro",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="11/01/2024",
    operation_time="22:00",
    operation_amount=292899.96,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra de colchon simomns",
    other="MercadoLibre",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=6,
    installments_paid=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/01/2024",
    operation_time="19:00",
    operation_amount=18199.98,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra de cortina para el living",
    other="Compras",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=2,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="31/01/2024",
    operation_time="22:00",
    operation_amount=16616,
    operation_category="VISA",
    operation_subcategory="Servicios",
    operation_description="Pago Claro Daniel y telefonia e internet",
    other="Servicios",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="06/02/2024",
    operation_time="12:00",
    operation_amount=21109,
    operation_category="VISA",
    operation_subcategory="MercadoLibre",
    operation_description="Compra de cosas varias de bazar por ML",
    other="MercadoLibre",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="09/02/2024",
    operation_time="11:30",
    operation_amount=14984,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="10/02/2024",
    operation_time="20:31",
    operation_amount=4580,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de adrogue antes de ir a la isla",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/02/2024",
    operation_time="11:51",
    operation_amount=47142.87,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Compra del set de espejos",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/02/2024",
    operation_time="12:32",
    operation_amount=8699.30,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/02/2024",
    operation_time="18:39",
    operation_amount=8205,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compras en el día de Palomar",
    other="Supermercado",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=1,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="03/03/2024",
    operation_time="16:48",
    operation_amount=119998.20,
    operation_category="VISA",
    operation_subcategory="Indumentaria",
    operation_description="Compra de un ambo (saco y pantalon) en mcownes",
    other="Ropa, Saco, Ambo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=6,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="05/03/2024",
    operation_time="19:50",
    operation_amount=6840,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compra en el dia de atun, mermelada y jugo clight",
    other="Comida",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="09/03/2024",
    operation_time="19:50",
    operation_amount=59290.02,
    operation_category="VISA",
    operation_subcategory="Indumentaria",
    operation_description="Compra en de zapatos de vestir en bleu, caseros",
    other="Zapatos",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="17/03/2024",
    operation_time="15:30",
    operation_amount=17779,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="2 hamburguesas de hutch en pedidos ya",
    other="Comida, Hutch",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="17/03/2024",
    operation_time="18:10",
    operation_amount=10800,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="Docena y media de facturas en la esperanza y 1/4 de galletitas de miel",
    other="Comida, Merienda, Facturas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="21/03/2024",
    operation_time="10:33",
    operation_amount=4400,
    operation_category="VISA",
    operation_subcategory="Comida",
    operation_description="Desayuna en nucha buscando wifi para laburar",
    other="Comida, Desayuno, Cafe, Facturas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="22/03/2024",
    operation_time="11:12",
    operation_amount=13050,
    operation_category="VISA",
    operation_subcategory="Farmacia",
    operation_description="Tafirol 1g, ibu 600, te vick",
    other="Remedios, Medicamentos",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="25/03/2024",
    operation_time="19:32",
    operation_amount=18480,
    operation_category="VISA",
    operation_subcategory="Combustible",
    operation_description="15000 de nafta y 3840 de gas para la renoleta",
    other="Nafta, Gas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="26/03/2024",
    operation_time="12:52",
    operation_amount=14820,
    operation_category="VISA",
    operation_subcategory="Salidas",
    operation_description="Almuerzo con Paui en 'La sede' CFC (cañuelas futbol club)",
    other="Salidas, Restaurant, Almuerzo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

# Dummy case for testing update_is_active function
insert_new_operation(
    connection,
    operation_date="28/03/2024",
    operation_time="12:52",
    operation_amount=11111,
    operation_category="VISA",
    operation_subcategory="Dummy",
    operation_description="Dummy",
    other="Dummy",
    operation_card_id=1234,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

# Dummy for testing
insert_new_operation(
    connection,
    operation_date="15/11/2023",
    operation_time="12:52",
    operation_amount=2211,
    operation_category="VISA",
    operation_subcategory="Dummy",
    operation_description="Dummy",
    other="Dummy",
    operation_card_id=1234,
    operation_card_brand="VISA",
    operation_installments=18,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/03/2024",
    operation_time="12:15",
    operation_amount=20000,
    operation_category="VISA",
    operation_subcategory="Combustible",
    operation_description="Carga gasoil estanciera para ir a buscar el sillon",
    other="Estanciera, Gasoil, Combustible",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="29/03/2024",
    operation_time="13:22",
    operation_amount=6300,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Cafe nesface instantaneo barato no torrado",
    other="Cafe",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="30/03/2024",
    operation_time="12:49",
    operation_amount=17680,
    operation_category="VISA",
    operation_subcategory="Restaurant",
    operation_description="Hamburguesa en hutch con pauis",
    other="Comida, Hamburguesa, Hutch",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="30/03/2024",
    operation_time="17:26",
    operation_amount=9000,
    operation_category="VISA",
    operation_subcategory="Perfumeria",
    operation_description="Compra de 2 repelentes marca pirulo",
    other="Repelente",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=2,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="01/04/2024",
    operation_time="20:24",
    operation_amount=43400,
    operation_category="VISA",
    operation_subcategory="Salidas",
    operation_description="Gato negro por el cumpleaños de Lanita",
    other="Cafeteria, Salidas, Anita, Cumpleaños",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="02/04/2024",
    operation_time="08:07",
    operation_amount=39006,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Carga combustible camioneta",
    other="Auto, Combustible, Nafta, Vacaciones",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="02/04/2024",
    operation_time="09:30",
    operation_amount=6500,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Medialunas de atalaya",
    other="Desayuno, Medialunas, Atalaya",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="02/04/2024",
    operation_time="20:59",
    operation_amount=6655,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Compra de comida en el dia de maipu",
    other="Latas, Cena, Guiso",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="03/04/2024",
    operation_time="14:23",
    operation_amount=33150,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Almuerzo en manolo con mi pauis",
    other="Restaurant, Vacaciones, Manolo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="03/04/2024",
    operation_time="18:16",
    operation_amount=11680,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Merienda en Cafe en las Nubes",
    other="Merienda, Cafeteria, Vacaciones",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="03/04/2024",
    operation_time="19:57",
    operation_amount=13700,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Alfajores Havanna para padres",
    other="Alfajores, Havanna, Regalo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="03/04/2024",
    operation_time="20:57",
    operation_amount=41076.99,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Carga Nafta en Mar del Plata",
    other="Combustible, Nafta, Honda",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="04/04/2024",
    operation_time="14:18",
    operation_amount=27800,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Almuerzo en pinamar con la pauis",
    other="Vacaciones, Pinamar, Almuerzo, Restaurante",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="05/04/2024",
    operation_time="10:59",
    operation_amount=20776,
    operation_category="VISA",
    operation_subcategory="Vacaciones",
    operation_description="Compra de Fumixane 4 pastillas",
    other="Maipu, Vacaciones, Plaga, Gamexane",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="01/01/2024",
    operation_time="10:59",
    operation_amount=20776,
    operation_category="VISA",
    operation_subcategory="DUMMY",
    operation_description="DUMMY",
    other="DUMMY",
    operation_card_id=1234,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="09/04/2024",
    operation_time="23:50",
    operation_amount=69800,
    operation_category="VISA",
    operation_subcategory="Regalo",
    operation_description="Mantita de regalo para paui por su cumple",
    other="Regalo, Paui, Cumple",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=6,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="10/04/2024",
    operation_time="14:49",
    operation_amount=13812.46,
    operation_category="VISA",
    operation_subcategory="Auto",
    operation_description="VTV de la renoleta.",
    other="Auto, Mantenimiento, VTV",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="16/04/2024",
    operation_time="10:00",
    operation_amount=9370.84,
    operation_category="VISA",
    operation_subcategory="Auto",
    operation_description="Seguro renoleta.",
    other="Auto, Seguro",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/04/2024",
    operation_time="02:00",
    operation_amount=2302.05,
    operation_category="VISA",
    operation_subcategory="Transporte",
    operation_description="Cabify para facha y nico",
    other="Cabify",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/05/2024",
    operation_time="11:30",
    operation_amount=10210.35,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Cafe gold intenso, un desodorante y una manteca en la APP de dia (hot sale)",
    other="Hot sale, Supermercado, Cafe",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/05/2024",
    operation_time="18:00",
    operation_amount=599999,
    operation_category="VISA",
    operation_subcategory="Depto",
    operation_description="Lavarropas en hot sale en 9 cuotas sin interes en fravega",
    other="Hot sale, Lavarropas, Fravega",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=9,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="16/05/2024",
    operation_time="20:45",
    operation_amount=17895.54,
    operation_category="VISA",
    operation_subcategory="Salidas",
    operation_description="3 entradas para la Magickmeeting ",
    other="VISA, Magic, Magicmeeting, Regalo, Cho, Chaufas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="23/05/2024",
    operation_time="12:35",
    operation_amount=9753,
    operation_category="VISA",
    operation_subcategory="Supermercado",
    operation_description="Compra de: galletitas de agua $1185, kg harina leudante $1149, atun en lata x2 $3980, tapa de empanada $849, huevos x2 $2990",
    other="VISA, Supermercado, Carrefour",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="23/05/2024",
    operation_time="18:20",
    operation_amount=15900,
    operation_category="VISA",
    operation_subcategory="Regalo",
    operation_description="Compra de Vinito para Re y Nahue como agradecimiento del sillón",
    other="VISA, Vino, Vinoteca, Regalo",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="31/05/2024",
    operation_time="20:50",
    operation_amount=6729,
    operation_category="Comida",
    operation_subcategory="Cena",
    operation_description="Pedido de hamburguesa epica a hutch por PedidosYa",
    other="VISA, Cena, Delivery, Hutch, Hamburgesa",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="09/06/2024",
    operation_time="21:43",
    operation_amount=36200,
    operation_category="Salidas",
    operation_subcategory="Restaurant",
    operation_description="Cena en pasta rosa lanusita con Pauis",
    other="VISA, Pasta Rosa, Cena, Restaurant, Pastas",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="10/06/2024",
    operation_time="12:00",
    operation_amount=14124.99,
    operation_category="Auto",
    operation_subcategory="Seguro",
    operation_description="Libra compañia de seguros Renoleta",
    other="VISA, Seguro, Libra, Renoleta, Renault",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="12/06/2024",
    operation_time="21:15",
    operation_amount=20800,
    operation_category="Comidas",
    operation_subcategory="Cena",
    operation_description="Automostaza con Pauis llevandola a su casa",
    other="VISA, Cena, Mostaza",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/06/2024",
    operation_time="21:08",
    operation_amount=37333.60,
    operation_category="Impuestos",
    operation_subcategory="ARBA",
    operation_description="Pago de cuotas 1,2,3,4,5 2024 partida 101-137475-8",
    other="VISA, ARBA, Impuesto",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/06/2024",
    operation_time="21:58",
    operation_amount=19609.80,
    operation_category="Impuestos",
    operation_subcategory="ARBA",
    operation_description="Pago de cuotas 1,2,3 2024 partida Maipu 066-006576",
    other="VISA, ARBA, Impuesto, Maipu",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="15/06/2024",
    operation_time="21:45",
    operation_amount=12100,
    operation_category="Salidas",
    operation_subcategory="Cumpleaños",
    operation_description="Cumple de pochi en pentos, hamburguesa",
    other="VISA, Pentos, Cumple, Pochi, Hamburguesa",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="19/07/2024",
    operation_time="22:05",
    operation_amount=5685,
    operation_category="Comidas",
    operation_subcategory="Cena",
    operation_description="Hamburguesa Epica en Hutch (por pedidos ya pero para llevar)",
    other="VISA, Hutch, Hamburguesa, Cena, PedidosYa",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="20/07/2024",
    operation_time="19:07",
    operation_amount=9000,
    operation_category="Auto",
    operation_subcategory="Estacionamiento",
    operation_description="Pago estacionamiento para la Magic Meeting",
    other="VISA, Auto, Estacionamiento, MagicMeeting",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="25/07/2024",
    operation_time="17:39",
    operation_amount=66000,
    operation_category="Salud",
    operation_subcategory="Optica",
    operation_description="Caja de lentes de contacto acuevue2",
    other="VISA,Lentes,Optica",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=2,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="25/07/2024",
    operation_time="22:00",
    operation_amount=29560,
    operation_category="Indumentaria",
    operation_subcategory="Ropa",
    operation_description="Compra de 4 boxers silko",
    other="VISA,Ropa,Boxers,Silko",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=0,
    is_active=1,
)
insert_new_operation(
    connection,
    operation_date="26/07/2024",
    operation_time="16:00",
    operation_amount=5529,
    operation_category="Compras",
    operation_subcategory="Regalo",
    operation_description="Docena de facturas del abuelo para mi pauis",
    other="VISA,Medialunas,Regalo,Registro,Moto",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="12/08/2024",
    operation_time="12:00",
    operation_amount=18422.97,
    operation_category="Auto",
    operation_subcategory="Seguro",
    operation_description="Seguro Libra Cia de Seguros: Seguro renoleta",
    other="VISA,Auto,Seguro",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="25/08/2024",
    operation_time="15:20",
    operation_amount=34200,
    operation_category="Salidas",
    operation_subcategory="Restaurant",
    operation_description="El bodegon de madero pasta libre con mi pauis",
    other="VISA,Restaurant,Pasta,Bodegon,Madero",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="07/09/2024",
    operation_time="11:36",
    operation_amount=44910,
    operation_category="Compras",
    operation_subcategory="Indumentaria",
    operation_description="Compra de 4 boxers Sylko talle M negros",
    other="VISA,Indumentaria,Ropa,Boxer,Sylko",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=9,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="13/09/2024",
    operation_time="09:00",
    operation_amount=18422.97,
    operation_category="Auto",
    operation_subcategory="Seguro",
    operation_description="Seguro de la renoleta",
    other="VISA,Auto,Seguro,Libra,Renoleta",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)


insert_new_operation(
    connection,
    operation_date="24/09/2024",
    operation_time="20:32",
    operation_amount=88000,
    operation_category="Salidas",
    operation_subcategory="Bar",
    operation_description="Crystal Bar: Salida de aniversario con pauis a comer al crystal bar",
    other="VISA,Bar,Salidas,Crystal,Aniversario",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=1,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="23/10/2024",
    operation_time="15:00",
    operation_amount=39000,
    operation_category="Compras",
    operation_subcategory="Indumentaria",
    operation_description="Compra de un pantalon de gabardina negro en Lanus con mi pauis",
    other="VISA,Pantalon,Ropa,Indumentaria",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=0,
    is_active=1,
)

insert_new_operation(
    connection,
    operation_date="07/11/2024",
    operation_time="16:00",
    operation_amount=41599.02,
    operation_category="Compras",
    operation_subcategory="Depto",
    operation_description="Ventilador para el depto",
    other="VISA,Ventilador,Depto,Electrodomestico",
    operation_card_id=2455,
    operation_card_brand="VISA",
    operation_installments=3,
    installments_paid=0,
    is_active=1,
)


