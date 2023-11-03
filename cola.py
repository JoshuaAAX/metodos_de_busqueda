'''
hola = ["d","f","g"]
print(hola)

hola.append("2")
print(hola)
fallo =hola.pop(0)
print(hola)
print(fallo)
'''

aba = [666]

def resolved(x):
    a=x=1
    b=x-1
    c=0
    d=1
    return a,b,c,d


print(resolved(2))

a,b,c,d=resolved(2)
aba.append(a)

print(aba)