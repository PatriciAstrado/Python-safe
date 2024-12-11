import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import cm
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax2 = fig.add_axes([0.1, 0.85, 0.8, 0.1])
s = Slider(ax = ax2, label = 'value', valmin = 0, valmax = 5, valinit = 1)
t = sp.symbols('t')
x = sp.symbols('x')
y = sp.symbols('y')
z = sp.symbols('z')
print("ESTE PROGRAMA SOLO LEE HSTA CUATRO PUNTOS PARA CALCULAR HASTA LA TERCERA DIMENSION")
print("-")
print("-")
c_punto_eval = 0 #4
class puntos:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
    def __str__(self):
        return f"{self.x},{self.y},{self.z}"
p_0 = puntos(sp.symbols('p0_x'), sp.symbols('p0_y'), sp.symbols('p0_z'))
p_1 = puntos(sp.symbols('p1_x'), sp.symbols('p1_y'), sp.symbols('p1_z'))
p_2 = puntos(sp.symbols('p2_x'), sp.symbols('p2_y'), sp.symbols('p2_z'))
p_3 = puntos(sp.symbols('p3_x'), sp.symbols('p3_y'), sp.symbols('p3_z'))   
def leer_puntos():
    global c_punto_eval
    c_punto_eval = c_punto_eval+1
    tf=0
    print("Por favor introdusca el punto %d:  "	 % (c_punto_eval))
    print("formato: x,y,z")
    while(tf==0):
        try:
            a,b,c = (input(":: ").split(","))
            a=int(a)
            b=int(b)
            c=int(c)
            tf=1
        except:
            print("Por favor introdusca en el formato indicado y que sean valores numericos")
            
        
    return puntos(a,b,c)

def ds():
    tf = 0
    while (tf == 0):
        try:
            des = int(input('Desea terminar de dar puntos? ( 1:Si / 2:No )'))
            if(des == 1 or des == 2):
                tf=1
            else:
                print('Introdusca 1 o 2')
                print('')
        except:
            print("ERROR INPUT DESICION")
            print('')
    return des

def asignar_p():
    p_0 = leer_puntos()
    if((ds() !=1)):
        p_1 = leer_puntos()
        if((ds()!=1)):
            p_2 = leer_puntos()
            if((ds() !=1)):
                p_3 = leer_puntos()
                return p_0,p_1,p_2,p_3
            else:
                return p_0,p_1,p_2,None
        else:
            return p_0,p_1,None,None
    else :
        return p_0,None,None,None
 
 
 
 
def parametrizacion(p_0,p_1=None,p_2=None,p_3=None):
    global c_punto_eval
#     p_0x,p_0y,p_0z =p_0.x,p_0.y,p_0,z
#     p_1x,p_1y,p_1z =p_1.x,p_1.y,p_1,z
#     p_2x,p_2y,p_2z =p_2.x,p_2.y,p_2,z
#     p_3x,p_3y,p_3z =p_3.x,p_3.y,p_3,z
    if(p_1 is None):#punto
        print('Con solo un punto no se puede calcular nada!')
        return -1,-1,-1
    if(p_2 is None):#lineal
        B_tx = (1-t)* p_0.x +p_1.x *t
        B_ty = (1-t)* p_0.y +p_1.y *t
        B_tz = (1-t)* p_0.z +p_1.z *t 
    elif(p_3 is None):#cuadratica
        B_tx =(1-t)**2 *p_0.x + 2*t*(1-t)*p_1.x+t**2 *p_2.x
        B_ty =(1-t)**2 *p_0.y + 2*t*(1-t)*p_1.y+t**2 *p_2.y
        B_tz =(1-t)**2 *p_0.z + 2*t*(1-t)*p_1.z+t**2 *p_2.z
    else:#cubica
        B_tx=((1-t)**3 )*p_0.x +3*t*((1-t)**2) *p_1.x +3*(t**2) *(1-t)*p_2.x +3*(t**3) *p_3.x
        B_ty=((1-t)**3 ) *p_0.y +3*t*((1-t)**2) *p_1.y +3*(t**2) *(1-t)*p_2.y +3*(t**3) *p_3.y
        B_tz=((1-t)**3 ) *p_0.z +3*t*(((1-t)**2)) *p_1.z +3*(t**2) *(1-t)*p_2.z +3*(t**3) *p_3.z
        
    B_tx=sp.simplify(B_tx)
    B_ty=sp.simplify(B_ty)
    B_tz=sp.simplify(B_tz)
    
    return B_tx,B_ty,B_tz

def mesh(X,Y,Z,t=1):
    k = np.linspace(0, t, 100)
    Xm = (X(k))
    Ym = (Y(k))
    Zm = (Z(k))
    return Xm,Ym,Zm


p_0,p_1,p_2,p_3 = asignar_p()
# p_0 = puntos(0,0,0) #tests
# p_1 = puntos(1,1,1)
# p_2 = puntos(1,2,2)
# p_3 = puntos(3,0,3)

def longitud(btx,bty,btz,k=1):
    dtx = sp.diff(btx,t)
    dty = sp.diff(bty,t)
    dtz = sp.diff(btz,t)
    md = sp.sqrt((dtx)**2 +(dty)**2 +(dtz)**2)#modulo
    md = sp.simplify(md)
    l = sp.integrate(md,(t,0,k))
    return l
X,Y,Z = parametrizacion(p_0,p_1,p_2,p_3)

if(c_punto_eval != 1):
    Xf = sp.lambdify(t,X)
    Yf = sp.lambdify(t,Y)
    Zf = sp.lambdify(t,Z)
    print('x=',Xf(t))#funciones
    print('y=',Yf(t))
    print('z=',Zf(t))
    
    
    #print(LoArc)
    
    
    
    
    p0x,p0y,p0z = p_0.x, p_0.y, p_0.z
    
   
    def update(val):
        value = s.val
        ax.cla()
        X,Y,Z = mesh(Xf,Yf,Zf,value)
        ax.plot3D(X, Y, Z, label=('R(t) (({}) , ({}) , ({}))'.format(Xf(t),Yf(t),Zf(t))))
        LoArc = sp.N(longitud(Xf(t),Yf(t),Zf(t)),value)
        ax.scatter(0,0,0,c='w',label=('Longitud de arco: {}'.format(LoArc)))#plot de punto en concreto
        ax.scatter(p0x,p0y,p0z,c='r',label=('Punto 0: {}, {}, {}'.format(p0x,p0y,p0z)))#plot de punto en concreto
        #ax.plot3D(X, Y, Z, label=('R(t) (({}) , ({}) , ({}))'.format(Xf(t),Yf(t),Zf(t))))
        ax.set_zlim(-2, 7)
        if(p_1 is not None):
            p1x,p1y,p1z = p_1.x, p_1.y, p_1.z
            ax.scatter(p1x,p1y,p1z,c='r',label=('Punto 1: {}, {}, {}'.format(p1x,p1y,p1z)))#plot de punto en concreto
        if(p_2 is not None):
            p2x,p2y,p2z = p_2.x, p_2.y, p_2.z
            ax.scatter(p2x,p2y,p2z,c='r',label=('Punto 2: {}, {}, {}'.format(p2x,p2y,p2z)))#plot de punto en concreto
        if(p_3 is not None):
            p3x,p3y,p3z = p_3.x, p_3.y, p_3.z
            ax.scatter(p3x,p3y,p3z,c='r',label=('Punto 3: {}, {}, {}'.format(p3x,p3y,p3z)))#plot de punto en concreto
    
    
    

    s.on_changed(update)
    update(0)
    
    
    
    
    #ax.legend(loc='best',title = "Curvas de Beizer")
    plt.show()
# 
# print('')
# # print(X)
# # print(Y)
# # print(Z)
# print('')
# # print(p_0)
# # print(p_1)
# # print(p_2)
# # print(p_3)
# #print('cantidad puntos %d'%( c_punto_eval))
#  #int(input("::"))
else:
    print("No hay suficientes puntos para calcular la curva.")