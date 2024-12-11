import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib import animation

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
x = sp.symbols('x')
y = sp.symbols('y')
h = sp.symbols('h')





def der_par(f,v):
        expr = (((f.subs(v, v+h)) - (f))/h)  #((f(x+h)-f(x))/h)
        smpl = sp.simplify(expr)
       
        expr = sp.limit(smpl,h,0) #lim h->0
    
        expr = sp.lambdify(x, expr) #expr(x) lo convierte en usa funcion en base a X
        #todo esto equivale a ::                  f´(x) = lim h->0 ((f(x+h)-f(x))/h)
        
        try:
            print(expr(x,y))
            return expr(x,y)
        except  TypeError:
            print(expr(x))
            return expr(x)
        
        

def p_tangente(fx,fy,a,b,c):
    #formula= derX(a,b,c)*(x-a) +derY(a,b,c)*(y-b) =(z-c)
     
    fx = fx.subs({x:a,y:b})
    fy = fy.subs({x:a,y:b})
   
    formula = fx * (x-a) +fy * (y-b) + c   
    fla = sp.simplify(formula)
    
    fla = sp.lambdify(((x ),(y )),fla)
    
    return fla



fdeX = input("introduzca la funcion a evaluar respecto .x.  e  .y. : ")#introducimos la funcion en la consola
f = sp.sympify(fdeX) #la simplificamos usando sympy
f = sp.lambdify(((x ),(y )), f,modules=['numpy']) #f(x) La convertimos en funcion respecto a u,v usando sympy y que acepte el modelo de datos de numpy
 
N = int(input('Por favor introdusca el dominio de X e Y al que evaluar la funcion : '))
# asignamos a unba variable el rango de datos 

A,B,C = (input("Por favor introdusca los puntos al que evaluar y buscar el plano tangente: ").split(","))
A,B,C = int(A,),int(B),int(C)
# Creamos una lista de datos para cada dominio de X e Y
dom_x = np.linspace(-N,N,100)
dom_y = np.linspace(-N,N,100)
dom_x,dom_y = np.meshgrid(dom_x,dom_y)


Z = np.zeros((N, N,N))
Z = f(dom_x,dom_y)

#calculamos las derivadas parciales de la funcion respecto X e Y
DFx  = der_par(f(x,y),x) #duncion derivada parcial de X
DFy = der_par(f(x,y),y) #funcion derivada parcial de y


PT = p_tangente(DFx,DFy,A,B,C) #formula del plano tangente en los puntos 1,1,2 segun x,y  PT(x,y)

dom_xt = dom_x
dom_yt = dom_y

Zt = np.zeros((N, N,N))
Zt = PT(dom_xt,dom_yt)

def init():
    ax.plot_surface(dom_xt,dom_yt,Zt,color='g',alpha = 0.25,label = ('Plano tangente:', str(PT(x,y))))#plot de funcion orignial
    ax.plot_surface(dom_x,dom_y,Z,color='m',alpha = 0.5,label = ('Funcion Original:',str(f(x,y))))#plot de funcion orignial
    
    
    return fig,

def animate(i):
    # azimuth angle : 0 deg to 360 deg
    ax.view_init(elev=10, azim=i)	
    ax.scatter(A, B, C, c='r')  # Update the scatter plot position
    return ax.scatter(A, B, C, c='r'),  # Return the updated scatter plot


ax.scatter(A,B,C,c='r',label='Punto en concreto: {}, {}, {}'.format(A, B, C))#plot de punto en concreto
ax.legend(loc='upper left')

ani = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=90, interval=50, blit=True)
plt.show()

