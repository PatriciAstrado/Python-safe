import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
x = sp.symbols('x')
y = sp.symbols('y')
h = sp.symbols('h')

def der_par(f,v):#calculamos la derivada parcial del mismo modo que la derivada normal pero con la diferencia que ahora podemos llamarlo referenciado que variable
        expr = (((f.subs(v, v+h)) - (f))/h)  #((f(x+h,y)-f(x,y))/h)
        smpl = sp.simplify(expr)
       #notar que H solo se suma a la variable asignada al llamar la funcion, esta variable sera remplazada por V+H
        
        expr = sp.limit(smpl,h,0) #lim h->0
        
        expr = sp.lambdify(x, expr) #expr(x,y) lo convierte en usa funcion en base a X,Y
        #todo esto equivale a ::                  f´(x,y) = lim h->0 ((f(x+h,y)-f(x,y))/h)
        
        
        #Probamos a enviar la funcion respecto 2 variables
        #si da error la enviara respecto 1 variable
        #esto es para asegurarse que *dependiedo de la funcion dada* no de errores inesperados
        try: 
           # print(expr(x,y))
            return expr(x,y)
        except  TypeError:
           # print(expr(x))
            return expr(x)
        
        

def p_tangente(fx,fy,a,b,c):
    #formula= derX(a,b)*(x-a) +derY(a,b)*(y-b) =(z-c)
     
     #evaluamos las derivadas parciales por los puntos dados, remplazando las variables si es que existen por sus respectivos puntos
    fx = fx.subs({x:a,y:b})
    fy = fy.subs({x:a,y:b})
   
   #calculamos la formula directamente y la simplificamos 
    formula = fx * (x-a) +fy * (y-b) + c   
    fla = sp.simplify(formula)
    #la convertimos en funcion
    fla = sp.lambdify(((x ),(y )),fla)
    
    #la enviamos
    return fla



fdeX = input("Por favor introdusca una funcion de dos variables a evaluar  (x,y): ")#introducimos la funcion en la consola
f = sp.sympify(fdeX) #la simplificamos usando sympy
f = sp.lambdify(((x ),(y )), f,modules=['numpy']) #f(x) La convertimos en funcion respecto a u,v usando sympy y que acepte el modelo de datos de numpy
 
N = int(input('Por favor introdusca el dominio de X e Y al que evaluar la funcion : '))
# asignamos a una variable para el rango de datos 

#preguntamos por los puntos en el que el plano tiene que tocar
A,B,C = (input("Por favor introdusca los puntos al que evaluar y buscar el plano tangente,  *Separados por comas*  a,b,c: ").split(","))
A,B,C = int(A,),int(B),int(C)

# Creamos una lista de datos para cada dominio de X e Y
dom_x = np.linspace(-N,N,100)
dom_y = np.linspace(-N,N,100)
dom_x,dom_y = np.meshgrid(dom_x,dom_y)

#evaluamos en Z la funcion respecto los dominios de X e Y
Z = np.zeros((N, N,N))
Z = f(dom_x,dom_y)

#calculamos las derivadas parciales de la funcion respecto X e Y
DFx  = der_par(f(x,y),x) #duncion derivada parcial de X
DFy = der_par(f(x,y),y) #funcion derivada parcial de y


PT = p_tangente(DFx,DFy,A,B,C) #formula del plano tangente en los puntos 1,1,2 segun x,y  PT(x,y)

dom_xt = dom_x#repetimos los diminios con distinto nombre por tema de sintax y orden personal
dom_yt = dom_y

Zt = np.zeros((N, N,N))#creamos el array para el plano en los Z y lo evaluamos en su respectiva funcion
Zt = PT(dom_xt,dom_yt)



#PLOT :)		no tiene chiste, solo algunos cambios de propiedades para que se vea mejor
ax.plot_surface(dom_xt,dom_yt,Zt,color='g',alpha = 0.25,label = ('Plano tangente:', str(PT(x,y))))#plot del plano tangente
ax.plot_surface(dom_x,dom_y,Z,color='m',alpha = 0.5,label = ('Funcion Original:',str(f(x,y))))#plot de funcion orignial
ax.scatter(A,B,C,c='r',label=('Punto en concreto: {}, {}, {}'.format(A, B, C)))#plot de punto en concreto
ax.legend(loc='upper left',title = "Plano tangente a un punto")
plt.show()