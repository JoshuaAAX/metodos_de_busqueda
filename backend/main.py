from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated

from datetime import datetime
import time


import amplitud 
import costo
import  profundidad
import avara

app = FastAPI()


# Configura CORS para permitir todas las solicitudes desde cualquier origen
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Convierte el archivo en una lista de listas
def read_matrix(content):
    matrix = []
    lines = content.decode("utf-8").splitlines()

    for line in lines:
        row = list(map(int, line.split()))
        matrix.append(row)
    
    return matrix

# Retorna el camino según el resultado de la busqueda
def find_path(result):
    response = result[0]
    node = result[1]

    if response=="no te falla":
        path = []
        
        while node:
            path.append(node.matriz)
            node = node.nodo_padre
        path.reverse()

        return path
   
    return response
    
# Retorna la profundida del nodo donde se encuentra la meta
def find_depth(result):
    response = result[0]
    node = result[1]

    if response=="no te falla":
        return node.profundidad
    
    return response


# Retorna la cantidad de nodos expandidos para hallar la meta
def find_nodes(result):
    response = result[0]
    node = result[1]
    count_node = result[2]

    if response=="no te falla":
        return count_node
    
    return response

# Retorna la cantidad de nodos expandidos para hallar la meta
def find_cost(result):
    response = result[0]
    node = result[1]
    count_node = result[2]

    if hasattr(node,"costo"):
        return str(node.costo)
    
    return "null"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile/{number}")
async def upload_file(number: int, file: UploadFile = File(...)):
    
    content = await file.read()
    matrix = read_matrix(content)
    result2 = None
    
    start_time = datetime.now()
     
    if number == 1:
        result = amplitud.busqueda_preferente_por_amplitud(matrix)
    elif number == 2:
        result = costo.busqueda_de_costo_uniforme(matrix)
    elif number == 3:
        result =  profundidad.busqueda_preferente_por_profundidad(matrix)
    elif number == 4:
        print("4444444444")
        result2 = avara.busqueda_informada_avara(matrix)

    end_time = datetime.now()
    time = end_time - start_time

    if result2 != None:
        arrays_response = [{"matrix": matrix} for matrix in result2[0]]
        nodes = result2[1]
        depth = result2[2]
        cost = None
    else:
        response = find_path(result)
        arrays_response = [{"matrix": matrix} for matrix in response]
        nodes = find_nodes(result)
        depth = find_depth(result)
        cost = find_cost(result)
   
    return {"filename": file.filename, "arrays": arrays_response, "nodes": nodes, "depth": depth, "time": time, "cost": cost}