import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import seaborn as sns

data=pd.read_csv("retencion-por-mes.csv")
data2=pd.read_csv("retencion-por-trimestre.csv")

data['Estado Cliente']= data['Estado Cliente'].astype('category')

# Convertimos la columna 'Mes de Abandono (Churn)' y 'Mes Registro' en un formato de fecha
data['Mes de Abandono (Churn)'] = pd.to_datetime(data['Mes de Abandono (Churn)'], format='%m/%Y')
data['Mes Registro'] = pd.to_datetime(data['Mes Registro'], format='%m/%Y')


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
            result = {"El número de clientes para el mes {} es:".format(mes): numero_clientes}
        else:
            result = {"El número de clientes para el mes {} es:".format(mes): 0}  # Si no hay clientes, el número es cero
    
    except KeyError as e:
        # Si hay un error de clave (KeyError), proporciona mensajes de error
        if 'Mes Registro' in data.columns and 'Mes de Abandono (Churn)' in data.columns:
            fecha_minima = data['Mes Registro'].min()
            fecha_maxima = data['Mes de Abandono (Churn)'].max()

            # Truncamos la fecha a Año-Mes
            fecha_minima_truncada = fecha_minima.strftime('%Y-%m')
            fecha_maxima_truncada = fecha_maxima.strftime('%Y-%m')

            result = {
                "error": f"La columna '{mes}' no es válida. Por favor, asegúrate de ingresar el nombre correcto de la columna.",
                "formato_fechas": f"El formato de las fechas es: M/YYYY. Los registros comienzan en {fecha_minima_truncada} y terminan en {fecha_maxima_truncada}."
            }
        
        else:
            result = {"error": f"La columna '{mes}' no es válida. Además, las columnas de fecha necesarias no están presentes en el DataFrame."}        
    
    return result


def Mes_mayorClientes(data):
    try:
        # Verifica si la columna 'Mes Registro' existe en el DataFrame
        if 'Mes Registro' not in data.columns:
            raise KeyError("La columna 'Mes Registro' es necesaria para calcular el mes con mayor número de nuevos clientes.")

        # Obtener el total de clientes nuevos por mes de registro
        clientes_por_mes = data.groupby('Mes Registro').size()

        # Verifica si hay datos disponibles para calcular
        if clientes_por_mes.empty:
            raise ValueError("No hay datos disponibles para calcular el mes con mayor número de nuevos clientes.")

        # Encontrar el mes con la mayor cantidad de nuevos clientes
        mes_mas_clientes = clientes_por_mes.idxmax()  # Obtiene el índice (mes) con el máximo valor
        num_clientes = int(clientes_por_mes.max())  # Convertir a tipo int

        result = {
            "Mes con mayor número de nuevos clientes": mes_mas_clientes,
            "Número de nuevos clientes en el mes": num_clientes
        }
    
    except KeyError as e:
        result = {"error": str(e)}

    except ValueError as e:
        result = {"error": str(e)}

    except Exception as e:
        result = {"error": f"Ocurrió un error inesperado al procesar la solicitud: {str(e)}"}

    return result



def Mes_mayor_abandono(data):
    try:
        # Verifica si la columna 'Mes de Abandono (Churn)' existe en el DataFrame
        if 'Mes de Abandono (Churn)' not in data.columns:
            raise KeyError("La columna 'Mes de Abandono (Churn)' es necesaria para calcular el mes con mayor número de clientes que abandonaron.")

        # Obtener el total de clientes que abandonaron por mes
        clientes_abandono_por_mes = data.groupby('Mes de Abandono (Churn)').size()

        # Verifica si hay datos disponibles para calcular
        if clientes_abandono_por_mes.empty:
            raise ValueError("No hay datos disponibles para calcular el mes con mayor número de clientes que abandonaron.")

        # Encontrar el mes con la mayor cantidad de abandono de clientes
        mes_mas_abandono = clientes_abandono_por_mes.idxmax()  # Obtiene el índice (mes) con el máximo valor
        num_clientes_abandono = int(clientes_abandono_por_mes.max())  # Obtiene el valor máximo (número de clientes que abandonaron)

        result = {
            "Mes con mayor número de clientes que abandonaron": mes_mas_abandono,
            "Número de clientes que abandonaron en el mes": num_clientes_abandono
        }
    
    except KeyError as e:
        result = {"error": str(e)}

    except ValueError as e:
        result = {"error": str(e)}

    except Exception as e:
        result = {"error": f"Ocurrió un error inesperado al procesar la solicitud: {str(e)}"}

    return result



def Mes_Mayor_Porcentaje_Retencion(mes: str):
    try:
        # Verifica si la columna 'Mes Registro' y 'Mes de Abandono (Churn)' existen en el DataFrame
        if 'Mes Registro' not in data.columns or 'Mes de Abandono (Churn)' not in data.columns:
            raise KeyError("Las columnas 'Mes Registro' y 'Mes de Abandono (Churn)' son necesarias para calcular el porcentaje de retención.")

        # Verifica si el mes especificado es válido
        if mes not in data['Mes Registro'].unique():
            raise ValueError(f"El mes '{mes}' no es válido. Asegúrate de ingresar un mes existente.")

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

        result = {
            "Mes": mes,
            "Porcentaje de retención para el mes dado": porcentaje_retencion_mes
        }
    
    except KeyError as e:
        result = {"error": str(e)}

    except ValueError as e:
        result = {"error": str(e)}

    except Exception as e:
        result = {"error": f"Ocurrió un error inesperado al procesar la solicitud: {str(e)}"}

    return result


def Mes_Mayor_Porcentaje_Abandono(mes:str):
    try:
        # Verifica si la columna 'Mes Registro' y 'Mes de Abandono (Churn)' existen en el DataFrame
        if 'Mes Registro' not in data.columns or 'Mes de Abandono (Churn)' not in data.columns:
            raise KeyError("Las columnas 'Mes Registro' y 'Mes de Abandono (Churn)' son necesarias para calcular el porcentaje de abandono.")

        # Verifica si el mes especificado es válido
        if mes not in data['Mes Registro'].unique():
            raise ValueError(f"El mes '{mes}' no es válido. Asegúrate de ingresar un mes existente.")

        # Calcular el porcentaje de retención para el mes dado
        resultado_retencion = Mes_Mayor_Porcentaje_Retencion(mes)
        porcentaje_retencion_mes = resultado_retencion["Porcentaje de retención para el mes dado"]

        # Calcular el porcentaje de abandono como el inverso del porcentaje de retención
        # Aplicando las bases estadísticas de Q=1-P
        porcentaje_abandono_mes = (1 - (porcentaje_retencion_mes / 100)) * 100

        result = {
            "Mes": mes,
            "Porcentaje de abandono para el mes dado": porcentaje_abandono_mes
        }
    
    except KeyError as e:
        result = {"error": str(e)}

    except ValueError as e:
        result = {"error": str(e)}

    except Exception as e:
        result = {"error": f"Ocurrió un error inesperado al procesar la solicitud: {str(e)}"}

    return result



def Mes_Mayor_Porcentaje_Retencion_Total(data):
    try:
        # Verifica si las columnas 'Mes Registro' y 'Mes de Abandono (Churn)' existen en el DataFrame
        if 'Mes Registro' not in data.columns or 'Mes de Abandono (Churn)' not in data.columns:
            raise KeyError("Las columnas 'Mes Registro' y 'Mes de Abandono (Churn)' son necesarias para calcular el porcentaje de retención total.")

        # Verifica si hay datos disponibles para calcular
        if data.empty:
            raise ValueError("No hay datos disponibles para calcular el porcentaje de retención total.")

        # Diccionario para almacenar los porcentajes de retención para cada mes
        porcentajes_retencion = {}

        # Iterar sobre todos los meses en los datos
        for mes in data['Mes Registro'].unique():
            # Calcular el porcentaje de retención para el mes dado
            resultado_mes = Mes_Mayor_Porcentaje_Retencion(mes)
            
            # Almacenar el porcentaje de retención para este mes en el diccionario
            porcentajes_retencion[mes] = resultado_mes["Porcentaje de retención para el mes dado"]

        # Encontrar el mes con el mayor porcentaje de retención
        mes_mayor_retencion = int(max(porcentajes_retencion, key=porcentajes_retencion.get))
        mayor_porcentaje_retencion = porcentajes_retencion[mes_mayor_retencion]

        result = {
            "Mes con mayor porcentaje de retención": mes_mayor_retencion,
            "Mayor porcentaje de retención": mayor_porcentaje_retencion
        }
    
    except KeyError as e:
        result = {"error": str(e)}

    except ValueError as e:
        result = {"error": str(e)}

    except Exception as e:
        result = {"error": f"Ocurrió un error inesperado al procesar la solicitud: {str(e)}"}

    return result



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