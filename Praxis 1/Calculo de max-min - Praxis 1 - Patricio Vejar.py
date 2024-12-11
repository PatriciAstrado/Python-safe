
import numpy as np
import sympy as sp
#	x**3 +y*3-y**3-3*x funcion prueba sola

#funcione prueba conjunta
#	9-x**2-y**2
#	x+y-2

x = sp.symbols('x')
y = sp.symbols('y')
l = sp.symbols('l')
z = sp.symbols('z')

def lagrange(f,g):
    
    fx = sp.diff(f,x)
    fy = sp.diff(f,y)
    gx = sp.diff(g,x)
    gy = sp.diff(g,y)
    lambx = (fx / gx) -l
    lamby = (fy / gy) -l
   # print(lambx)
    #print(lamby)
    
    sol = sp.solve([(lambx),(lamby),(g)])
    print(sol)
    xo=sol[x]
    yo=sol[y]
    zo = f.subs([(x,xo),(y,yo)])
  #  print(xo,yo,zo)
    
    det,feex=determinar(f,xo,yo)
    cond = compa(det,feex)
    #heisen(f,g,xo,yo)
    if(cond == 0):
        print("No hay informacion en el punto : (",xo,",",yo,",",zo,")")
    elif (cond == 1):
        print("Es un punto silla en : (",xo,",",yo,",",zo,")")
    elif(cond == 2):
        print("Es un punto minimo local en : (",xo,",",yo,",",zo,")")
    elif(cond == 3):
        print("Es un punto maximo local en : (",xo,",",yo,",",zo,")")


def heisen(f,g,a,b):
    fx = sp.diff(f,x)
    fy = sp.diff(f,y)
    gx = sp.diff(g,x)
    gy = sp.diff(g,y)
    
    gxx = sp.diff(gx,x)
    gyy = sp.diff(gy,y)
    gxy = sp.diff(gx,y)
    
    fxE = fx.subs([(x,a),(y,b)])
    fyE = fy.subs([(x,a),(y,b)])
    gxxE = gxx.subs([(x,a),(y,b)])
    gyyE = gyy.subs([(x,a),(y,b)])
    gxyE = gxy.subs([(x,a),(y,b)])
    
    
    H = -fxE*(-fxE*gyyE -gxyE* -fyE) + fyE*(-fxE*gxyE - gxxE* -fyE)
    #print(H)

def compa (det,fxxE): #comparamos los datos de determinante y la segunda derivada evaluada
    if(det == 0): 		#y dependiedo devolvemos un valor en concreto que luego se compara, 
        return 0		#funcion para acortar la cantidad de comparaciones llamadas en main
    elif(det < 0):#silla
        return 1
    elif(det > 0):
        if(fxxE > 0): #minimo
            return 2 
        elif(fxxE < 0): #maximo
            return 3
        else:
            print("error")
            return 0
    else:
        print("error")
        return 0


def determinar(f,a,b): #calcula el determinante apartir de 1 punto critico y devuelve el valor de determinante y la segunda derivada evaluada
    fx = sp.diff(f,x)
    fy = sp.diff(f,y)#primeras derivadas
    
    fxx = sp.diff(fx,x)#segundas derivadas
    fyy = sp.diff(fy,y)
    fxy = sp.diff(fx,y)
    fyx = sp.diff(fy,x)
    
    fxxE = fxx.subs([(x,a),(y,b)])#segundas derivadas evaluadas
    fyyE = fyy.subs([(x,a),(y,b)])
    fxyE = fxy.subs([(x,a),(y,b)])
    fyxE = fyx.subs([(x,a),(y,b)])

    det = fxxE * fyyE - fxyE * fyxE #determinante
    print("Determinante: ",det)
    return det, fxxE

def puntos0 (f): #los puntos criticos de una funcion
    fx = sp.diff(f,x)
    fy = sp.diff(f,y)
    
    x0 = sp.solve(fx,x)
    y0 = sp.solve(fy,y)
    if(x0 or y0): #preguntamos si la lista esta vacio: si no hay datos encontrados : si no hay puntos criticos
        return x0,y0
    else:
        print("No se encontraron puntos criticos")
        return [0],[0]


S = int(input("Le gustaria evaluar 1 funcion o 2 funciones?:   si:1 / no:2"))

if(S == 1):
    
    fdeX = input("Por favor introdusca una funcion de dos variables a evaluar  (x,y): ")
    fdeX = sp.sympify(fdeX)	
    fdeX = sp.lambdify((x,y),fdeX)
    
    gdeX = input("Por favor introdusca una segunda funcion de dos variables limitante a evaluar  (x,y): ")
    gdeX = sp.sympify(gdeX)
    gdeX = sp.lambdify((x,y),gdeX)
    
    lagrange(fdeX(x,y),gdeX(x,y))
else:


    fdeX = input("Por favor introdusca una funcion de dos variables a evaluar  (x,y): ")
    fdeX = sp.sympify(fdeX)
    fdeX = sp.lambdify((x,y),fdeX)
    xo,yo = puntos0(fdeX(x,y)) #lista de puntos criticos

    print("------------------")

    #evalua todos los puntos criticos posibles
    for a in xo:
        for b in yo:
            det,fxxE = determinar(fdeX(x,y),a,b)
            cond = compa(det,fxxE)
            
            if(cond == 0):
                print("No hay informacion en el punto : (",a,",",b,")")
            elif (cond == 1):
                print("Es un punto silla en : (",a,",",b,")")
            elif(cond == 2):
                print("Es un punto minimo local en : (",a,",",b,")")
            elif(cond == 3):
                print("Es un punto maximo local en : (",a,",",b,")")
            else:
                print("error")
            
            
print("*_*")