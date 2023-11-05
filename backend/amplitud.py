


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
    
    # param: Int, Boolean, Boolean, Boolean ->  Int
    # Verifica si a posicion no pasa por un  fuego sin agua
    def verificar_fuego(self, x,y):
        if self.matriz[x][y] == 2 and  self.hidrante == False:
            return False
        else:
            return True

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

                
                #elif self.nodo_padre.matriz[self.posicion[0]][self.posicion[1]] == 2 and  self.hidrante==True:
                 #  nueva_matriz[self.posicion[0]][self.posicion[1]] = 0

                #elif self.nodo_padre.matriz[self.posicion[0]][self.posicion[1]] == 2 and  self.hidrante==False:
                 #  nueva_matriz[self.posicion[0]][self.posicion[1]] = 2
            
                elif self.matriz[x][y] == 2 and self.cubeta1 and self.hidrante==True:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                    hidrante = False

                elif self.nodo_padre.matriz[self.posicion[0]][self.posicion[1]] == 6:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 6

                else:
                    nueva_matriz[self.posicion[0]][self.posicion[1]] = 0
                
        
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
                    hidrante,
                )
                movimientos.append(nuevo_nodo)

        return movimientos
    



# Devuelve la posicion del agente
def find_agent(matriz):
    for row in range(len(matriz)):
        for column in range(len(matriz)):
            if matriz[row][column] == 5:
                return [row,column]





def busqueda_preferente_por_amplitud(matriz):

    x =1
    initial_position = find_agent(matriz)

    queue = []
    queue.append(Nodo(matriz, initial_position, None))
    #print_matriz(queue[0].matriz)

    while True:
        #print("=======================")
        #print("cola antes de expansion")
        #print_movimientos(queue)

        if not queue:
            return "no, te falla", 
        
        current_node = queue.pop(0)
        #print("nodo a expandir")
        #print_matriz(current_node.matriz)

        if current_node.esMeta():
            return ["no te falla", current_node]
        
        children = current_node.expandir()

        for child in children:
            queue.append(child)

        #print("cola despues de expansion")
        #print_movimientos(queue)
        #print("=======================")

        #aplanar lista
        #queue = aplanar_lista(queue)
        x= x+1

    return "no hay meta -- se pierde en bucles entonces nunca accede ea esto"


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


"""
result = busqueda_preferente_por_amplitud(matriz2)
print(result)

path = imprimir_camino(result)

for matriz in yeison:
    print_matriz(matriz)
    print("--")






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