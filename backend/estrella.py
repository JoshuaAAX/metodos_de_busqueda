class Nodo:

    #constructor
    def __init__(self, 
                 matriz, 
                 posicion, 
                 posicion_cubetas, 
                 posicion_hidrante, 
                 posicion_fuegos, 
                 nodo_padre = None, 
                 fuego_restante = 2, 
                 cubeta1 = False, 
                 cubeta2 = False, 
                 hidrante = False, 
                 costo=0, 
                 costo_total =1007):
        
        self.matriz = matriz
        self.posicion = posicion
        self.posicion_cubetas = posicion_cubetas
        self.posicion_hidrante = posicion_hidrante
        self.posicion_fuegos = posicion_fuegos
        self.nodo_padre = nodo_padre
        self.fuego_restante  = fuego_restante
        self.cubeta1 = cubeta1
        self.cubeta2 = cubeta2
        self.hidrante = hidrante
        self.profundidad = 0 if nodo_padre is None else nodo_padre.profundidad + 1
        self.costo = costo
        self.costo_total = costo_total

    # param: object -> Boolean
    # Verifica si apago todas las llamas
    def esMeta(self):
        return self.fuego_restante == 0
    
    # param: Int, Int -> Boolean
    # Acciones en caso de pasar por la cubeta de 1 litro
    def paso_cubeta1(self, x, y):
        if self.cubeta2 == False and self.matriz[x][y] == 3:
            return True
        else:
            return self.cubeta1

    # param: Int, Int -> Boolean
    # Acciones en caso de pasar por la cubeta de 2 litros
    def paso_cubeta2(self, x, y):
        if self.cubeta1 == False and self.matriz[x][y] == 4:
            return True
        else:
            return self.cubeta2

    # param: Int, Int -> Boolean
    # Acciones en caso de pasar por un hidrante
    def paso_hidrante(self, x, y):
        if (self.cubeta1 or self.cubeta2) and self.matriz[x][y] == 6:
            return True
        else:
            return self.hidrante
        
    # param: Int, Int -> Int
    # Acciones en caso de pasar por fuego
    def paso_fuego(self, x, y):
        if self.hidrante==True and self.matriz[x][y] == 2:
            return self.fuego_restante - 1
        else:
            return self.fuego_restante

    # param: List<Int> -> Boolean
    # Verifica si als propiedades del nodo actual son diferentes al de nodo padre
    def verificar_padre(self, posicion):
        if self.nodo_padre:

            return   (posicion != self.nodo_padre.posicion 
                     or  self.nodo_padre.fuego_restante != self.fuego_restante 
                     or self.hidrante != self.nodo_padre.hidrante 
                     or self.cubeta1 != self.nodo_padre.cubeta1 
                     or self.cubeta2 != self.nodo_padre.cubeta2)
        
        return True
    
    # param: Int, Int -> Boolean
    # Verifica si la posicion va de acuerdo a los limites de la matriz
    def verificar_limites(self, x, y):
        return 0 <= x < len(self.matriz) and 0 <= y < len(self.matriz[0]) 
    
    # param: Int, Int -> Boolean
    # Verifica si a posicion no pasa por un  fuego sin agua
    def verificar_fuego(self, x,y):
        if self.matriz[x][y] == 2 and  self.hidrante == False:
            return False
        else:
            return True

    # param: Int, Boolean, Boolean, Boolean ->  Int
    # Calcula ell costo de acuerdo a las reglas del juego
    def calculo_costo(self, costo, cubeta1, cubeta2, hidrante, fuego_restante):
        if (cubeta1 and hidrante) or (cubeta2 and hidrante and fuego_restante==1):
            return costo + 2
        if cubeta2 and hidrante:
            return costo + 3
        else:
            return costo + 1
        
        
    # calcula la distancia de Manhattan entre dos puntos en un plano cartesiano (heurística de Avara)
    def distancia_manhattan(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    
    def caculo_heuristica(self, cubeta1, cubeta2, hidrante, fuego_restante, x,y, matriz):
          
        #si ya no hay fuegos
        if fuego_restante == 0:    
            return 0
        
        #si hay dos fuegos, encontrar la distancia entre sí
        if fuego_restante == 2:
            pos_fuego1 = self.posicion_fuegos[0]
            pos_fuego2 = self.posicion_fuegos[1]
            dis_entre_fuegos = self.distancia_manhattan(pos_fuego1[0], pos_fuego1[1], pos_fuego2[0], pos_fuego2[1])

            dis_agt_fuegos = []
            for fuego in self.posicion_fuegos:
                 dis_agt_fuegos.append(self.distancia_manhattan(x, y, fuego[0], fuego[1]))
            dis_apagar_fuego = min(dis_agt_fuegos[0], dis_agt_fuegos[1])
        else:
            dis_entre_fuegos = 0
            goals=[]

            for row in  range(len(self.matriz)):
              for column in range(len(self.matriz)):
                if self.matriz[row][column]==2:
                  goals.append([row, column])
              
 
            pos_ultimo_fuego = goals[0]
            dis_apagar_fuego = self.distancia_manhattan(x, y, pos_ultimo_fuego[0], pos_ultimo_fuego[1])

        #distancia desde el agente a cada una de las cubetas, elegir mas cercana
        if not cubeta1 or not cubeta2:

            dis_a_cubetas = []
            for cubeta  in self.posicion_cubetas:
                dis_a_cubetas.append(self.distancia_manhattan(x,y, cubeta[0], cubeta[1]))
            dis_tomar_cub = min(dis_a_cubetas[0], dis_a_cubetas[1])

        else: 
            dis_tomar_cub = 0



        #distancia cuando no tiene agua
        if not hidrante:
            dis_a_hid = self.distancia_manhattan(x,y, self.posicion_hidrante[0], self.posicion_hidrante[1])
        else:
            dis_a_hid = 0
        
        return dis_tomar_cub + dis_a_hid + dis_apagar_fuego + dis_entre_fuegos


    # calcula la suma entre el costo y la heuristica
    def calculo_total(self, costo, cubeta1, cubeta2, hidrante, fuego_restante,  x ,y, matriz):
         suma = costo + self.caculo_heuristica(cubeta1, cubeta2, hidrante, fuego_restante, x, y, matriz)
         return suma



    # param: self.Object ->  List<Object>
    # Retorna los  nodos con los posibles Movimientos
    def expandir(self):
        
        movimientos = []

        # Posibles movimientos: izquierda, derecha, arriba, abajo,
        movimientos_posibles = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in movimientos_posibles:

            x, y = self.posicion[0] + dx, self.posicion[1] + dy

          

            # Verificar si el movimiento es válido dentro de la matriz (este en los limites, no sea pared y no sea igual al padre)
            if self.verificar_limites(x,y) and self.matriz[x][y] != 1 and self.verificar_padre([x,y]) and self.verificar_fuego(x,y):

               
                
                # variable global de hidrante - mala practica  corregir
                hidrante = self.paso_hidrante(x,y)

                # Copia la matriz a una nueva
                nueva_matriz = [fila[:] for fila in self.matriz] 


                # Borra la posicion del personaje asignar el valor que corresponda a esa casiila
                if self.nodo_padre is None:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0

            
                elif self.matriz[x][y] == 2 and self.cubeta1 and self.hidrante==True:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                    hidrante = False

                elif self.nodo_padre.matriz[self.posicion[0]][self.posicion[1]] == 6:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 6

                else:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                
        
                # Mover al personaje a la nueva posición
                nueva_matriz[x][y] = 5  
                 

                # Aplica el calculo del costo y costo total a la nueva matriz
                costo_nodo = self.calculo_costo(self.costo, self.paso_cubeta1, self.paso_cubeta2, hidrante, self.paso_fuego(x,y))
                costo_total = self.calculo_total(costo_nodo, self.paso_cubeta1, self.paso_cubeta2, hidrante, self.paso_fuego(x,y), x,y, nueva_matriz)

                # Crea y guarda el nodo hijo en un array
                nuevo_nodo = Nodo(
                    nueva_matriz, 
                    [x, y], 
                    self.posicion_cubetas,
                    self.posicion_hidrante,
                    self.posicion_fuegos,
                    self, 
                    self.paso_fuego(x,y),
                    self.paso_cubeta1(x,y),
                    self.paso_cubeta2(x,y),
                    hidrante,
                    costo_nodo,
                    costo_total
                )

                movimientos.append(nuevo_nodo)

        return movimientos
    

# Imprime matriz
def print_matriz(matriz):
    for fila in matriz:
            print(fila)
        

# Imprime los posibles movimientos  
def print_movimientos(movimientos_posibles):
    for movimiento in movimientos_posibles:
        for fila in movimiento.matriz:
            print(fila)
        print("")



# Devuelve la posicion del agente
def find_agent(matriz):
    for row in range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column] == 5:
                return [row,column]
            

# Devuelve la posicion del hidrante
def find_hidrante(matriz):
    for row in range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column] == 6:
                return [row,column]
            

# Devuelve la posicion de las cubetas
def find_cubetas(matriz):
    cubetas = []

    for row in range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column] == 3:
                cubetas.append([row, column])

    for row in range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column] == 4:
                cubetas.append([row, column])


# Devuelve la posicion de los fuegos
def find_goals(matriz):
    
    goals=[]

    for row in  range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column]==2:
                goals.append([row, column])
    return goals




def busqueda_a_estrella(matriz):

    initial_position = find_agent(matriz)
    posicion_cubetas = find_cubetas(matriz)
    posicion_hidrante = find_hidrante(matriz)
    posicion_fuegos = find_goals(matriz)
    count_nodes = 0

    queue = []
    queue.append(Nodo(matriz, initial_position, posicion_cubetas, posicion_hidrante, posicion_fuegos, None))
    #print_matriz(queue[0].matriz)

    while True:
        #print("=======================")
        #print("cola antes de expansion")
        #print_movimientos(queue)

        if not queue:
            return "no, te falla", 
        
        current_node =  min(queue, key=lambda x: x.costo_total)
        queue.remove(current_node)
        #print("nodo a expandir")
        #print_matriz(current_node.matriz)

        if current_node.esMeta():
            return ["no te falla", current_node, count_nodes]
        
        children = current_node.expandir()
        count_nodes += 1

        for child in children:
            queue.append(child)


        #print("cola despues de expansion")
        #print_movimientos(queue)
        #print("=======================")

        #aplanar lista
        #queue = aplanar_lista(queue)

    return "no hay meta"


# Ejemplo de uso:

matriz0 = [
[5, 3, 6, 2, 2],
]

matriz = [
[3, 0, 5],
[0, 1, 6],
[0, 2, 2]
]

matriz1 = [
[2, 0, 0, 1, 0],
[0, 1, 0, 0, 0],
[0, 0, 2, 0, 2],
[0, 1, 1, 0, 2],
[0, 0, 5, 3, 6]
]

matriz2 = [
[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
[0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
[0, 1, 0, 2, 0, 0, 0, 0, 0, 1],
[0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
[5, 0, 0, 6, 0, 0, 0, 1, 0, 1],
[0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
[3, 0, 0, 0, 2, 0, 0, 1, 0, 1],
[0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
[0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
]

def imprimir_camino(resultado):
    respuesta = resultado[0]
    nodo = resultado[1]
    if respuesta=="no te falla":
        camino = []
        
        while nodo:
            camino.append(nodo.matriz)
            nodo = nodo.nodo_padre
        camino.reverse()

        return camino
    else:
        print(respuesta)



"""
result = busqueda_a_estrella(matriz2)
print(result)

path = imprimir_camino(result)

for matriz in path:
    print_matriz(matriz)
    print("--")


initial_position = find_agent(matriz1)
queue = []
queue.append(Nodo(matriz1, initial_position, None))
queue.append(Nodo(matriz1, initial_position, None))

current_node =  min(queue, key=lambda x: x.costo)
queue.remove(current_node)

print_movimientos(queue)


nodoinicial =Nodo(matriz1, find_agent(matriz1))
movimientos_p =nodoinicial.expandir()
print_movimientos(movimientos_p)
print(movimientos_p[1].cubeta1)

g=movimientos_p[1].expandir()
print_movimientos(g)
print(g[1].cubeta1)
print(g[1].hidrante)



nodoinicial =Nodo(matriz1, find_agent(matriz1))
movimientos_p =nodoinicial.expandir()
print_movimientos(movimientos_p)
print(movimientos_p[1].cubeta1)


g=movimientos_p[1].expandir()
print_movimientos(g)
print(g[1].cubeta1)
print(g[1].hidrante)

h=g[0].expandir()
print_movimientos(h)
print(h[0].cubeta1)
print(h[0].hidrante)
print(h[0].fuego_restante)

i=h[0].expandir()
print_movimientos(i)
print(i[1].cubeta1)
print(i[1].hidrante)
print(i[1].fuego_restante)
print(i[1].esMeta())
print(i[1].profundidad)


"""