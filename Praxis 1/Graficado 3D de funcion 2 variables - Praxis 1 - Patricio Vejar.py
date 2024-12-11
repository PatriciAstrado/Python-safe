import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy import sin, pi
import matplotlib.animation as animation
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')


v = sp.symbols('v')
u = sp.symbols('u')

def update_plot(frame_number, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(dom_x, dom_y, Z[:,:,frame_number], cmap="magma")

f = sp.sin(u)* sp.cos(v)
txt = "Superficie 3D de la funcion f(x,y)= sen(x)*cos(y)"
f = sp.lambdify((u ,v), f,modules=['numpy']) #f(x) La convertimos en funcion respecto a u,v usando sympy y que acepte el modelo de datos de numpy


if(int(input("Quiere evaluar una funcion de su eleccion (no trigonometricas) [1] ó utilizar la funcion base= (sen(u)*cos(v)) [0]")) == 1):
    
    fdeX = input("introduzca la funcion a evaluar respecto .u.  y  .v. : ")#introducimos la funcion en la consola
    f = sp.sympify(fdeX) #la simplificamos usando sympy
    f = sp.lambdify(((u ),(v )), f,modules=['numpy']) #f(x) La convertimos en funcion respecto a u,v usando sympy y que acepte el modelo de datos de numpy
    txt = "Superficie 3D de la funcion f(x,y)=",str(f(u,v))



fps = 10 #frames por segundo
frn = 50 #cantidad de frames por animacion
N = int(input('Por favor introdusca el rango al que evaluar la funcion : '))
# asignamos a unba variable el rango de datos 


# Creamos una lista de datos para cada dominio de X e Y
dom_x = np.linspace(-N,N,100)
dom_y = np.linspace(-N,N,100)



#los convertimos en coordenadas de matrices a partir de vectores
dom_x,dom_y = np.meshgrid(dom_x,dom_y)
Z = np.zeros((100, 100,frn))
#evaluamos la funcion F apartir de los arrays de matrices en X e Y
for i in range(frn):
    Z[:,:,i] = f(dom_x,dom_y)





# Mostramos la superficie
plot = [ax.plot_surface(dom_x, dom_y, Z[:,:,0], color='0.75', rstride=1, cstride=1)]

#ax.plot_surface(dom_x,dom_y,Z,cmap='viridis')



#ax.set_aspect('equal')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(txt)
ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(Z, plot), interval=1000/fps)
plt.show()
