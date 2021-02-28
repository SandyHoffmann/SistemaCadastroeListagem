n1=0
n2=0
lista1=[1,2,6]
lista2=[1,1,5]
divisao=lista1[0]/lista2[0]
lista1multiplicada = []
lista2diminuida=[]
for x in lista1:
    lista1multiplicada.append(x*divisao)
for i in lista2:
    lista2diminuida.append(i-lista1multiplicada[n1])
    n1+=1
divisao=lista1[1]/lista2diminuida[1]
lista2multiplicada = []
lista1diminuida=[]
for x in lista2diminuida:
    lista2multiplicada.append(x*divisao)
for i in lista1:
    lista1diminuida.append(i-lista2multiplicada[n2])
    n2+=1
a=lista1diminuida[0]
b=lista2diminuida[1]

listafinal1=[]
listafinal2=[]

for y in lista1diminuida:
    listafinal1.append(y/a)
for z in lista2diminuida:
    listafinal2.append(z/b)
                
quantidade1 = listafinal1[2]    
quantidade2 = listafinal2[2]    

print(quantidade1)
print(quantidade2)