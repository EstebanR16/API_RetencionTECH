import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import seaborn as sns

data=pd.read_csv("retencion-por-mes.csv")
data2=pd.read_csv("retencion-por-trimestre.csv")

data['Estado Cliente']= data['Estado Cliente'].astype('category')

# Convertimos la columna 'Mes de Abandono (Churn)' y 'Mes Registro' en un formato de fecha
data['Mes de Abandono (Churn)'] = pd.to_datetime(data['Mes de Abandono (Churn)'])
data['Mes Registro'] = pd.to_datetime(data['Mes Registro'])

# Truncar las columnas al mes --> y se vuelve a convertir los datos a tipo object
data['Mes de Abandono (Churn)'] = data['Mes de Abandono (Churn)'].dt.strftime('%Y-%m')
data['Mes Registro'] = data['Mes Registro'].dt.strftime('%Y-%m')



def Clientes_por_Mes(mes: str):
    try:
        # Verifica si la columna mes existe en el DataFrame
        if mes not in data.columns:
            raise KeyError("El nombre de la columna '{}' no es válido. Por favor, asegúrate de ingresar el nombre correcto de la columna. ".format(mes))

        # Filtra el DataFrame por el mes especificado
        data_filtered = data[mes]

        if not data_filtered.empty:
            # Realiza una función de agregación para el mes especificado
            numero_clientes = data_filtered.sum()
            return {
                "El número de clientes para el mes {} es:".format(mes): numero_clientes
            }
        else:
            return {
                "El número de clientes para el mes {} es:".format(mes): 0  # Si no hay clientes, el número es cero
            }
    except KeyError:
        # Si hay un error de clave (KeyError), proporciona mensajes de error
        # Calculamos el mínimo y el máximo de las fechas si las columnas existen
        if 'Mes Registro' in data.columns and 'Mes de Abandono (Churn)' in data.columns:
            fecha_minima = data['Mes Registro'].min()
            fecha_maxima = data['Mes de Abandono (Churn)'].max()

            # Truncamos la fecha a Año-Mes
            fecha_minima_truncada = fecha_minima.strftime('%Y-%m')
            fecha_maxima_truncada = fecha_maxima.strftime('%Y-%m')

            
            print("El nombre de la columna '{}' no es válido. Por favor, asegúrate de ingresar el nombre correcto de la columna.".format(mes))
            print("\nEl formato de las fechas es: M/YYYY. Los registros comienzan en {} y terminan en {}.".format(fecha_minima_truncada, fecha_maxima_truncada))

        else:
            
            print("La columna a la que intentas ingresar no es valida")
        

def Mes_mayorClientes(data):
    # Diccionario para almacenar el recuento de nuevos clientes por mes
    nuevos_clientes_por_mes = {}

    # Iterar sobre las columnas del DataFrame para contar los nuevos clientes por mes
    for i, columna in enumerate(data.columns[4:], start=1):
        # Filtrar clientes nuevos para el mes actual
        clientes_mes_actual = data[columna].dropna()
        # Excluir clientes que ya estaban registrados en el mes anterior (si corresponde)
        if i > 1:  # Excluir el primer mes
            clientes_mes_anterior = data[data.columns[i - 1]].dropna()
            clientes_mes_actual = clientes_mes_actual[~clientes_mes_actual.isin(clientes_mes_anterior)]
        # Contar el número de nuevos clientes para el mes actual
        count = len(clientes_mes_actual)
        # Almacenar el recuento en el diccionario
        nuevos_clientes_por_mes[columna] = count

    # Encontrar el mes con el segundo mayor recuento de nuevos clientes
    mes_mas_clientes = sorted(nuevos_clientes_por_mes, key=nuevos_clientes_por_mes.get, reverse=True)[1]
    num_clientes = nuevos_clientes_por_mes[mes_mas_clientes]

    return {
        "Mes con mayor número de nuevos clientes": mes_mas_clientes,
        "Número de nuevos clientes en el mes": num_clientes
    }


def Mes_mayor_abandono(data):
    # Diccionario para almacenar el recuento de abandono de clientes por mes
    abandono_por_mes = {}

    # Iterar sobre las columnas del DataFrame para contar el abandono de clientes por mes
    for i, columna in enumerate(data.columns[4:], start=1):  # Excluir el primer mes
        # Filtrar clientes activos para el mes actual
        clientes_mes_actual = data[data[columna].isnull()]
        #clientes_mes_actual = data[columna].dropna()
        # Filtrar clientes activos para el mes anterior
        if i > 1:
            clientes_mes_anterior = data[data[data.columns[i-1]].notna()]
            # Excluir clientes que ya habían abandonado en el mes anterior
            clientes_mes_actual = clientes_mes_actual[~clientes_mes_actual.index.isin(clientes_mes_anterior.index)]
        # Contar el número de clientes abandonados para el mes actual
        count = len(clientes_mes_actual)
        # Almacenar el recuento en el diccionario
        abandono_por_mes[columna] = count

    # Encontrar el mes con el mayor recuento de abandono de clientes
    mes_con_mayor_abandono = max(abandono_por_mes, key=abandono_por_mes.get)
    num_clientes_abandonados = abandono_por_mes[mes_con_mayor_abandono]

    return {
        "Mes con mayor abandono de clientes": mes_con_mayor_abandono,
        "Número de clientes abandonados en ese mes": num_clientes_abandonados
    }


def Porcentaje_Retencion_Abandono(data):
    # Inicializar listas para almacenar los porcentajes de retención y abandono mes a mes
    porcentajes_retencion = []
    porcentajes_abandono = []

    # Iterar sobre las columnas del DataFrame
    for columna in data.columns[4:]:
        # Filtrar clientes activos y churned para el mes actual
        clientes_activos = data[data[columna] == 1] #Esta activo cuando es 1
        clientes_inactivos = data[data[columna].isna()] #inactivo cuando es NaN

        # Contar el número de clientes activos y abandonados para el mes actual
        count_activos = len(clientes_activos)
        count_abandonados = len(clientes_inactivos)

        # Calcular el porcentaje de retención y abandono para el mes actual
        total_clientes_mes = count_activos + count_abandonados
        porcentaje_retencion_mes = (count_activos / total_clientes_mes) * 100
        porcentaje_abandono_mes = (count_abandonados / total_clientes_mes) * 100

        # Almacenar los porcentajes mes a mes
        porcentajes_retencion.append(porcentaje_retencion_mes)
        porcentajes_abandono.append(porcentaje_abandono_mes)

    # Calcular el promedio de los porcentajes de retención y abandono de todos los meses
    promedio_retencion = sum(porcentajes_retencion) / len(porcentajes_retencion)
    promedio_abandono = sum(porcentajes_abandono) / len(porcentajes_abandono)

    return {
        "Porcentaje promedio de retención de clientes": promedio_retencion,
        "Porcentaje promedio de abandono de clientes": promedio_abandono
    }