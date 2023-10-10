class Nodo:

    #constructor
    def __init__(self, matriz, posicion, nodo_padre = None):
        self.matriz = matriz
        self.posicion = posicion
        self.nodo_padre = nodo_padre
        self.profundidad = 0
        self.fuego_restante  = 2


    #verifica si apago todas las llamas
    def esMeta(self):
        return self.fuego_restante == 0
    
    
    #verifica si el movimiento que le entregan es igual a la del padre)
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

            # Verificar si el movimiento es válido dentro de la matriz
            if self.verificar_limites(x,y) and self.matriz[x][y] != 1 and self.verificar_padre([x,y]):
               
                # Copia la matriz a una nueva
                nueva_matriz = [fila[:] for fila in self.matriz]  
                # Borrar la posición actual
                nueva_matriz[self.posicion[0]][self.posicion[1]] = 0 
                # Mover al personaje a la nueva posición
                nueva_matriz[x][y] = 5  

                # Crea y guarda el nodo hijo en un array
                nuevo_nodo = Nodo(nueva_matriz, [x, y], self)
                movimientos.append(nuevo_nodo)

        return movimientos
    

# Imprime matriz
def print_matriz(matriz):
    for fila in matriz:
            print(fila)
        

    
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



def busqueda_preferente_por_amplitud(matriz):

    x =1
    initial_position = find_agent(matriz)
    goals = find_goals(matriz)

    queue = []
    queue.append(Nodo(matriz, initial_position, None))

    while (x != 50):

        if not queue:
            return "no, te falla"
        
        current_node = queue.pop(0)

        if current_node.esMeta():
            return "no te falla"    
        
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


def aplanar_lista(arr):
    resultado = []
    for elemento in arr:
        if isinstance(elemento, list):
            resultado.extend(aplanar_lista(elemento))
        else:
            resultado.append(elemento)
    return resultado



hola = busqueda_preferente_por_amplitud(matriz)
print(hola)





print_movimientos(hola)








