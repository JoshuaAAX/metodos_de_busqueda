class Nodo:

    #constructor
    def __init__(self, matriz, posicion, nodo_padre = None, fuego_restante = 2, cubeta1 = False, cubeta2 = False, hidrante = False):
        self.matriz = matriz
        self.posicion = posicion
        self.nodo_padre = nodo_padre
        self.fuego_restante  = fuego_restante
        self.cubeta1 = cubeta1
        self.cubeta2 = cubeta2
        self.hidrante = hidrante
        self.profundidad = 0 if nodo_padre is None else nodo_padre.profundidad + 1


    #verifica si apago todas las llamas
    def esMeta(self):
        return self.fuego_restante == 0
    
    
    #acciones en caso de pasar por la cubet de 1 litro
    def paso_cubeta1(self, x, y):
        if self.cubeta2 == False and self.matriz[x][y] == 3:
            return True
        else:
            return self.cubeta1

    
    #acciones en caso de pasar por la cubetde 2 litros
    def paso_cubeta2(self, x, y):
        if self.cubeta1 == False and self.matriz[x][y] == 4:
            return True
        else:
            return self.cubeta2


    #acciones en caso de pasar por un hidrante
    def paso_hidrante(self, x, y):
        if (self.cubeta1 or self.cubeta2 )and self.matriz[x][y] == 6:
            return True
        else:
            return self.hidrante

    #acciones en caso de pasar por fuego
    def paso_fuego(self, x, y):
        if self.hidrante==True and self.matriz[x][y] == 2:
            return self.fuego_restante - 1
        else:
            return self.fuego_restante

 
    #verifica si el movimiento que le entregan es igual a la del padre
    def verificar_padre(self, posicion):
        if self.nodo_padre:
            return  not posicion == self.nodo_padre.posicion
        
        return True
    
    #si la posicion va deacuerdo a los limites de la matriz
    def verificar_limites(self, x, y):
        return 0 <= x < len(self.matriz) and 0 <= y < len(self.matriz[0]) 
    

    def expandir(self):
        movimientos = []

        # Posibles movimientos: izquierda, derecha, arriba, abajo,
        movimientos_posibles = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in movimientos_posibles:

            x, y = self.posicion[0] + dx, self.posicion[1] + dy

            # Verificar si el movimiento es válido dentro de la matriz  (este en los limites, no sea pared y no sea igual al padre)
            if self.verificar_limites(x,y) and self.matriz[x][y] != 1 and self.verificar_padre([x,y]):
               
                # Copia la matriz a una nueva
                nueva_matriz = [fila[:] for fila in self.matriz] 



                if self.nodo_padre is None:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                else:
                   if self.nodo_padre.matriz[self.posicion[0]][self.posicion[1]] ==2 and not self.hidrante:
                       nueva_matriz[self.posicion[0]][self.posicion[1]] = 2
                   else:
                       nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                
                # Borrar la posición actual
                



                # Mover al personaje a la nueva posición
                nueva_matriz[x][y] = 5  

                # Crea y guarda el nodo hijo en un array
                nuevo_nodo = Nodo(
                    nueva_matriz, 
                    [x, y], 
                    self, 
                    self.paso_fuego(x,y),
                    self.paso_cubeta1(x,y),
                    self.paso_cubeta2(x,y),
                    self.paso_hidrante(x,y),
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


# Encuentra las posiciones del fuego
def find_goals(matriz):
    
    goals=[]

    for row in  range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column]==2:
                goals.append([row, column])
    return goals


def aplanar_lista(arr):
    resultado = []
    for elemento in arr:
        if isinstance(elemento, list):
            resultado.extend(aplanar_lista(elemento))
        else:
            resultado.append(elemento)
    return resultado



def busqueda_preferente_por_amplitud(matriz):

    x =1
    initial_position = find_agent(matriz)
    goals = find_goals(matriz)

    queue = []
    queue.append(Nodo(matriz, initial_position, None))

    while True:

        if not queue:
            return "no, te falla", 
        
        current_node = queue.pop(0)

        if current_node.esMeta():
            return ["no te falla", current_node]
        
        children = current_node.expandir()
        queue.append(children)

        #aplanar lista
        queue = aplanar_lista(queue)
        x= x+1

    return  queue


# Ejemplo de uso:
matriz = [
[2, 0, 0, 1, 0],
[0, 1, 0, 0, 0],
[0, 0, 2, 0, 0],
[0, 1, 1, 0, 0],
[0, 0, 5, 0, 0]
]

matriz1 = [
[2, 0, 0, 1, 0],
[0, 1, 0, 0, 0],
[0, 0, 2, 0, 2],
[0, 1, 1, 0, 2],
[0, 0, 5, 3, 6]
]

matriz2 = [
[2, 0, 0, 1, 0],
[0, 1, 6, 0, 0],
[0, 0, 0, 0, 0],
[0, 1, 1, 0, 0],
[0, 0, 5, 2, 3]
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



hola = busqueda_preferente_por_amplitud(matriz2)
print(hola)

yeison = imprimir_camino(hola)

for matriz in yeison:
    print_matriz(matriz)
    print("--")


"""

nodoinicial =Nodo(matriz2, find_agent(matriz2))
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

