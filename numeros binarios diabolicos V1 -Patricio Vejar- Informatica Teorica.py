

#------------------Entrada a bin str---------------------#
def string_binario (n): #entrada n=numero, salida = binario en formato string
    
    finish = 0
    str_bin = []
    
    if (n != 0 and n!= 1):
        while(finish == 0):
            str_bin.append(str(int(n%2)))
            n = int(n/2)
            
            if(n == 1 or n == 0):
                str_bin.append(str(n))
                finish = 1
                
                
        str_bin.reverse()
        
        return str_bin
    else:
        return str(n)
#----------------------------------------------------------------------------------#    
    
    
#--------------------Es el numero diabolico?-----------------------------#
def bin_diabolico (str_bin): #entrada string preferiblemente binario, salida = false/true
    x = str_bin.count("0")
    x = x%2
    if(x ==0):
        return True
    else:
        return False
#-------------------------------------------------------------------------------------------------# 
 
 

valor = 0
done =False


while not done:#en un mientras el valor sea un numero para asegurase de la naturaleza de la entrada 
    print("Por favor introdusca el numero que desea evaluar si su forma binaria es de naturaleza diabloica... :")
    valor = input()
    try :
        valor = int(valor)
        done = True
    except ValueError: 
        print('POR FAVOR INTRODUZCA UN VALOR VALIDO (número)')


binario = string_binario(valor)  

print(binario)  #mostramos el numero binario

#preguntamos la naturaleza de la funcion
if(bin_diabolico(binario) == True):
 print("El numero es del diablo")
else:
    print("el numero es un santo")