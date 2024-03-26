from fastapi import FastAPI
from API_Retencion import (Clientes_por_Mes, Mes_mayorClientes, Mes_mayor_abandono, 
                           Mes_Mayor_Porcentaje_Retencion,
                           Mes_Mayor_Porcentaje_Abandono, Mes_Mayor_Porcentaje_Retencion_Total)

app_retencion = FastAPI()

@app_retencion.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Retención!"}

@app_retencion.get("/clientes-mes/{mes}")
def obtener_clientes_por_mes(mes: str):
    result = Clientes_por_Mes(mes)
    return {"result": result}

@app_retencion.get("/mes-mayor-clientes")
def obtener_mes_mayor_clientes():
    result = Mes_mayorClientes(data)
    return {"result": result}

@app_retencion.get("/mes-mayor-abandono")
def obtener_mes_mayor_abandono():
    result = Mes_mayor_abandono(data)
    return {"result": result}

@app_retencion.get("/porcentaje-retencion-mes/{mes}")
def obtener_porcentaje_retencion_mes(mes: str):
    result = Mes_Mayor_Porcentaje_Retencion(data, mes)
    return {"result": result}

@app_retencion.get("/porcentaje-retencion-total")
def obtener_porcentaje_retencion_total():
    result = Mes_Mayor_Porcentaje_Retencion_Total(data)
    return {"result": result}

@app_retencion.get("/porcentaje-abandono-mes/{mes}")
def obtener_porcentaje_abandono_mes(mes: str):
    result = Mes_Mayor_Porcentaje_Abandono(data, mes)
    return {"result": result}

