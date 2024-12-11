
import sympy as sp
from sympy import symbols, Lambda, Matrix, sqrt, atan2, cos, sin,pi
from sympy.diffgeom import Manifold, Patch, CoordSystem
from sympy.diffgeom.rn import R2_r, R2_p

m = Manifold('M', 2)
p = Patch('P', m)
x, y,a,b = symbols('x y a b', real=True)
r, theta = symbols('r theta', nonnegative=True)
relation_dict = {
('Car2D', 'Pol'): Lambda((x, y), Matrix([sqrt(x**2 + y**2), atan2(y, x)])),
('Pol', 'Car2D'): Lambda((r, theta), Matrix([r*cos(theta), r*sin(theta)]))	#complicado de explicar, ver documentacin sympy en transformaciones
}
Car = CoordSystem('Car2D', p, [x, y], relation_dict)
Pol = CoordSystem('Pol', p, [r, theta], relation_dict)
x, y = Car.symbols
r, theta = Pol.symbols


def polarcon(f=0,des=1):
    if(f==0):#si hay un problema con la funcion introducida da ero
        print("error en polarcon, funcion entrada incorrecta")
        return 0
    
    if(des ==1):#cartesiano a polar
        
        w = (f.rewrite(Pol))
       # print(w)
        
    elif(des ==2):#polar a cartesiano
        w= f.rewrite(Car)

    else:#multiples escenarios usarlo en distintos escenarios y luego poder usarlo en otros porgramas
        print("error en des, polarcon")
        return 0
    if(f == w):
        print("!!")
    
    return w

def Integ (f,q,k,t,n):
    f = (sp.sympify(f)) *r #multiplicamos la funcion por R, el jacoviano de los polares
    #print(f)
    val = sp.integrate(f,(r,q,k))# integramos por primera vez
    #print(val)
   # print(sp.integrate(val,theta))
    val = sp.integrate(val,(theta,t,n))#integramos por segunda
    return val#devolvemos el resultado

t=0
f = input("Por favor introdusca una funcion de dos variables a evaluar  (x,y): ")
f = sp.lambdify((x,y),f)


while(not t):
    print("Por favor introdusca el tipo de tranformacion que actuara")
    print(" 1  =  Coordenadas polares  (r,0): ")
   # print(" 2  =  Coordenadas polares descentradas (xo,yo,r,0)")
   # print(" 2  =  Coordenadas elipticas (a,b,r,0)")
   # print(" 4  =  Transformacion Lineal (A,B,C,D,u,v)")
    try:# originalmente tenia pensado hacer para varias transformaciones pero por tema de tiempo lo deje en polar solamente
        S= int(input(":: "))
        if(not(S < 1 or S > 1)):
            t=1
        else:
            print("valores validos por favor")
            print("")
            print("")
            print("-")
    except ValueError:
        print("valores validos por favor")
        print("")
        print("")
        print("-")
        
t=0
while(not t):
    print("------------------")
    try:#pedimos los limites de parte del usuario , estos tienen que estar en termini de la transformacion polar
        print("Por favor introdisca los limites en termino polares")
        Lim1s = (input("Por favor ponga el limite superior de la primera integral : "))
        Lim1i = (input("Por favor ponga el inferior de la primera integral  : "))
        Lim1s = sp.sympify(Lim1s)
        Lim1i = sp.sympify(Lim1i)
        Lim2s =(input("Por favor ponga el limite superior de la segunda integral : "))
        Lim2i =(input("Por favor ponga el inferior de la primera integral  : "))
        Lim2s = sp.sympify(Lim2s)
        Lim2i = sp.sympify(Lim2i)
        t=1
    except:
        print("error en entradas por favor introdusca valores/simbolos validos")
    
if(S == 1):
    print("------------------")
    w = polarcon(f(x,y),1)
    print('Funcion Polar:', w)
    val = Integ(w,Lim1i,Lim1s,Lim2i,Lim2s)
    print('Volumen : {}'.format(val))
print("------------------")
