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
            raise KeyError(f"El nombre de la columna '{mes}' no es válido. Por favor, asegúrate de ingresar el nombre correcto de la columna.")

        # Filtra el DataFrame por el mes especificado
        data_filtered = data[mes]

        if not data_filtered.empty:
            # Realiza una función de agregación para el mes especificado
            numero_clientes = data_filtered.sum()
            return {"El número de clientes para el mes {} es:".format(mes): numero_clientes}
        else:
            return {"El número de clientes para el mes {} es:".format(mes): 0}  # Si no hay clientes, el número es cero
    
    except KeyError as e:
        # Si hay un error de clave (KeyError), proporciona mensajes de error
        if 'Mes Registro' in data.columns and 'Mes de Abandono (Churn)' in data.columns:
            fecha_minima = data['Mes Registro'].min()
            fecha_maxima = data['Mes de Abandono (Churn)'].max()

            # Truncamos la fecha a Año-Mes
            fecha_minima_truncada = fecha_minima.strftime('%Y-%m')
            fecha_maxima_truncada = fecha_maxima.strftime('%Y-%m')

            return {
                "error": f"La columna '{mes}' no es válida. Por favor, asegúrate de ingresar el nombre correcto de la columna.",
                "formato_fechas": f"El formato de las fechas es: M/YYYY. Los registros comienzan en {fecha_minima_truncada} y terminan en {fecha_maxima_truncada}."
            }
        
        else:
            return {"error": f"La columna '{mes}' no es válida. Además, las columnas de fecha necesarias no están presentes en el DataFrame."}        

def Mes_mayorClientes(data):
    # Obtener el total de clientes nuevos por mes de registro
    clientes_por_mes = data.groupby('Mes Registro').size()

    # Encontrar el mes con la mayor cantidad de nuevos clientes
    mes_mas_clientes = clientes_por_mes.idxmax()  # Obtiene el índice (mes) con el máximo valor
    num_clientes = clientes_por_mes.max()  # Obtiene el valor máximo (número de clientes)

    return {
        "Mes con mayor número de nuevos clientes": mes_mas_clientes,
        "Número de nuevos clientes en el mes": num_clientes
    }

def Mes_mayor_abandono(data):
    # Obtener el total de clientes que abandonaron por mes
    clientes_abandono_por_mes = data.groupby('Mes de Abandono (Churn)').size()

    # Encontrar el mes con la mayor cantidad de abandono de clientes
    mes_mas_abandono = clientes_abandono_por_mes.idxmax()  # Obtiene el índice (mes) con el máximo valor
    num_clientes_abandono = clientes_abandono_por_mes.max()  # Obtiene el valor máximo (número de clientes que abandonaron)

    return {
        "Mes con mayor número de clientes que abandonaron": mes_mas_abandono,
        "Número de clientes que abandonaron en el mes": num_clientes_abandono
    }

def Mes_Mayor_Porcentaje_Retencion(data, mes:str):
    # Cuenta el número de clientes por mes de inicio
    clientes_por_mes_inicio = data.groupby('Mes Registro').size()

    # Cuenta el número de clientes por mes de fin
    clientes_por_mes_fin = data.groupby('Mes de Abandono (Churn)').size()

    # Ordena los datos por fecha
    clientes_por_mes_fin = clientes_por_mes_fin.sort_index()

    # Obtener el total de clientes activos hasta el mes dado
    nuevos_clientes_hasta_mes = clientes_por_mes_inicio.loc[mes]

    # Obtener el total de abandonos hasta el mes dado
    abandonos_hasta_mes = clientes_por_mes_fin.loc[:mes].sum()

    # Calcular el porcentaje de retención para el mes dado
    porcentaje_retencion_mes = (((nuevos_clientes_hasta_mes - abandonos_hasta_mes) / len(data)) - 1) * -100

    return {
        "Mes": mes,
        "Porcentaje de retención para el mes dado": porcentaje_retencion_mes

    }

def Mes_Mayor_Porcentaje_Retencion_Total(data):
    # Diccionario para almacenar los porcentajes de retención para cada mes
    porcentajes_retencion = {}

    # Iterar sobre todos los meses en los datos
    for mes in data['Mes Registro'].unique():
        # Calcular el porcentaje de retención para el mes dado
        resultado_mes = Mes_Mayor_Porcentaje_Retencion(data, mes)
        
        # Almacenar el porcentaje de retención para este mes en el diccionario
        porcentajes_retencion[mes] = resultado_mes["Porcentaje de retención para el mes dado"]

    # Encontrar el mes con el mayor porcentaje de retención
    mes_mayor_retencion = max(porcentajes_retencion, key=porcentajes_retencion.get)
    mayor_porcentaje_retencion = porcentajes_retencion[mes_mayor_retencion]

    return {
        "Mes con mayor porcentaje de retención": mes_mayor_retencion,
        "Mayor porcentaje de retención": mayor_porcentaje_retencion
    }

def Mes_Mayor_Porcentaje_Abandono(data, mes):
    # Calcular el porcentaje de retención para el mes dado
    resultado_retencion = Mes_Mayor_Porcentaje_Retencion(data, mes)
    porcentaje_retencion_mes = resultado_retencion["Porcentaje de retención para el mes dado"]

    # Calcular el porcentaje de abandono como el inverso del porcentaje de retención
    #Aplicando las bases estadisticas de Q=1-P
    porcentaje_abandono_mes = (1- (porcentaje_retencion_mes/100)) * 100

    return {
        "Mes": mes,
        "Porcentaje de abandono para el mes dado": porcentaje_abandono_mes
    }

'''def Mes_Mayor_Porcentaje_Abandono_Total(data):
    # Diccionario para almacenar los porcentajes de abandono para cada mes
    porcentajes_abandono = {}

    # Iterar sobre todos los meses en los datos
    for mes in data['Mes de Abandono (Churn)'].unique():
        # Calcular el porcentaje de abandono para el mes dado
        resultado_mes = Mes_Mayor_Porcentaje_Abandono(data, mes)
        
        # Almacenar el porcentaje de abandono para este mes en el diccionario
        porcentajes_abandono[mes] = resultado_mes["Porcentaje de abandono para el mes dado"]

    # Encontrar el mes con el mayor porcentaje de abandono
    mes_mayor_abandono = max(porcentajes_abandono, key=porcentajes_abandono.get)
    mayor_porcentaje_abandono = porcentajes_abandono[mes_mayor_abandono]

    return {
        "Mes con mayor porcentaje de abandono": mes_mayor_abandono,
        "Mayor porcentaje de abandono": mayor_porcentaje_abandono
    }'''