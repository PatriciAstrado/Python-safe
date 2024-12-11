import matplotlib.pyplot as plt
import sympy as sp


def ejes_principales(): ## define lineas en los ejes x=0 e y=0
    
    fix, ax = plt.subplots()
    
    for spine in ['left','bottom']:
        ax.spines[spine].set_position('zero')
        
    for spine in ['right','top']:
        ax.spines[spine].set_color("none")
     
    return ax







#-------------------------Grafico------------------------------------#

def Graf(x,y,z,w):
     
    
    ax = ejes_principales()
    ax.grid()
    ax.plot(x,y,label="funcion") #funcion
    plt.legend()
    plt.title('Funcion')
    plt.ylabel('f(x)')
    plt.xlabel('x')
    plt.show() #grafica funcion
    ax = ejes_principales()
    ax.grid()
    ax.plot(x,z,label="derivada") # derivada
    plt.legend()
    plt.title('Derivada')
    plt.ylabel('f(x)')
    plt.xlabel('x')
    plt.show() #grafica derivada
    ax = ejes_principales()
    ax.grid()
    ax.plot(x,w,label="integral") # integral
    plt.legend()
    plt.title('Integral')
    plt.ylabel('f(x)')
    plt.xlabel('x')
    plt.show() #grafica integlar
    

#-----------------------------------------------------------------#







#---------------------Graficos de todo a la vez-----------------------------#
def Graf_unido(x,y,z,w): #muestra el plot apartir de los datos y funcion dados
    
    
    ax = ejes_principales()
    ax.grid()
    ax.plot(x,y,label="funcion") #funcion
    ax.plot(x,z,label='derivada')
    ax.plot(x,w,label='integral')
    plt.legend()
    plt.title('Funcion')
    plt.ylabel('f(x)')
    plt.xlabel('x')
    plt.show() #grafica funcion
#--------------------------------------------------------------------------------------#
    
    
    
    
    
    

#------------------------------INTEGRALES DEFINIDAS----------------------#
def intg(f):
    top = 2 #numeros de prueba para comparar los dos limites
    bot = 1
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
#----------------------------------------------------------#








#----------------CALCULO DE DERIVADA--------#
def ddf(f,fo):
        #a mano
    expr = (((f.subs(x, x+h)) - (f))/h)  #((f(x+h)-f(x))/h)
    smpl = sp.simplify(expr)
       
    expr = sp.limit(smpl,h,0) #lim h->0
    
    expr = sp.lambdify(x, expr) #expr(x) lo convierte en usa funcion en base a X
    #todo esto equivale a ::                  f´(x) = lim h->0 ((f(x+h)-f(x))/h)
    
   
    
    ddf_sp = sp.diff(fo,x)#calculamos la derivada segun la funcion sympy.diff
    ddf_sp = sp.lambdify(x, ddf_sp) #ddf_x(x)
    
    if expr(x) == ddf_sp(x): # si la ecuaciones son iguales devuelve la hecha a mano
        return expr(x)
    else:#rogemos que no de
        print('error en el calculo de la derivada')
        return 0
#--------------------------------------------------#










#---------------Evaluar G funcion dada, en T punto dado------------------------------#

def Feval(g,t): #evaluar funcion en t
    sol = g.subs(x,t)
    #g(t) ; g = funcion dada ; t = punto dado
    return sol
    ax.grid()
#---------------------------------------------#











#----------------RECTA TANGETE A X_0, Y_0 ---------------------------------------------#

def Rtan(ddx,x_0,y_0):
    m = ddx.subs(x,x_0) #calculamos la pendiente usando la derivada y evaluandola en el punto x_0
    recta = (m*(x - x_0)) + y_0  #calculamos la recta con la pendiente y puntos dados
    recta = sp.simplify(recta) #simplificamos
    
    
   # recta = sp.lambdify(x, recta)
    
    return recta # devolvemos la ecuacion
#-----------------------------------------------------------------------#











#--------------------------------Graficado recta tangente----------------------------#
def Gtan(x,y,tan,x_0,y_0):
    ax = ejes_principales()
    ax.grid()
    ax.scatter(x_0,y_0,label = 'punto tangente',color='r') #marca el punto donde toca la tangente y la funcion
    ax.scatter(x_0,y_0,label = (str(x_0),str(y_0)),color='none') #marca el punto donde toca la tangente y la funcion
    ax.plot(x,y,label="funcion",color = 'b') #funcion
    ax.plot(x,tan,label = 'Tangente') #linea recta tangente
    plt.legend() 
    plt.title('tangente')
    plt.ylabel('y')
    plt.xlabel('x')
   
    plt.show()
#----------------------------------------------------------#
    
    
    
    
    
    
    




#----------------------MAIN""---------------------------------#

#leemos un documento del cual sacaremos los datos
#FORMATO DEL DOC
# primera linea la funcion  SIN ESPACIOS  ex: 2*x**2 +1 
# segunda linea el punto a evaluar
# tercera linea Punto minimo a evaluar intregral
# cuarta linea Punto maximo a evaluar integral			
# quinta linea , puntos a evaluar en grafica, 1 solo numero
# sexta linea, punto x_0 para evaluar la tangente. TIENE QUE PERTENECER AL DOMINIO DE F Y DENTRO DEL LIMITE DE -N,N PARA QUE SE GRAFIQUE BIEN
# septima linea, punto y_0 para evaluar la tangente. TIENE QUE PERTENECER AL RECORRIDO DE F
DocInput = open('Entrada.txt','r')
fdeX = DocInput.readline()
Eval = int(DocInput.readline())
Min = int(DocInput.readline())
Max = int(DocInput.readline())
N = int(DocInput.readline())
x_0 = int(DocInput.readline())
y_0 = int(DocInput.readline())
DocInput.close()

h = sp.symbols('h')
x = sp.symbols('x')

if int(input("Desea introducior por la consola la funcion (1) o leer el documento \"Entrada.txt\" : ")) == 1:
    
    fdeX = input("introdusca la funcion a evaluar : ")#introducimos la funcion en la consola
    #Esto solo leera y dara la funcion. Aun leera los demas datos de el archivo
    #por ende si el archivo no existe o no tiene los datos dara error



f = sp.lambdify(x, fdeX) #f(x)



fA1 = x**2 + x + 5
fA1_x = sp.lambdify(x, fA1) #fA1_x(x)
punt_evaluar = 2

DinDX_A1 = ddf(fA1_x(x),fA1)
DinDX_A1_x = sp.lambdify(x,DinDX_A1 ) #DinDX_A1(x)

#print('funcion de A1 :',fA1_x(x))
#print('ecuacion de la derivada A1:',DinDX_A1)

punto_evaluado = Feval(fA1_x(x),punt_evaluar)
punto_evaluado_der = Feval(DinDX_A1_x(x),punt_evaluar)
    
#print('evaluados en el punto: ',punt_evaluar)
#print('funcion en el punto: ',punto_evaluado)
#print('derivada en el punto: ',punto_evaluado_der)

try :
    f = sp.sympify(f(x))
    
except sp.SympifyError:
    print('funcion invalida')

else:
    DinDX = ddf(f,fdeX)
    Inter = intg(f)
    RectaTan = Rtan(DinDX,x_0,y_0)
    
    #Eval = int(input('Punto a evaluar: '))
    
    print('Funcion leida: ',f)
    print('equacion para derivada: ',DinDX )
    print('equacion para integral: ' , Inter )
    print('Tangente en los puntos x_0, y_0: ',RectaTan)
    

    PuntoF = Feval(f,Eval)#evalua funcion en Eval
    print('f(',Eval,') = ',PuntoF)

    PuntoD = Feval(DinDX,Eval) #evalua derivada en Eval
    print('D(',Eval,') = ',PuntoD)

    PuntoI = int(Feval(Inter,Eval)) #evalua integral en Eval
    print('I(',Eval,') = ',PuntoI)


    #area con integrales

    #pedimos los puntos a evaluar la integral
    #Min =  input("Introdusca el punto minimo a evaluar de la integral: ")
    #Max =  input("Introdusca el punto maximo a evaluar de la funcion integral: ")
    #calculamos el area total con los datos dados

    #teorema de barrraow
    AreaT = int(Feval(Inter,Max)) - int(Feval(Inter,Min))

    # los mostramso junto con la "formula" seguida
    print('I(',Max,') - I(',Min,') = ',AreaT, ' aproximadamente')



    #escribimos todos los datos en el rachivo llamado Salida.txt
    DocOut = open('Salida.txt','w')
    DocOut.writelines('Funcion Original ; F(x) = ')
    DocOut.writelines(str(fdeX))
    DocOut.writelines('\nEvaluados en: ')
    DocOut.writelines(str(Eval))
    DocOut.writelines('\nPunto X evaluado para tangente: ')
    DocOut.writelines(str(x_0))
    DocOut.writelines('\nPunto Y evaluado para tangente: ')
    DocOut.writelines(str(y_0))
    DocOut.writelines('\nFuncion original evaluada en el punto Eval ')
    DocOut.writelines(str(PuntoF))
    DocOut.writelines('\nEcuacion de la derivada ; D(x) = ')
    DocOut.writelines(str(DinDX))
    DocOut.writelines('\nDerivada evaluada en el punto Eval: ')
    DocOut.writelines(str(PuntoD))
    DocOut.writelines('\nTangente en los puntos x_0, y_0: ')
    DocOut.writelines(str(RectaTan))
    DocOut.writelines('\nEcuacion de la integral ;I(x) = ')
    DocOut.writelines(str(Inter))
    DocOut.writelines('\nIntegral evaluada en el punto Eval: ')
    DocOut.writelines(str(PuntoI))
    DocOut.writelines('\nMinimo de la funcion: ')
    DocOut.writelines(str(Min))
    DocOut.writelines('\nMaximo de la funcion: ')
    DocOut.writelines(str(Max))
    DocOut.writelines('\nArea total de integral entre minimo y maximo: ')
    DocOut.writelines(str(AreaT))
    DocOut.writelines('\n')
    DocOut.close()
        
    N = list(range(-N,N+1)) # crea una lista de numeros segun N, siendo -N hasta N+1 ; ex: N= 10. -N = -10, N+1 = 10. nuevo N = -10,-9,...9,10
    
    
    X = [x for x in N] #convierte x en todos los numeros de la lista N
    Y = [f.subs(x,p) for p in X] #evalua puntos de x en F(x) y los pone en una lista de Y
    Z = [DinDX.subs(x,q) for q in X] #evalua puntos de x en DinDX(x) y los pone en una lista de Z
    W = [Inter.subs(x,t) for t in X]#evalua puntos de x en Inter(x) y los pone en una lista de W
    R = [RectaTan.subs(x,r) for r in X]#evalua los puntos de x en RecTan(x) y los pone en la lista R
    
    Graf(X,Y,Z,W) #genera las graficas de cada una una por una
    Graf_unido(X,Y,Z,W)
    Gtan(X,Y,R,x_0,y_0)