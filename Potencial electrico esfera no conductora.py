import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

r = sp.symbols('r')
R = sp.symbols('R')
q = sp.symbols('q')
p = sp.symbols('p')
e = sp.symbols('e')
#potencial de una carga cosntante en una esfera no conductora , distribucion uniforme p ; p= constante
epsilon = e  #= 8.8541878176 * (10**(-12))

#Kconstante = (8.99) * (10**9)	#1/4np.pi*eps = 8.99 * 10^9
superficie = 4* np.pi * (r**2) #superficie redonda r = radio en que evaluar respecto la esfera cargada
q =p * ((4/3) * np.pi * R**3) #carga electrica constate podemops decir que es p*volumen ; R = radio de la esfera cargada

#escribimos el campo en terminos constantes como la distribucion y el volumen 
E = q / (epsilon * superficie)

print("Campo electrico")
print(E)#el cambo electrico ecuacion
#print(E.evalf(subs={e: (8.8541878176 * (10**(-12)))}))##el campo evaluado en el valor numerico para comprobar

#potencuial electrico
print("Potenciales electricos ; R = radio de carga, r = radio de esfera de prueba ")
V = (sp.integrate(E,(r,R, np.inf)))
print("	Escenario R > r")
print(V) ##escenario donde R =/= r

print("	ESCENARIO R==r")
Vr = V.evalf(subs={r:R})
print(Vr)#escenario donde R==r


print("	ESCENARIO R < r")

E = E.evalf(subs={R:r})
#print(E)
#VR - Vr = -integro Edr respecto r-R


integE = (sp.integrate(E,(r,r,R)))
integE = sp.simplify(integE)

VR = integE + Vr
print(VR)
