import numpy as np
import sympy as sp
#http://hyperphysics.phy-astr.gsu.edu/hbasees/electric/elepot.html#c1

epsilon = 8.8541878176 * (10**(-12))
K = 1/(4*np.pi*epsilon) #constantes
r = sp.symbols('r')
R = sp.symbols('R')

def cargaPuntual(carga,r):  #calcula el potencial de una carga a distancia r
    potencialElectrico = K*carga /r
    return potencialElectrico


def cargasMultiples(carga_array,r_array): #recive arrays de datos que evalua y suma al potencial
    potencialElectrico =0#declaramos que existe y para que sume correctamente
    if len(carga_array) != len(r_array):#revisamos datos
        raise ValueError("Los datos de distancia y cargas tienen que ser la misma cantidad")
    for carga, r in zip(carga_array, r_array):#vamos por cada dato con este calculo = V = C_1 * K / r_1 + C_2 * K / r_2 +...+C_n * K / r_n
        potencialElectrico += (K*carga/r)
    return potencialElectrico


def cargaLineal (densidad, distancia_final,distancia_inicial,altura,): #si la distancia incial esta detras de 0, tiene que estar en negativo
        sup = distancia_final+ sp.root((distancia_final**2)+(altura**2))
        inf = distancia_inicial + sp.root((distancia_inicial**2)+(altura**2))
        potencialElectrio = densidad*K * (sp.log(sup/inf))
        return potencialElectrio
    
def anilloDeCargas (densidad,Radio,altura):
    distancia_punto = sp.root(Radio**2 + altura**2)
    potencialElectrico = (K*densidad*2*np.pi*Radio) /distancia_punto  #version dependiente de densidad lineal
    #potencialElectrico = K*carga / distancia_punto    #version dependiente de carga
    return potencialElectrico

def discoDeCargas (densidad,Radio_gus,altura):
    distancia_punto = sp.root(Radio_gus**2 + altura**2)
    potencialElectrico = K*densidad*2*np.pi * (distancia_punto -altura)
    return potencialElectrico

def esferaConductoraCargadaUniformemente (carga,radio_obj,Radio_gus):
    #http://laplace.us.es/wiki/index.php/Esfera_conductora_en_equilibrio_electrost%C3%A1tico
    if(radio_obj <= Radio_gus):  
        potencialElectrico = K*carga / radio_obj
    elif (radio_obj > Radio_gus):
        potencialElectrico = K*carga / Radio_gus   
    return potencialElectrico


    