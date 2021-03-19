# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 01:20:15 2019

@author: igna
Intento de billetera para control de gastos

Historial de modificaciones:
14/11/2020: Se agrega la excepción a la función Precio_dolar(), si no hay inet
            y se intenta scrapear, captura la excepción y usa el último precio
            de dolar registrado usando los datos del archivo Balance.txt.
            Si no hay dolares en la cuenta, te dice que no hay y te pone el 
            dolar a 0.0, ya que no hace falta usarlo.
12/03/2021: Se modifica sutilmente la función BalanceGraf(). Antes usaba el 
            DataFrame de pandas con los datos del archivo balance, para pasar-
            los a un array de numpy, es decir: 
                data = pd.read_csv(etc...)
                Data = data.values
                ...
            como eso es un paso innecesario, se cambio. Además el código queda
            más descriptivo
"""
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt  # agregado 30-08-2019
from bs4 import BeautifulSoup  # agregado 11-03-2020
from urllib.request import urlopen  # agregado 11-03-2020
directorio = os.path.dirname(os.path.abspath(__file__))  # agregado 22-10-2020
#  directorio = r"C:\Users\igna\Desktop\Igna\Python Scripts\billetera"
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

TODO    Solucionar error
        PermissionError: [WinError 5] Acceso denegado: "nombreusuarUSR"
        al intentar borrar un usuario

TODO    Que no se pueda crear usuario estando logueado en algún usuario

TODO    Separar todo este script en módulos específicos para que no sea
        tanta paja ponerse a editar una función y scrollear como un pelotudo.

TODO    Que no se puedan hace transferencias de cuentas de distintos tipos
        (de pesos a dolares o dolares a pesos)
        
TODO    Ver qué son las excepciones que no están comentadas ni explicadas
        porque ya no me acuerdo si están al pedo, si están bien puestas,
             si están haciendo cagada, etc.
"""


def Fecha():
    """
    simplemente genera la hora en formato argento
    """
    fecha_hora = datetime.now()
    fecha = str(fecha_hora)[:10]
    hora = str(fecha_hora)[11:19]
    fecha = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")
    return fecha, hora


def Precio_dolar():
    """
    Creada (aprox) 21-03-2020
    Scrapea el precio del dolar del banco nacion
    TODO: meter exceptions que manejen las excepciones
    ver la forma que si no anda la pagina del banco central, use otra.
    Modificada 14/11/2020 para manejar algunas excepciones
    """
    urlDOLAR1 = "http://www.bna.com.ar/Personas"
    # urlDOLAR2 = "https://www.cotizacion-dolar.com.ar/cotizacion_hoy.php"
    # urlDOLAR3 = "https://banco.santanderrio.com.ar/exec/cotizacion/index.jsp"
    # urlDOLAR4 = "https://www.bancoprovincia.com.ar/Productos/inversiones/
    # dolares_bip/dolares_bip_info_gral"
    # urlDOLAR5 = "https://www.bancogalicia.com/banca/online/web/Personas/
    # ProductosyServicios/Cotizador"
    # Try: intenta scrappear, si no puede captura la excepción
    try:
        url = urlopen(urlDOLAR1)
        soup = BeautifulSoup(url.read(), "html.parser")
        target = soup.find("table")
        text = target.text
        PrecioDolar = text[41:46]
    except:
        # Si no pude escrapear viene acá y te avisa que no pudo.
        # Lo proximo que intenta es calcular el último valor del dolar usando
        # los datos el archivo Balance.txt. Si el ultimo dato de Balance es 0
        # dolares, captura la excepción
        print("no se pudo scrappear el dolar, se usó la ultima cotización")
    
        # acá voy a calcular cuánto estuvo el dolar la última vez
        bal_datos = pd.read_csv("Balance.txt",
                                skiprows = 1,
                                sep="\t",
                                encoding="latin1").values
        tot_dinero = bal_datos[-1,2]
        tot_pesos = bal_datos[-1,3]
        tot_dolares = bal_datos[-1,4]
        # si el ultima dato de balance es 0 dolares, necesito capturar la 
        # division por 0 de la siguiente cuenta. En ese caso, asumo que no hay
        # dolares en la cuenta (si en balance la columna de dolar es 0,
        # entonces no hay dolares)
        try:
            PrecioDolar = str(round((tot_dinero - tot_pesos)/tot_dolares, 2))
        except ZeroDivisionError:
            print("No hay dolares, asi que no importa cuanto vale")
            PrecioDolar = "0.0"
        
    return float(PrecioDolar.replace(",", "."))


def Info():  # Creada 15-06-2019  # Modificada 21-03-2020
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
    str_funciones = "\nFecha()\nPrecio_dolar()\nInfo()\n"\
        + "\nCrearUsuario()\nIniciarSesion()\nCerrarSesion()\n"\
        + "\nCrear_cuenta()\nLista_cuentas()\nDatos_cuenta()"\
        + "\nAsignador_cuentas()\nTotal()\n"\
        + "\nIngreso()\nExtraccion()\nGasto()\nTransferencia()\nReajuste()"\
        + "\nBalance()<---NO USAR-Ver help(Balance)"\
        + "\nBalanceGraf()\nFiltro()\n"
    print("Funciones:\n", str_funciones)
    print("Cuentas existentes:\n", informacion)
    print("Dolares totales: $%.2f" % total_dolares)
    print("Pesos totales: $%.2f" % total_pesos)
    print("Dinero total en cuentas: $%.2f" % total)
    # return informacion


# %%


def CrearUsuario():  # creada 10-02-2019
    nombre = input("\nIngrese el nombre de usuario\n") + "USR"
    if os.path.isdir(nombre):  # 10/01/2020 msj al intentar crear usr existente
        print("\nYa existe el usuario\n")
    else:
        os.makedirs(nombre)
        print("\nSe creo el usuario %s\n" % nombre[:-3])


def IniciarSesion():  # creada 10-02-2019
    nombre = input("\nNombre de usuario\n") + "USR"
    if os.path.isdir(nombre):
        Dir = directorio + "/" + "%s" % nombre
        os.chdir(Dir)
        print("\nInicio de sesion de %s\n" % nombre[:-3])
        Info()
    else:
        print("\nNo existe el usuario\n")


def CerrarSesion():  # creada 10-02-2019
    os.chdir(directorio)
    print("\nSe ha cerrado sesión\n")


"""
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
            os.remove(nombre)
            print("\nSe eliminó el usuario %s\n" % nombre[:-10])
        else:
            print("\nNo se eliminó el usuario %s\n" % nombre[:-10])
    else:
        print("\nNo existe el usuario\n")
"""

# %%


def Crear_cuenta():
    """
    Crea un .txt cuyo nombre será el nombre de la cuenta
    """
    nombre = input("\nIntrduzca el nombre para la nueva cuenta\n")
    tipo_cuenta = input("\nIngresar 0 para cuenta en pesos\n"
                        "Ingresar 1 para cuenta en dolares\n")
    archivo = nombre
    if tipo_cuenta == "0":
        archivo += "CUENTA.txt"
    elif tipo_cuenta == "1":
        archivo += "CUENTA_DOL.txt"
    else:
        print("\n %s inválido\n" % tipo_cuenta)
    Encabezados = ["Fecha", "hora", "Total", "Ingresos", "Extracciones",
                   "Gasto", "Categoria", "Subcategoria", "Descripcion",
                   "Balance"]
    fila = ""
    for elementos in Encabezados:
        fila += elementos + "\t"
    fila = fila[:-1]  # Borra el "\t" del final
    fila += "\n"
    fila += "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n"
    with open(archivo, "x") as micuenta:
        micuenta.write(fila)
    print("\nSe ha creado la cuenta %s\n" % nombre)


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
        print("\nSe eliminó la cuenta %s\n" % nombre[:-10])
    else:
        print("\nNo se eliminó la cuenta %s\n" % nombre[:-10])


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
    for i in range(len(alfabeto)):
        Dic.update({str(i+1): alfabeto[i]})
        cuenta = alfabeto[i].replace("CUENTA", "").replace("_DOL", "")\
            .replace(".txt", "")
        Cuentas += "\n" + str(i+1) + ": " + cuenta + "\n"
    numero = input("\nElija la cuenta\n" + Cuentas + "\n")
    try:
        NombreCuenta = Dic[numero]
        return NombreCuenta
    except:
        print("\nEl numero pifiaste ameo\n")


def Total():
    # lista con los nombres de los archivos de cuenta
    Lista = Lista_cuentas()
    DolVal = Precio_dolar()
    # lista con el saldo total de dinero de cada cuenta
    total = []
    total_pesos = []
    total_dolares = []
    for elem in Lista:
        valor_elem = pd.read_csv(elem,
                                 sep="\t",
                                 encoding="latin1").values[-1, 2]
        try:
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
    fecha = Fecha()[0]
    hora = Fecha()[1]
    ingreso = input("\nCantidad de dinero a ingresar\n")
    categoria = input("\nCategoría: \n")
    subcategoria = input("\nSubcategoría: \n")
    descripcion = input("\nDescripción: \n")
    extraccion = "0"  # esto siempre debería ser 0 al ingresar dinero
    gasto = "0"  # esto siempre debería ser 0 al ingresar dinero
    if len(datos) == 0:
        total = ingreso
    else:
        total = str(round(float(ingreso) + datos[-1, 2],2))
    balance = "0"  # TODO: ver si balance es necesario
    Campos = [fecha, hora, total, ingreso, extraccion,
              gasto, categoria, subcategoria, descripcion,
              balance]
    fila = ""
    for elementos in Campos:
        fila += elementos + "\t"
    fila = fila[:-1]  # Borra el "\t" del final
    fila += "\n"
    with open(nombre, "a") as micuenta:
        micuenta.write(fila)
    dinero_final = pd.read_csv(nombre,
                               sep="\t",
                               encoding="latin1").values[-1, 2]
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
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
    fecha = Fecha()[0]
    hora = Fecha()[1]
    ingreso = "0"  # esto siempre debería ser 0 al extraer dinero
    gasto = "0"  # esto es 0 por definicion de extraccion =/= gasto
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
            total = str(round(datos[-1, 2] - float(extraccion),2))
            balance = "0"  # TODO: ver si balance es necesario
            Campos = [fecha, hora, total, ingreso, extraccion,
                      gasto, categoria, subcategoria, descripcion,
                      balance]
            fila = ""
            for elementos in Campos:
                fila += elementos + "\t"
            fila = fila[:-1]  # Borra el "\t" del final
            fila += "\n"
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre,
                               sep="\t",
                               encoding="latin1").values[-1, 2]
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
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
    fecha = Fecha()[0]
    hora = Fecha()[1]
    ingreso = "0"  # esto siempre debería ser 0 al hacer un gasto
    extraccion = "0"  # esto siempre debería ser 0 al hacer un gasto
    if len(datos) == 0:
        print("\nNo hay dinero en la cuenta\n")
    else:
        valor = input("\nValor del gasto\n")
        if datos[-1, 2] < float(valor):
            print("\nNo hay dinero suficiente en la cuenta\n")
        else:
            categoria = input("\nCategoría: \n")
            subcategoria = input("\nSubcategoría: \n")
            descripcion = input("\nDescripción: \n")
            total = str(round(datos[-1, 2] - float(valor),2))
            balance = "0"  # TODO: ver si balance es necesario
            Campos = [fecha, hora, total, ingreso, extraccion,
                      valor, categoria, subcategoria, descripcion,
                      balance]
            fila = ""
            for elementos in Campos:
                fila += elementos + "\t"
            fila = fila[:-1]  # Borra el "\t" del final
            fila += "\n"
            with open(nombre, "a") as micuenta:
                micuenta.write(fila)
    dinero_final = pd.read_csv(nombre,
                               sep="\t",
                               encoding="latin1").values[-1, 2]
    total, total_pesos, total_dolares = Total()
    print("\nDinero en cuenta: $%.2f\n" % dinero_final,
          "\nDinero total %.2f\n" % total)
    Balance()  # agregado 12-08-2019


def Transferencia():
    """
    creada 10-02-2019
    Funcion de transferencias
    Modificado: 21-03-2020  01:42
        Ahora se elijen las cuentas en vez de ingresarlas manualmente
    """
    print("Cuenta salida:")
    nombre_salida = Asignador_cuentas()
    print("cuenta entrada:")
    nombre_entrada = Asignador_cuentas()
    # si las dos cuentas existen
    contenido_salida = pd.read_csv(nombre_salida,
                                   sep="\t",
                                   encoding="latin1")
    contenido_entrada = pd.read_csv(nombre_entrada,
                                    sep="\t",
                                    encoding="latin1")
    datos_salida = contenido_salida.values
    datos_entrada = contenido_entrada.values
    fecha = Fecha()[0]
    hora = Fecha()[1]
    if len(datos_salida) == 0:
        print("\nNo hay dinero en la cuenta %s\n" % nombre_salida[:-10])
    else:
        valor = input("\nCantidad de dinero a transferir\n")
        if datos_salida[-1, 2] < float(valor):
            print("\nNo hay dinero suficiente en la cuenta %s"
                  % nombre_salida[:-10])
        categoria = "Transferencia"
        subcategoria_salida = "Transferencia de salida"
        descripcion_salida = "Transferencia a %s" % nombre_entrada[:-10]
        subcategoria_entrada = "Transferencia de entrada"
        descripcion_entrada = "Transferencia de %s" % nombre_salida[:-10]
        total_salida = str(round(datos_salida[-1, 2] - float(valor),2))
        total_entrada = str(round(datos_entrada[-1, 2] + float(valor),2))
        balance = gasto = extraccion = ingreso = "0"
        # TODO: ver si balance es necesario
        Campos_entrada = [fecha, hora, total_entrada, valor, extraccion,
                          gasto, categoria, subcategoria_entrada,
                          descripcion_entrada, balance]
        Campos_salida = [fecha, hora, total_salida, ingreso, valor,
                         gasto, categoria, subcategoria_salida,
                         descripcion_salida, balance]
        fila_entrada = ""
        fila_salida = ""
        for elementos in Campos_entrada:
            fila_entrada += elementos + "\t"
        fila_entrada = fila_entrada[:-1]  # Borra el "\t" de mas
        fila_entrada += "\n"
        for elementos in Campos_salida:
            fila_salida += elementos + "\t"
        fila_salida = fila_salida[:-1]  # Borra el "\t" de mas
        fila_salida += "\n"
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
    fecha = Fecha()[0]
    hora = Fecha()[1]
    total = input("\nIngrese el saldo actual\n")
    categoria = "Reajuste"
    if datos[-1, 2] < float(total):
        subcategoria = "Positivo"
        descripcion = "Reajuste positivo de saldo"
        extraccion = "0"
        gasto = "0"
        balance = "0"
        ingreso = str(round(float(total) - datos[-1, 2],2))
        Campos = [fecha, hora, total, ingreso, extraccion,
                  gasto, categoria, subcategoria, descripcion,
                  balance]
    else:
        subcategoria = "Negativo"
        descripcion = "Reajuste negativo de saldo"
        ingreso = "0"
        gasto = "0"
        balance = "0"
        extraccion = str(round(datos[-1, 2] - float(total),2))
        Campos = [fecha, hora, total, ingreso, extraccion,
                  gasto, categoria, subcategoria, descripcion,
                  balance]
    fila = ""
    for elementos in Campos:
        fila += elementos + "\t"
    fila = fila[:-1]  # Borra el "\t" del final
    fila += "\n"
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
    hora = Fecha()[0]
    fecha = Fecha()[1]
    if not os.path.isfile("Balance.txt"):
        with open("Balance.txt", "x") as balance:
            balance.write("Hora\tFecha\tTotal\tTotal_pesos\tTotal_dolares\n")
            balance.write("%s\t%s\t%s\t%s\t%s\n" % (fecha,
                                                    hora,
                                                    total,
                                                    total_pesos,
                                                    total_dolares))
    elif os.path.isfile("Balance.txt"):
        with open("Balance.txt", "a") as balance:
            balance.write("%s\t%s\t%s\t%s\t%s\n" % (fecha,
                                                    hora,
                                                    total,
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
    T = data["Fecha"] + "-" +data["Hora"]
    formato = "%d-%m-%Y-%H:%M:%S"
    Tiempo = [datetime.strptime(i, formato) for i in T]
    plt.plot(Tiempo, data["Total"],
             'o-',
             fillstyle="full",
             markersize=5,
             label="Total")
    plt.plot(Tiempo, data["Total_pesos"],
             'o-',
             fillstyle="none",
             markersize=3,
             label="Total de pesos $")
    plt.plot(Tiempo, data["Total_dolares"],
             '-',
             fillstyle="none",
             label="Total de dolares u$s")
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


IniciarSesion()
