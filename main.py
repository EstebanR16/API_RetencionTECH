from fastapi import FastAPI
from API_Retencion import Clientes_por_Mes, Mes_mayorClientes, Mes_mayor_abandono, Porcentaje_Retencion_Abandono

app_retencion = FastAPI()

@app_retencion.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Recomendaciones!"}

@app_retencion.get("/clientes-mes/{mes}")
def obtener_clientes_por_mes(mes: str):
    result = Clientes_por_Mes(mes)
    return {"result": result}


'''@app_retencion.get("/user-for-genre/{genero}")
def read_user_for_genre(genero: str):
    result = UserForGenre(genero)
    return {"result": result}

@app_retencion.get("/users-recommend/{año}")
def read_users_recommend(año: int):
    result = UsersRecommend(año)
    return {"result": result}

@app_retencion.get("/users-worst-developer/{año}")
def read_users_worst_developer(año: int):
    result = UsersWorstDeveloper(año)
    return {"result": result}'''
