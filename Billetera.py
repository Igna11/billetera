# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos
"""
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

from ConversorClass import ConversorMoneda

directorio = os.path.dirname(os.path.abspath(__file__))

os.chdir(directorio)
pd.set_option("display.max_columns", 11)
# %%
"""
Cosas que quisiera ir agregándole al script:


TODO    Editor de entradas:
        Alguna manera para editar un gasto, un ingreso, o algo que fue mal
        ingresado (puede que haga falta usar archivos temporales y librerias
        afines)

TODO    Graficos:
        Alguna forma fácil de ver gastos/ingresos/whatever por día, por semana
        por mes, por año.

TODO    Interfaz Gráfica y ejectuable:
        nada, eso, a futuro (lejano)

TODO    Que no se pueda crear usuario estando logueado en algún usuario

TODO    Separar todo este script en módulos.

TODO    Que no se puedan hace transferencias de cuentas de distintos tipos
        (de pesos a dolares o dolares a pesos)
"""


def Fecha():
    """
    simplemente genera la hora en formato argento
    """
    fecha_hora = datetime.now()
    fecha = fecha_hora.strftime("%d-%m-%Y")
    hora = fecha_hora.strftime("%H:%M:%S")
    return {"Fecha": fecha, "hora": hora}


def Precio_dolar(verbose=False):
    """
    Creada (aprox) 21-03-2020
    Scrapea el precio del dolar del banco nacion
    Ver la forma que si no anda la pagina del banco central, use otra.
    Modificada 14/11/2020 para manejar algunas excepciones
    Modificada 10/08/2021 Usa una función aparte bien armada para conseguir el
    precio del dolar
    """
    # Creo el objeto que maneja la consulta y me devuelve el precio
    dolar = ConversorMoneda(verbose=verbose)
    try:
        # Trato de conseguir el precio de internet, si no, handleo el error
        PrecioDolar = dolar.precio()["Dolar U.S.A"]["Compra"]
    except AttributeError as e:
        if verbose is True:
            print("Ocurrio el siguiente error durante la consulta:")
            print(e)
            print("Seguramente se debe a un error urlopen y no de Attribute")
        print("No se pudo obtener el precio del dolar de internet, se usó la",
              " última cotización")
        # Como no pude conseguir el precio de internet, lo infiero de el último
        # balance en la cuenta Balance.txt
        bal_datos = pd.read_csv("Balance.txt", sep="\t", encoding="latin1")
        tot_dinero = bal_datos["Total"].values[-1]
        tot_pesos = bal_datos["Total_pesos"].values[-1]
        tot_dolares = bal_datos["Total_dolares"].values[-1]
        try:
            PrecioDolar = str(round((tot_dinero - tot_pesos)/tot_dolares, 2))
        except ZeroDivisionError:
            print("No hay dolares, asi que no importa cuanto vale")
            PrecioDolar = "0.00"

    return float(PrecioDolar.replace(",", "."))


def Info():  # Creada 15-06-2019  # Modificada 21-03-2020
    # Funciones actuales del codigo
    funciones = [
        "Fecha()",
        "Precio_dolar()",
        "Info()",
        "CrearUsuario()",
        "IniciarSesion()",
        "CerrarSesion()",
        "Crear_cuenta()",
        "Lista_cuentas()",
        "Datos_cuenta()",
        "Asignador_cuentas()",
        "Total()",
        "Ingreso()",
        "Extraccion()",
        "Gasto()",
        "Transferencia()",
        "Reajuste()",
        "Balance()<--NO USAR-ver help",
        "BalanceGraf()",
        "Filtro()",
        "balances()",
        "balances_totales()"
        ]
    # lista con los nombres de los archivos de cuenta
    Lista = Lista_cuentas()
    DolVal = Precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = []
    for elem in Lista:
        try:
            total.append(pd.read_csv(elem,
                                     sep="\t",
                                     encoding="latin1").values[-1, 2])
        except IndexError:
            total.append(0)
    # nombre de la cuenta con el saldo total
    informacion = ""
    for i in range(len(Lista)):
        if "DOL" in Lista[i]:
            try:
                total[i]*DolVal
            except TypeError:
                total[i] = 0
            informacion += "\n" + Lista[i] + ": " + "Saldo total u$s"\
                + str("%.2f" % total[i]) + " Saldo total $"\
                + str("%.2f" % (total[i]*DolVal)) + "\n"
        else:
            informacion += "\n" + Lista[i] + ": " + "Saldo total $"\
                + str("%.2f" % total[i]) + "\n"
    informacion = informacion.replace("CUENTA", "").replace("_DOL", "")\
        .replace(".txt", "")
    total, total_pesos, total_dolares = Total()
    str_funciones = "\n".join(funciones)
    print("Funciones:\n", str_funciones)
    print("="*50)
    print("Cuentas existentes:\n", informacion)
    print("="*50)
    print("Dolares totales: $%.2f" % total_dolares)
    print("="*50)
    print("Pesos totales: $%.2f" % total_pesos)
    print("="*50)
    print("Dinero total en cuentas: $%.2f" % total)
    print("="*50)
    # return informacion


# %%


def CrearUsuario():  # creada 10-02-2019
    nombre = input("\nIngrese el nombre de usuario\n") + "USR"
    if os.path.isdir(nombre):  # 10/01/2020 msj al intentar crear usr existente
        print("\nYa existe el usuario\n")
    else:
        os.makedirs(nombre)
        print("\nSe creo el usuario %s\n" % nombre.strip("USR"))


def IniciarSesion():  # creada 10-02-2019
    nombre = input("\nNombre de usuario\n") + "USR"
    if os.path.isdir(nombre):
        Dir = directorio + "/" + nombre
        os.chdir(Dir)
        print("\nInicio de sesion de %s\n" % nombre.strip("USR"))
        Info()
    else:
        print("\nNo existe el usuario\n")


def CerrarSesion():  # creada 10-02-2019
    os.chdir(directorio)
    print("\nSe ha cerrado sesión\n")


def EliminarUsuario():  # TODO solucion el PermissionError 10/01/2020
    nombre = input("\nIngrese el nombre de usuario a borrar\n") + "USR"
    if os.path.isdir(nombre):
        advertencia = "¿Seguro que queres eliminar el usuario?\n\n\
        todos los datos contenidos en ella se perderán para siempre.\n\n\
        Ingrese '1', 'si' o 'y' para borrar\n\
        Ingrese cualquier otra cosa para cancelar\n"
        respuesta = input(advertencia)
        posibles_respuestas = ["1", "si", "y"]
        if respuesta in posibles_respuestas:
            os.rmdir(nombre)
            print("\nSe eliminó el usuario %s\n" % nombre.strip("USR"))
        else:
            print("\nNo se eliminó el usuario %s\n" % nombre.strip("USR"))
    else:
        print("\nNo existe el usuario\n")


# %%


def Crear_cuenta():
    """
    Crea un .txt cuyo nombre será el nombre de la cuenta
    """
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    tipo_cuenta = input("\nIngresar 0 para cuenta en pesos\n"
                        "Ingresar 1 para cuenta en dolares\n")
    if tipo_cuenta == "0":
        nombre += "CUENTA.txt"
    elif tipo_cuenta == "1":
        nombre += "CUENTA_DOL.txt"
    else:
        print("\n %s inválido\n" % tipo_cuenta)
    Encabezados = ["Fecha", "hora", "Total", "Ingresos", "Extracciones",
                   "Gasto", "Categoria", "Subcategoria", "Descripcion",
                   "Balance"]
    fila = "\t".join(Encabezados) + "\n"
    with open(nombre, "x") as micuenta:
        micuenta.write(fila)
    print("\nSe ha creado la cuenta %s\n"
          % nombre.strip("_DOL.txt").strip("CUENTA"))


def Eliminar_cuenta():
    nombre = Asignador_cuentas()
    advertencia = "¿Seguro que queres eliminar la cuenta?\n\n\
    todos los datos contenidos en ella se perderán para siempre.\n\n\
    Ingrese '1', 'si' o 'y' para borrar\n\
    Ingrese cualquier otra cosa para cancelar\n"
    respuesta = input(advertencia)
    posibles_respuestas = ["1", "si", "y"]
    if respuesta in posibles_respuestas:
        os.remove(nombre)
        print("\nSe eliminó la cuenta %s\n"
              % nombre.strip("_DOL.txt").strip("CUENTA"))
    else:
        print("\nNo se eliminó la cuenta %s\n"
              % nombre.strip("_DOL.txt").strip("CUENTA"))


def Lista_cuentas():
    """
    Hace una list de todas las cuentas, en pesos y en dolares
    función auxiliar creada el 20-03-2020, a las 02:25 primeras horas de la
    cuarentena obligatoria por el COVID-19
    """
    """
    EVALUAR LA POSIBILIDAD DE USAR glob.glob: (gracias paui 20-03-2020 -13:26)
        El código se simplifica a una linea así:
    Lista = glob.glob(r"*CUENTA*.txt")
    """
    lista = os.listdir()
    Lista = []
    for elem in lista:
        if "CUENTA.txt" in elem or "CUENTA_DOL.txt" in elem:
            Lista.append(elem)
    return Lista


def Datos_cuenta():
    """
    los datos crudos de la cuenta
    Modificada 21-03-2020  01:00
    """
    nombre = Asignador_cuentas()
    datos = pd.read_csv(nombre, sep="\t", encoding="latin1")
    return datos


def Asignador_cuentas():
    """
    20-03-2020  15:03
    Genera un diccionario con el nombre de las cuentas existentes y un numero
    para que el usuario elija a qué cuenta ingresar un gasto o un ingreso
    mediante un input numérico
    """
    alfabeto = Lista_cuentas()
    Dic = {}
    Cuentas = ""
    for i, elem in enumerate(alfabeto):
        # voy armando un diccionario que asigna un numero a cada cuenta
        Dic.update({str(i+1): elem})
        # defino una variable sin sufijos para printear
        cuenta_str = (elem.replace("CUENTA", "")
                      .replace("_DOL", "")
                      .replace(".txt", ""))
        # actualizo el string final que se imprime en consola
        Cuentas += "\n" + str(i+1) + ": " + cuenta_str + "\n"
    # Meto un input de teclado
    while True:
        numero_cta = input("\nElija la cuenta\n" + Cuentas + "\n")
        try:
            nombre_cuenta = Dic[numero_cta]
            return nombre_cuenta
        except KeyError:
            print("="*50)
            print("\nValor elegido: '%s' erroneo, intente de nuevo."
                  % numero_cta)
            print("Presione Ctrol+C para salir\n")
            print("="*50)


def Total():
    # lista con los nombres de los archivos de cuenta
    Lista = Lista_cuentas()
    DolVal = Precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = []
    total_pesos = []
    total_dolares = []
    for elem in Lista:
        df = pd.read_csv(elem, sep="\t", encoding="latin1")
        # Si la cuenta no es nueva, entonces busca el total, si no, al no tener
        # dinero adentro, va a tirar IndexError. En ese caso el valor_elem = 0
        try:
            valor_elem = df["Total"].values[-1]
            if "DOL" in elem:
                total_dolares.append(valor_elem)
                total.append(valor_elem*DolVal)
            else:
                total_pesos.append(valor_elem)
                total.append(valor_elem)
        except IndexError:
            total.append(0)
    # Reciclo las variables reescribiéndolas
    total = round(sum(total), 2)
    total_pesos = round(sum(total_pesos), 2)
    total_dolares = round(sum(total_dolares), 2)
    return total, total_pesos, total_dolares


# %%


def Ingreso():
    """
    Ingresa el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    Modificado: 21-03-2020  01:38
        Ahora se elije la cuenta en vez de ingresarla manualmente
    """
    nombre = Asignador_cuentas()
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = input("\nCantidad de dinero a ingresar\n")
    categoria = input("\nCategoría: \n")
    subcategoria = input("\nSubcategoría: \n")
    descripcion = input("\nDescripción: \n")
    extraccion = "0.00"  # esto siempre debería ser 0 al ingresar dinero
    gasto = "0.00"  # esto siempre debería ser 0 al ingresar dinero
    if len(datos) == 0:
        total = ingreso
    else:
        total = str(round(float(ingreso) + datos[-1, 2], 2))
    balance = "0"  # TODO: ver si balance es necesario
    Campos = [fecha, hora, total, ingreso, extraccion,
              gasto, categoria, subcategoria, descripcion,
              balance]
    # Escribo la fila que se va a appendear al archivo
    fila = "\t".join(Campos) + "\n"
    # La appendeo al archivo
    with open(nombre, "a") as micuenta:
        micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final["Total"].values[-1],
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Extraccion():
    """
    Extrae el dinero en la cuenta correcta, en la columna correcta
    Completa el resto de las columnas con información repetida de ser
    necesario
    Modificado: 21-03-2020  01:39
        Ahora se elije la cuenta en vez de ingresarla manualmente
    """
    nombre = Asignador_cuentas()
    # se fija si el archivo de la cuenta existe
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = "0.00"  # esto siempre debería ser 0 al extraer dinero
    gasto = "0.00"  # esto es 0 por definicion de extraccion =/= gasto
    if len(datos) == 0:
        print("\nAún no se ha ingresado dinero en la cuenta\n")
    else:
        extraccion = input("\nCantidad de dinero a extraer\n")
        if datos[-1, 2] < float(extraccion):
            print("\nNo hay dinero suficiente en la cuenta\n")
        else:
            categoria = input("\nCategoría: \n")
            subcategoria = input("\nSubcategoría: \n")
            descripcion = input("\nDescripción: \n")
            total = str(round(datos[-1, 2] - float(extraccion), 2))
            balance = "0"  # TODO: ver si balance es necesario
            Campos = [fecha, hora, total, ingreso, extraccion,
                      gasto, categoria, subcategoria, descripcion,
                      balance]
            # Escribo la fila que se va a appendear al archivo
            fila = "\t".join(Campos) + "\n"
            # La appendeo al archivo
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final["Total"].values[-1],
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Gasto():
    """
    Genera un gasto en la cuenta indicada
    """
    nombre = Asignador_cuentas()
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    ingreso = "0.00"  # esto siempre debería ser 0 al hacer un gasto
    extraccion = "0.00"  # esto siempre debería ser 0 al hacer un gasto
    if len(datos) == 0:
        return print("\nNo hay dinero en la cuenta\n")
    else:
        valor = input("\nValor del gasto\n")
        if datos[-1, 2] < float(valor):
            print("\nNo hay dinero suficiente en la cuenta\n")
        else:
            categoria = input("\nCategoría: \n")
            subcategoria = input("\nSubcategoría: \n")
            descripcion = input("\nDescripción: \n")
            total = str(round(datos[-1, 2] - float(valor), 2))
            balance = "0"  # TODO: ver si balance es necesario
            Campos = [fecha, hora, total, ingreso, extraccion,
                      valor, categoria, subcategoria, descripcion,
                      balance]
            # Escribo la fila que se va a appendear al archivo
            fila = "\t".join(Campos) + "\n"
            # La appendeo al archivo
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre, sep="\t", encoding="latin1")
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final["Total"].values[-1],
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Transferencia():
    """
    creada 10-02-2019
    Funcion de transferencias
    Modificado: 21-03-2020  01:42
        Ahora se elijen las cuentas en vez de ingresarlas manualmente
    """
    # Abro la cuenta de salida
    print("Cuenta salida:")
    nombre_salida = Asignador_cuentas()
    info_salida = pd.read_csv(nombre_salida, sep="\t", encoding="latin1")
    # Si la cuenta de saldia está vacía, o no tiene dinero, se cancela la
    # transferencia
    if len(info_salida) == 0 or info_salida["Total"].values[-1] == 0:
        return print("\nNo hay dinero en la cuenta %s\n" % nombre_salida[:-10])
    # Abro la cuenta de entrada
    print("cuenta entrada:")
    nombre_entrada = Asignador_cuentas()
    info_entrada = pd.read_csv(nombre_entrada, sep="\t", encoding="latin1")
    try:
        tot_entrada_i = info_entrada["Total"].values[-1]
    except IndexError:
        tot_entrada_i = 0.0
    # No permito transferencias a una misma cuenta.
    if nombre_entrada == nombre_salida:
        return print("\nNo tiene sentido transferir a una misma cuenta!!\n")
    # Fecha y hora
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    # Valor a transferir
    valor = input("\nCantidad de dinero a transferir\n")
    tot_salida_i = info_salida["Total"].values[-1]
    if tot_salida_i < float(valor):
        print("\nNo hay dinero suficiente en la cuenta %s"
              % nombre_salida[:-10])
    else:
        categoria = "Transferencia"
        subcategoria_salida = "Transferencia de salida"
        descripcion_salida = ("Transferencia a %s" % nombre_entrada
                              .strip("CUENTA.txt"))
        subcategoria_entrada = "Transferencia de entrada"
        descripcion_entrada = ("Transferencia de %s" % nombre_salida
                               .strip("CUENTA.txt"))
        tot_salida_f = str(round(tot_salida_i - float(valor), 2))
        tot_entrada_f = str(round(tot_entrada_i + float(valor), 2))
        balance = gasto = extraccion = ingreso = "0.00"
        # TODO: ver si balance es necesario
        Campos_entrada = [fecha, hora, tot_entrada_f, valor, extraccion,
                          gasto, categoria, subcategoria_entrada,
                          descripcion_entrada, balance]
        Campos_salida = [fecha, hora, tot_salida_f, ingreso, valor,
                         gasto, categoria, subcategoria_salida,
                         descripcion_salida, balance]
        # Escribo las filas que se van a appendear al archivo
        fila_entrada = "\t".join(Campos_entrada) + "\n"
        fila_salida = "\t".join(Campos_salida) + "\n"
        # Las appendeo a los archivos
        with open(nombre_entrada, "a") as micuenta:
            micuenta.write(fila_entrada)
        with open(nombre_salida, "a") as micuenta:
            micuenta.write(fila_salida)


def Reajuste():
    """
    17-12-2019
    Funcion que modifica el total del dinero en la cuenta y lo guarda como
    gasto(ingreso) llenando los campos de categoria, subcategoria y
    descripción de la siguiente manera
        Categoria: Reajuste
        Subcategoria: Negativo(Positivo)
        Descripción: Reajuste Negativo(Positivo) de saldo
    Modificada 21-03-2020  01:52
        Ahora se ingresa el numero de la cuenta en vez de manualmente el
        nombre de la cuenta
    """
    nombre = Asignador_cuentas()
    # Abre y lee los datos de la cuenta
    contenido_cuenta = pd.read_csv(nombre, sep="\t", encoding="latin1")
    datos = contenido_cuenta.values
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    total = input("\nIngrese el saldo actual\n")
    categoria = "Reajuste"
    if datos[-1, 2] < float(total):
        subcategoria = "Positivo"
        descripcion = "Reajuste positivo de saldo"
        extraccion = "0.00"
        gasto = "0.00"
        balance = "0.00"
        ingreso = str(round(float(total) - datos[-1, 2], 2))
        Campos = [fecha, hora, total, ingreso, extraccion,
                  gasto, categoria, subcategoria, descripcion,
                  balance]
    else:
        subcategoria = "Negativo"
        descripcion = "Reajuste negativo de saldo"
        ingreso = "0.00"
        gasto = "0.00"
        balance = "0.00"
        extraccion = str(round(datos[-1, 2] - float(total), 2))
        Campos = [fecha, hora, total, ingreso, extraccion,
                  gasto, categoria, subcategoria, descripcion,
                  balance]
    # Escribo la fila que se va a appendear al archivo
    fila = "\t".join(Campos) + "\n"
    # La appendeo al archivo
    with open(nombre, "a") as micuenta:
        micuenta.write(fila)
    dinero_final = pd.read_csv(nombre,
                               sep="\t",
                               encoding="latin1").values[-1, 2]
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Balance():  # creada 12-08-2019
    """
    Funcion que guarda en cada transaccion el saldo total de las cuentas
    en función de la fecha.
        Si no está creado el archivo 'Balance.txt' lo crea y guarda el
        primer dato.
        Si ya está creado el archivo 'Balance.txt' appendea los nuevos
        datos.
    Esta función está sólo para ser usada por las funciones que modifican
    los saldos de las cuentas de alguna manera (Gasto(), Ingreso(), etc). No
    usar por usar porque va a appendear datos al pedo.
    """
    total, total_pesos, total_dolares = Total()
    fecha = Fecha()["Fecha"]
    hora = Fecha()["hora"]
    if not os.path.isfile("Balance.txt"):
        with open("Balance.txt", "x") as balance:
            balance.write("Hora\tFecha\tTotal\tTotal_pesos\tTotal_dolares\n")
            balance.write("%s\t%s\t%s\t%s\t%s\n" % (hora, fecha, total,
                                                    total_pesos,
                                                    total_dolares))
    elif os.path.isfile("Balance.txt"):
        with open("Balance.txt", "a") as balance:
            balance.write("%s\t%s\t%s\t%s\t%s\n" % (hora, fecha, total,
                                                    total_pesos,
                                                    total_dolares))
    else:
        print("\nO Se ErRoR rE lOcO\n")


def BalanceGraf():  # 10-09-2019 Se agrega el graficador de balance
    """
    30-08-2019
    Primera aproximación a grafico de balance con fechas y horas.
    Lo que quiero lograr:
        Lograr poner tics solo en los meses.
            Lograr que los puntos se separen
            segun su valor horario. ->10-09-2020 solucionado
    """
    data = pd.read_csv("Balance.txt", sep="\t")
    # Armo un string con la fecha y la hora en el formato del .txt
    T = data["Fecha"] + "-" + data["Hora"]
    # Especifico ese formato acá, para usarlo en la funcion strptime
    formato = "%d-%m-%Y-%H:%M:%S"
    # transformo el string a un objeto datetime usando el formato dado
    Tiempo = [datetime.strptime(i, formato) for i in T]
    plt.plot(Tiempo, data["Total"],
             'o-',
             alpha=.5,
             fillstyle="full",
             markersize=5,
             label="Total: $%.2f"
             % data["Total"].values[-1])
    plt.plot(Tiempo, data["Total_pesos"],
             'o-',
             alpha=.5,
             fillstyle="none",
             markersize=3,
             label="Total de pesos: $%.2f"
             % data["Total_pesos"].values[-1])
    plt.plot(Tiempo, data["Total_dolares"],
             '-',
             alpha=.5,
             fillstyle="none",
             label="Total de dolares: u$s%.2f"
             % data["Total_dolares"].values[-1])
    plt.grid()
    plt.legend()
    plt.xticks(rotation=25)
    plt.show()


def Filtro():  # 10/01/2020
    """
    Con esta funcion se puede ver puntualmente categorias de gastos/ingresos
    para poder llevar un control más sencillo y rápido de cuánto se está
    gastando/ingresando.
    """
    nombre = Asignador_cuentas()
    # Abre y lee los datos de la cuenta
    datos = pd.read_csv(nombre, sep="\t", encoding="latin1")
    Categoria = input("\nIngrese la categoría\n")
    datos = datos[datos["Categoria"] == Categoria]
    print(datos)
    respuesta = input("\n\nSeguir filtrando?\n\nsi/no\n\n")
    if respuesta == "si":
        Subcategoria = input("\nIngrese la subcategoría\n")
        datos = datos[datos["Subcategoria"] == Subcategoria]
        return datos
    else:
        return datos


# %%

def balances(cuenta: str, month: int, year: int):
    """
    Permite ver de forma fácil el balance mensual de la cuenta: Ingresos,
    Gastos y Balance = Ingresos - Gastos.
    Inputs:
        cuenta: str
        Nombre de la cuenta como archivo o path del archivo cuenta. Solo hace
        falta el nombre, ej: MercadoPagoCUENTA.txt
        month: int
        Numero del mes deseado para ver el balance: Válidos del 1 al 12
        year: int
        Número del año deseado para ver el balance: Válidos 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por cuenta: float
    """
    df = pd.read_csv(cuenta, sep="\t", index_col=("Fecha"), parse_dates=True,
                     dayfirst=True, encoding="latin1")
    montly_src = df[(df.index.month == month) & (df.index.year == year)
                    & (df["Categoria"] != "Transferencia")]
    montly_spend = montly_src["Gasto"].sum()
    montly_spend += montly_src["Extracciones"].sum()
    montly_earn = montly_src["Ingresos"].sum()
    balance = montly_earn - montly_spend

    return {"Ingresos_m": round(montly_earn, 2),
            "Gasto_m": round(montly_spend, 2),
            "Balance_m": round(balance, 2)}


def balances_totales(month: int, year: int, verbose=False):
    """
    Permite ver el balance total entre todas las cuentas para un dado mes y año
    del usuario: Ingresos totales, Gastos totales y Balance total. Usa la
    función balances().
    Inputs:
        month: int
        Numero del mes deseado para ver el balance: Válidos del 1 al 12
        year: int
        Número del año deseado para ver el balance: Válidos 2019, 2020, 2021
    returns: dic
        Ingresos, Gastos y Balances mensuales por usuario: float
    """
    ingresos_tot = gastos_tot = balances_tot = 0
    for cuenta in os.listdir():
        if "CUENTA" in cuenta and "DOL" not in cuenta:
            try:
                dic_c = balances(cuenta, month, year)
            except AttributeError as e:
                if verbose is True:
                    print("Error en la cuenta: ", cuenta)
                    print(e)
            ingresos_tot += dic_c["Ingresos_m"]
            gastos_tot += dic_c["Gasto_m"]
            balances_tot += dic_c["Balance_m"]

    return {"Ingresos_tot": round(ingresos_tot, 2),
            "Gasto_tot": round(gastos_tot, 2),
            "Balance_tot": round(balances_tot, 2)}

# %%
IniciarSesion()
