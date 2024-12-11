import re
import sympy as sp
import os
from time import sleep
PI = 3.141592653589793



#-----------------VOLUMEN------------------------------#
def Vol(f,top,bot):
    try:      
        resultado = sp.integrate((f**2)*PI,(x,bot,top))
        return resultado
    except ValueError:
        print('ERROR EN VOL . VALOR NUMERICO INVALIDO')
                 
#------------------------------------------------------#




#------------------LONGITUD DE ARCO----------------------------------#
def Long(ddf,top,bot):
    try :
        ecuacion = sp.sqrt(1+(ddf)**2)
        integ = (sp.integrate(ecuacion,(x,bot,top))).evalf()
        #print(ecuacion)
        #print('longitud de arco :',integ.evalf())
        return integ
    except ValueError:
        print('ERROR EN LONG . VALOR NUMERICO INVALIDO')

#--------------------------------------------------------------------#






#------------------------ARAE DE SUPERFICIE----------------------------------------#
def Area_super(f,ddf,top,bot):
    try:
        #ecuacion de superficie:  integral(2pi * |f(x)| * raiz(1+(ddf)^2))  --> Origen: WA
        ecuacion = 2*PI* abs(f) * sp.sqrt(1+(ddf)**2)
        resultado = sp.integrate(ecuacion,(x,bot,top))
        resultado_aproximado = resultado.evalf()
        #print('area de superficie SIN EVALF: ',resultado)
        print('area de superficie CON EVALF: ',resultado_aproximado)
    except ValueError:
        print('ERROR EN AREA_SUPER . VALOR NUMERICO INVALIDO')

#---------------------------------------------------------------------------#







#----------------------------MAIN-------------------------------#
 
h = sp.symbols('h')
x = sp.symbols('x')

done = False
while not done:
    top = input('Introduzca el valor maxima a evaluar la integral: ')
    
    try:
        top = int(top)
        #print('True')  
        done = True
    except ValueError:
        print('POR FAVOR INTRODUZCA UN VALOR VALIDO (número)')
      
      
done = False
while not done:
    bot = input('Introduzca el valor minima a evaluar la integral: ')
    
    try:
        bot = int(bot)
        #print('True')  
        break
    except ValueError:
        print('POR FAVOR INTRODUZCA UN VALOR VALIDO (número)')        


if(top < bot):
    holder= top
    top = bot
    bot = holder

done = False    
while not done:
    try:
        raiz = int(input('te gustaria calcular la raiz de una funcion? (Si:1\ No:0)')    )
        raiz = int(raiz)
        if(raiz == 1 or raiz == 0):
            break 
        else:
            print('ERROR NUMERICO . POR FAVOR INTRODUZCA UN VALOR VALIDO (0 o 1)')
            
    except ValueError:
        
        print('ERROR DE ENTRADA. POR FAVOR INTRODUZCA UN VALOR VALIDO (0 o 1)')      



done = False
# ------ Entrada con cualquier variable
while not done:
    try:
        if(raiz == 0):
            fdeX = input("Introduzca la función (1 sola variable): ")
            # Replace 'x' with 'x' and handle 'sqrt'
            fdeX = re.sub(r'[^x0-9\+\-\*\/\(\)\.\^]', '', fdeX)  # Keep other characters
            fdeX = re.sub(r'sqrt', 'sp.sqrt', fdeX)
            fdeX = sp.sympify(fdeX)
            result = sp.simplify(fdeX)
            f = sp.lambdify(x, fdeX)  # f(x)
            print('Función leída respecto a x:', f(x))
            der = sp.diff(f(x), x) 
            break
        elif(raiz == 1):
            fdeX = input("Introduzca la función (1 sola variable): ")
            # Replace 'x' with 'x' and handle 'sqrt'
            fdeX = re.sub(r'[^x0-9\+\-\*\/\(\)\.\^]', '', fdeX)  # Keep other characters
            fdeX = re.sub(r'sqrt', 'sp.sqrt', fdeX)
            fdeX = sp.sympify(fdeX)
            result = sp.simplify(fdeX)
            f = sp.lambdify(x, fdeX)  # f(x)
            f = sp.sqrt(f(x))
            f = sp.lambdify(x, fdeX)  # f(x)
            der = sp.diff(f(x), x) 
            break
    except:
        print('ERROR DE ENTRADA. POR FAVOR INTRODUZCA UNA FUNCION VALIDA')
        print(e)

    
f = sp.lambdify(x, fdeX) #f(x)
ddx = sp.lambdify(x, der) #ddf(x)



integ = Vol(f(x),top,bot)
lon = Long(ddx(x),top,bot)
ar = Area_super(f(x),ddx(x),top,bot)






print('longituid de arco : ',lon)
print('Volumen: ',integ,' u^2')
print('pi: ',PI)
print('Funcion',fdeX)
#print(f(2))
print('Derivada: ',der)
#print(ddx(2))