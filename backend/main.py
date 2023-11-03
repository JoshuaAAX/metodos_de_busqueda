from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated


import breadthFirstSearch 

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

# Imprime el camino según el resultado de la busqueda
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
    else:
        return response
    


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    
    content = await file.read()
    matrix = read_matrix(content)


    result = breadthFirstSearch.busqueda_preferente_por_amplitud(matrix)

    response = find_path(result)

    arrays_response = [{"matrix": matrix} for matrix in response]

    
    return {"filename": file.filename, "arrays": arrays_response}





