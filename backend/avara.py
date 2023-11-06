
import numpy as np

class Nodo:
    def __init__(self, matriz, estado_agente, recorrido, nodos_visitados, profundidad, costo, heuristica):
        self.matriz = matriz
        self.estado_agente = estado_agente
        self.recorrido = recorrido
        self.nodos_visitados = nodos_visitados
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica

    # verifica si se han apagado los fuegos
    def esMeta(self):
        return len(self.estado_agente[1]) == 0

    # calcula la distancia de Manhattan entre dos puntos en un plano cartesiano (heurística de Avara)
    def distancia_manhattan(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    # encuentra una estimación de la distancia restante desde el estado actual del agente hasta el objetivo del problema
    def definir_heuristica(self):
        #si ya no hay fuegos
        if len(self.estado_agente[1]) == 0:
            return 0
        
        #si hay dos fuegos, encontrar la distancia entre sí
        if(len(self.estado_agente[1]) == 2): 
            pos_fuego1 = self.estado_agente[1][0]
            pos_fuego2 = self.estado_agente[1][1]
            dis_entre_fuegos = self.distancia_manhattan(pos_fuego1[0], pos_fuego1[1], pos_fuego2[0], pos_fuego2[1])
            
            dis_agt_fuegos = []
            for fuego in self.estado_agente[1]:
                dis_agt_fuegos.append(self.distancia_manhattan(self.estado_agente[0][0], self.estado_agente[0][1], fuego[0], fuego[1]))
            dis_apagar_fuego = min(dis_agt_fuegos[0], dis_agt_fuegos[1])

        else:
            dis_entre_fuegos = 0
            pos_ultimo_fuego = self.estado_agente[1][0]
            dis_apagar_fuego = self.distancia_manhattan(self.estado_agente[0][0], self.estado_agente[0][1], pos_ultimo_fuego[0], pos_ultimo_fuego[1])

        #distancia desde el agente a cada una de las cubetas, elegir mas cercana
        if(self.estado_agente[4] == "sin cubeta"):
            dis_a_cubetas = []
            for cubeta in self.estado_agente[2]:
                dis_a_cubetas.append(self.distancia_manhattan(self.estado_agente[0][0], self.estado_agente[0][1], cubeta[0], cubeta[1]))
            dis_tomar_cub = min(dis_a_cubetas[0], dis_a_cubetas[1])
        else:
            dis_tomar_cub = 0

        #distancia cuando no tiene agua
        if(self.estado_agente[5] == 0):
            dis_a_hid = self.distancia_manhattan(self.estado_agente[0][0], self.estado_agente[0][1], self.estado_agente[3][0], self.estado_agente[3][1])
        else:
            dis_a_hid = 0
        
        self.heuristica = dis_tomar_cub + dis_a_hid + dis_apagar_fuego + dis_entre_fuegos
        return self.heuristica
        

# Función para verificar movimientos y generar hijos
def estudiar_movimientos(xi, yi, copiaEstadoAgente, copiaMatriz, matriz, heuristica):
    estado_agente = copiaEstadoAgente
    nueva_matriz = copiaMatriz
    nuevo_estado = []

    #encuentra un fuego y lleva agua
    if(matriz[yi, xi] == 2 and estado_agente[5] > 0):
        estado_agente[1].remove((xi, yi))
        estado_agente[5] -= 1
        nueva_matriz[yi, xi] = 0

    #encuentra una cubeta de 1l y no lleva cubeta
    if(matriz[yi, xi] == 3 and estado_agente[4] == "sin cubeta"): 
        estado_agente[4] = "1l" 
        nueva_matriz[yi, xi] = 0
        print("tengo cubeta 1l")
    
    #encuentra una cubeta a 2 lts y no lleva cubeta
    if(matriz[yi, xi] == 4 and estado_agente[4] == "sin cubeta"): 
        estado_agente[4] = "2l" 
        nueva_matriz[yi, xi] = 0
        print("tengo cubeta 2l")

    #encuentra un hidratante y lleva cubeta de 1 lt
    if(matriz[yi, xi] == 6 and estado_agente[4] == "1l"):
        estado_agente[5] = 1

    #encuentra un hidratante y lleva cubeta de 2 lts
    if(matriz[yi, xi] == 6 and estado_agente[4] == "2l"):
        estado_agente[5] = 2     

    estado_agente[0] = ((xi, yi))
    nuevo_estado = nueva_matriz, estado_agente, heuristica
    return nuevo_estado


# Algoritmo de búsqueda avara
def avara(matriz_mundo):
    nodos_creados = 0
    nodos_expandidos = 0

    puntos_de_fuego = []
    pos_cubetas = []
    for i in range(matriz_mundo.shape[0]):
        for j in range(matriz_mundo.shape[1]):
            if matriz_mundo[i][j] == 2:  # posición de los puntos de fuego
                puntos_de_fuego.append((j, i))
            if matriz_mundo[i][j] == 3: #cubeta de 1l
                pos_cubetas.append((j, i, "1l"))
            if matriz_mundo[i][j] == 4: #cubeta de 2l
                pos_cubetas.append((j, i, "2l"))
            if matriz_mundo[i][j] == 6: #hidratante
                pos_hidratante = (j, i)
            if matriz_mundo[i][j] == 5: #posición agente
                pos_agente = (j, i)
                matriz_mundo[i][j] = 0

    '''ESTADO'''
    estado_agente = [pos_agente, puntos_de_fuego, pos_cubetas, pos_hidratante, "sin cubeta", 0] #0 lts de agua
    print(estado_agente)
    raiz = Nodo(matriz_mundo, estado_agente, [pos_agente], [[pos_agente]], 0, 0, 0)
    cola = [raiz]
    nodos_visitados = []
    
    while len(cola) > 0:
        nodo = min(cola, key=lambda x: x.heuristica)
        cola.remove(nodo)
        nodos_visitados.append(nodo.estado_agente)
        nodos_expandidos += 1

        #print(nodo.matriz)
    
        if nodo.esMeta():
            solucion = nodo.recorrido, nodos_expandidos, nodo.profundidad, matriz_mundo, nodo.estado_agente
            return solucion  

        x = nodo.estado_agente[0][0]
        y = nodo.estado_agente[0][1]
        
        # Generar hijos
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
        for movimiento in movimientos:
            xi = x + movimiento[0]
            yi = y + movimiento[1]

            if 0 <= xi < matriz_mundo.shape[1] and 0 <= yi < matriz_mundo.shape[0] and matriz_mundo[yi][xi] != 1:
                movimientos_resultantes = estudiar_movimientos(xi, yi, nodo.estado_agente.copy(), nodo.matriz.copy(), nodo.matriz, nodo.definir_heuristica())
                hijo = Nodo(
                    movimientos_resultantes[0], #nueva_matriz
                    movimientos_resultantes[1], #estado_agente
                    nodo.recorrido.copy(),
                    nodos_visitados,
                    nodo.profundidad + 1,
                    nodo.costo + 1,
                    movimientos_resultantes[2] #heuristica
                )
                nodos_creados += 1
                if movimientos_resultantes[1] not in nodos_visitados:
                    cola.append(hijo)
                    hijo.recorrido.append((xi, yi))                 
                    
    return "No hay solución", nodos_creados, nodos_expandidos, nodo.profundidad


def busqueda_informada_avara(matriz):
    matriznp = np.array(matriz)
        
    solucion, nodos_expandidos, profundidad, matriz_fin, estado_fin = avara(matriznp)

    lista_matrices_camino = []
    matrix = matriz_fin.copy()
    for step in solucion:
        x, y = step
        if matriz_fin[y][x] == 4 and "2l" == estado_fin[4]:
            print("entro aqui")
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 0
        elif matriz_fin[y][x] == 3 and "1l" == estado_fin[4]:
            print("entro aca")
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 0
        elif matriz_fin[y][x] == 6:
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 6
        elif matriz_fin[y][x] == 3 and estado_fin[4] != "1l":
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 3
        elif matriz_fin[y][x] == 4 and estado_fin[4] != "2l":
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 4       
        else:
            matrix[y][x] = 5
            lista_matrices_camino.append(matrix.copy())
            matrix[y][x] = 0

    matrices_camino = [matriz.tolist() for matriz in lista_matrices_camino]
    return matrices_camino, nodos_expandidos, profundidad
