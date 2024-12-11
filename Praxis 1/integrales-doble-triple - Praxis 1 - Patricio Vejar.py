import sympy as sp


def cambios(a,b):
    if(a>b):
        h = a
        a = b
        b = h
    return a,b

def integ2 (f,a1,b1,a2,b2): #integral doble en termino de cualquier variable, recive, funcion original, limites de integral
    u,v = f.free_symbols
    ec = sp.integrate(f,(u,a1,b1))
   # print(ec)
    ec = sp.integrate(ec,(v,a2,b2))
    #print(ec)
    return ec
def integ3 (f,a1,b1,a2,b2,a3,b3):#integral triple en termino de cualquier variable, recive, funcion original, limites de integral
    u, v, n = f.free_symbols
    ec = sp.integrate(f,(u,a1,b1))
   # print(ec)
    ec = sp.integrate(ec,(v,a2,b2))
   # print(ec)
    ec = sp.integrate(ec,(n,a3,b3))
    return ec

#f=z**2+x**2-2*y#constante de prueba
#l1,l2,l3,l4,l5,l6 = 0,1,0,1,0,1

print("Este programa soporta hasta 3 variable:")
print("----")
        
t=0
while(not t):
    try:#pedimos la funcion,en loop hasta conseguir entrada viable
        f = input("Por favor introdusca la funcion a integrar:")
        f = sp.sympify(f)
        if(not len(f.free_symbols) > 3):
            t=1
        else:
            print("Por favor introdusca una funcion de 3 variables")
    except:
        print("Error en la entrada de funcion por favor introdusca una entrada valida")
t=0

print("----")
print("")
if(len(f.free_symbols) == 3):#preguntamos por la cantidad de simbolos dentro de la funcion leida y ejecutamos la respectiva integral
    print("Por favor introdusca los limites por orden pedido")
    l1 = sp.sympify(input("Limite inferior de primera variable: "))#preguntamos por los limites respectivos en cada escenario para no tener que preguntar de mas en ciertos escenarios y no tener variables vacias
    l2 = sp.sympify(input("Limite superior de primera variable: "))
    if(l1.free_symbols == False and l2.free_symbols==True):#si los limites de cada integral no son en terminos de variables, revisamos que el sentido de estas este correcto 
        cambios(l1,l2)
    
    l3 = sp.sympify(input("Limite inferior de segunda variable: "))
    l4 = sp.sympify(input("Limite superior de segunda variable: "))
    if(l3.free_symbols == False and l4.free_symbols== True):
            cambios(l3,l4)
            
    l5 = sp.sympify(input("Limite inferior de tercera variable: "))
    l6 = sp.sympify(input("Limite superior de tercera variable: "))
    if(l5.free_symbols == False and l6.free_symbols==True):
        cambios(l5,l6)
        
    print("------")
    print("Volumen de la funcion con los datos dados: {}".format(integ3(f,l1,l2,l3,l4,l5,l6)))#con los datos dados imprimimos el resultado y fin
elif(len(f.free_symbols) ==2):
    print("Por favor introdusca los limites por orden pedido")
    l1 = sp.sympify(input("Limite inferior de primera variable: "))
    l2 = sp.sympify(input("Limite superior de primera variable: "))
    if(l1.free_symbols == False and l2.free_symbols==True):
        cambios(l1,l2)
        
    l3 = sp.sympify(input("Limite inferior de segunda variable: "))
    l4 = sp.sympify(input("Limite superior de segunda variable: "))
    if(l3.free_symbols == False and l4.free_symbols== True):
            cambios(l3,l4)
            
    print("------")
    print("Volumen de la funcion con los datos dados: {}".format(integ2(f,l1,l2,l3,l4)))
elif(len(f.free_symbols) == 1):
    print("Por favor introdusca los limites por orden pedido")
    l1 = sp.sympify(input("Limite inferior de primera variable: "))
    l2 = sp.sympify(input("Limite superior de primera variable: "))
    if(l1.free_symbols == False and l2.free_symbols==True):
        cambios(l1,l2)
        
    u= f.free_symbols
    print("------")
    print("Volumen de la funcion con los datos dados: {}".format(sp.integrate(f,(u,l1,l2))))
elif(len(f.free_symbols) == 0):#si la funcion dada es una constante se dice no se calcula nada
    print("Usted introdujo una constante, no una funcion")
else:#peor escenario:  puede causarlo un simbolo sin nada
    print("error em | len(f.free_symbols) | posible causa: entrada de funcion invalida: evite usar 'simbolos solitarios'")
    
    
print("Funcion leida: {}".format(f))
print("")
print("")
print("------------Fin programa")