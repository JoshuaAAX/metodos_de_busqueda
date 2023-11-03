
file = "Prueba1.txt"

with open(file, "r") as archivo:
    lineas = archivo.readlines()

matriz = []

for linea in lineas:
    numeros = [int(numero) for numero in linea.strip().split()]
    matriz.append(numeros)

#print matriz
for fila in matriz:
    print(fila)
