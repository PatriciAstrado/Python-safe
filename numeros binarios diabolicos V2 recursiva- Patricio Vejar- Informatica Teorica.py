

#---------------------------Cantidad de ceros en binario de N-numero-----------------------------#
def deca_bina (n,c):
    if n >= 1:
        if(n%2 == 0):
            #print("e")
            c+=1
        c+=deca_bina(int(n/2),c)
   
    print(n%2,sep='',end='')
    return c
#------------------------------------------------------------------------------------------------#


#--------------main-------------------------------#
done = 0
while(done == 0):
    try:
        print("Por favor introdusca un numero para convertir a binario y saber su naturaleza")
        valor = int(input())
        done = 1
    except ValueError:
        print("INTRODUSCA UN VALOR VALIDO (numero)")

print("Numero binario:")
num_bin= (deca_bina(valor,0)-1)
print('\n')

if((num_bin%2) != 0):
    print("El numero es Santo!")
else:
    print("El numero es del diablo")