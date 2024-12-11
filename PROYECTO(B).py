import matplotlib.pyplot as plt
import sympy as sp
    
#---------------------Calculo de dominio------------------------------#
    
def DOM(f,n): # n es una lista con los valores del dominio, f es la funcion a evaluar
    
    nan = [] # lista para guardar los valores en la que la funcion de resutado No Numerico. O en otras palabras numeros complejos
    
    for valor in n: #para vada valor dentro del dominio dado en el doc
        resultado =  f.subs(x,valor)
        if not resultado.is_real: # si el resultado de la funcion segun el valor no da un numero Real has:
            nan.append(valor)#añade ese valor a la lista de nan
    for valor in nan:#toma el valor que este en la lista de nan y lo elimina de la lista N
        n.remove(valor)
    print('x pertenece a lor reales; expeto por los valores : ',nan)
    return n #devuelve la lista N cambiada

#----------------------------------------------------------------------#    
    
    
    
    
#------------------------------INTEGRALES DEFINIDAS----------------------#
def intg(f,g,top,bot):
    if g == None:
            #por funcion de sympy
        integ = sp.integrate(f,(x,bot,top)) # integrate(funcion(variable), varialbe, limte inf, limite top) ## funciona!
         
            #a mano

        #use las ecuaciones:
        # 	integral f(x) dx = (x**n+1)/(n+1) 		
        # x * f(x) = x**n+1		
        # lim x -> infinito (log(x**n)) / (log(x)) = n.  
        
       # n = (sp.degree(f,x)) #Encuentra el valor mas alto al que X este elevado dentro de la funcion
       # nplus = n+1
        
        #metodo = desarmar a una equacion compresible para la maquina ; remplasar el limite inf y top y restarlo. Consigue la integra. O el la idea
               

       # idx = x**nplus / nplus #  (x**n+1)/(n+1) 		ID1

    #no funciono :x
        #no tengo idea porque no me funcionaba lo de arriba pero usando la funcion de intrgrar puedo armar la integral en x. 
        idx = sp.integrate(f,x)
       

        idxE = idx.subs(x,top) - idx.subs(x,bot) #remplasa x por lo valores de top y bot. Para restarlos y terminar con el valor final
        
        #print(idx)

        

        if sp.simplify(idxE - integ) == 0: #simplificamos pues estos valores son de tipo float. Lo que llega a ser problematico. Si da 0 la resta. Entoces son iguales los valores. Asique devuelve la equacion
            return idx
        else:#sino da error lo que espero, ruego que no
            
                print('error en el calculo de la integral') 
                return 0
            
            
    else: #si hay funcion G calcula en area entre G y F, 
         
        if (sp.degree(g) > sp.degree(f)): #si g es de mayor grado que f entocens calcula la integral de f-g
            Areatotal =  sp.integrate(f,(x,bot,top))-sp.integrate(g,(x,bot,top))
            #print('g-f')
        elif (sp.degree(g) < sp.degree(f)):
            #print('f-g')
            Areatotal =  sp.integrate(g,(x,bot,top))-sp.integrate(f,(x,bot,top))
        elif (g.subs(x,5)) < (f.subs(x,5)):
            Areatotal =  sp.integrate(g,(x,bot,top))-sp.integrate(f,(x,bot,top))
        elif (g.subs(x,5)) > (f.subs(x,5)):
            Areatotal =  sp.integrate(f,(x,bot,top))-sp.integrate(g,(x,bot,top))
            
        return Areatotal
    
#----------------------------------------------------------#    
    
    
    
#-----------------------------------Main--------------------------------------------------#
    
h = sp.symbols('h')
x = sp.symbols('x')

fdeX = input("introdusca la funcion a evaluar : ")#introducimos la funcion en la consola
f = sp.lambdify(x, fdeX) #f(x)
f = sp.sympify(f(x))

segundafdeX = input("introdusca la segunda funcion a evaluar : ")#introducimos la funcion en la consola
g = sp.lambdify(x, segundafdeX) #f(x)
g = sp.sympify(g(x))


Nmin = int(input("introdusca el X minimo a evaluar: "))#introducimos el dominio valor minimo
Nmax = int(input("introdusca el X maximo a evaluar: "))#introducimos el dominio valor maximo
N = list(range(Nmin,Nmax+1))
N = DOM(f,N)


Integ = intg(f,None, Nmin, Nmax) #calcula la formula de la integral
X =[] #creamos una lista para los valores de X
Y = [] #creamos una lista para los valores de Y
AreaTotal_suma = intg(f,g, Nmin, Nmax)
#print(AreaTotal_suma)

print('Formula de la primera integral: ',Integ)
print('Formula de la segunda integral: ',intg(g,None,Nmin,Nmax))
AreaTotal = Integ.subs(x,Nmax)-Integ.subs(x,Nmin) #calcula el valor del area total de la zona achurada
#print('Total del area achurada: ',AreaTotal)
    
for valor in N: #llena la lista de X e Y con los valores del dominio y recorrido
    X.append(valor)
    valor = int(f.subs(x,valor))
    Y.append(valor)
        
        
plt.plot(X, Y,label=fdeX)
plt.fill_between(X, Y, alpha=0.4,color= 'grey')#muestra el area achurada
plt.grid(True)
plt.legend()
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Grafico del area bajo la curva f(x): ')
plt.show()
    
    
    #limpiamos la lista para llenarla con los valores de la segunda funcion
X.clear()
Y.clear()

    #segunda funcion
for valor in N: #llena la lista de X e Y con los valores del dominio y recorrido
    X.append(valor)
    valor = int(g.subs(x,valor))
    Y.append(valor)
        
        
plt.plot(X, Y,label=segundafdeX)
plt.fill_between(X, Y, alpha=0.4,color= 'grey')#muestra el area achurada
plt.grid(True)
plt.legend()
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Grafico del area bajo la curva g(x): ')
plt.show()    
    

#nueva lista para el recorrido de la segunda funcion y graficarlas juntas sin problema
Z = []
X.clear()
Y.clear()


for valor in N: #llena la lista de X, Y y Z con los valores del dominio y recorrido 
    X.append(valor)
    posZ = int(f.subs(x,valor))
    Z.append(posZ)
    posY = int(g.subs(x,valor))
    Y.append(posY)
        
plt.plot(X,Z,label = fdeX)  #Graficado de la primera funcion      
plt.plot(X, Y,label=segundafdeX) #Graficado de la segunda funcion
plt.fill_between(X, Y, Z , alpha=0.4,color= 'grey',label= 'Area total:')#muestra el area achurada
plt.grid(True)
plt.scatter(0,0,label = str(AreaTotal_suma),color='none')
plt.title('Grafico del area total entre dos funciones')
plt.legend(loc = 'best')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()   