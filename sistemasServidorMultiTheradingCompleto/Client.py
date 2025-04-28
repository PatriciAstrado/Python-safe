import socket
import os
import threading
import re   
class ChatClient:
    def __init__(self, host='127.0.0.1', port=55555):
        
        self.estadoConexion = 0
        while(self.estadoConexion==0):
            try:
                self.host = host
                self.port = port
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((host, port))
                self.nickname = None
                self.estadoConexion = 1
                self.preparing = False
                self.file = None
                self.expectedSize = 0
                self.recibidoByte = 0
                self.nombreFile = ""
            except:
                print("SYS>> error, no se a detectado servidor o la IP que esta introducida no es valida")
                inpt = input("SYS>> desea conectar a una ip distinta a "+host+"?       Y/n:  ")
                if(inpt == "Y"):
                    ip =     input("..")
                    if(self.valIP(ip)):
                        host = ip
                    else:
                        print("IP invalida")
                elif(inpt == "n"):
                    return
    def valIP(self, ip):
        forma = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not forma.match(ip):
            return 0
        partes = ip.split('.')
        return all(0 <= int(p) <= 255 for p in partes)

    def serverConect(self,port=55555):
        serverDefault = "127.0.0.1"
        self.client.close()
        while True:
            ipIn = input(f"SYS>> Ingrese la ip del servidor que quiere acceder (ENTER para servidor default):   ").strip()
            if(ipIn == ''):
                self.host = serverDefault
            elif(self.valIP(ipIn)):
                self.host = ipIn
            else:
                print("SYS>> ip invalida")
                continue
            self.estadoConexion = 0
            while self.estadoConexion == 0:
                try:
                    #self.port = port
                    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.client.connect((self.host, self.port))
                    self.nickname = None
                    self.estadoConexion = 1
                    print(f'SYS>> Ingresado exitosamente a server '+ipIn)
                    self.endThreads()
                    self.start()
                    return
                except:
                    print("SYS>> Error al ingresar al servidor")
                    s = input("SYS>> desea ingresar una nueva IP?      Y/n:  ")
                    if(s != "Y"):
                        print("Cerrando conexiones....")
                        return
                

    def receive(self):
        while not self.endSignal:
            try:
                data =self.client.recv(1024)
                if not data:
                    print("SYS>> servidor cerrado por host")
                    self.endSignal = 1
                    self.client.close()
                    break

                if not self.preparing:
                    message = data.decode('utf-8')

                    if message.startswith("prepararenviarserver"):
                        partes = message.split()
                        self.filename = partes[1]
                        self.expected_size = int(partes[2])
                        self.received_bytes = 0

                        dir_actual = os.getcwd()
                        os.makedirs(dir_actual, exist_ok=True)
                        self.file = open(os.path.join(dir_actual, self.filename), 'wb')
                        self.preparing = True
                        print(f"SYS>> Preparándose para recibir archivo {self.filename} de {self.expected_size} bytes.")

                    else:
                        print(message)

                else:
                    
                    self.file.write(data)
                    self.received_bytes += len(data)

                    if self.received_bytes >= self.expected_size:
                        self.file.close()
                        self.preparing = False
                        print(f"SYS>> Archivo {self.filename} recibido completamente.")
            except Exception as e:
                print("Error! Conexión cerrada. error:: "+str(e))
                self.endSignal = 1
                self.client.close()
                break
    
    def write(self):
        while not self.endSignal :
            
            message = input("")
            if(len(message)<= 0):
                continue
            if message.lower() == '/exit':
                # Enviar "exit" al servidor indicando que el cliente se desconecta
                self.client.send("exit".encode('utf-8'))
                print("SYS>> Desconectando...")
                self.endSignal = 1
                self.client.close()
                break
            elif message.lower() == '/help':  #TODO
                self.client.send("help".encode('utf-8'))                
            elif message.lower() == "/change":
                print("SYS>> cambiando servidor...")
                self.endSignal = 1
                self.client.close()
                self.serverConect()
                
                break
            elif message.lower() == '/ip':
                print("SYS>> Su ip es::  "+self.host)
            elif message.lower() == '/prt':
                print("SYS>> Su puerto es::  "+str(self.client.getsockname()[1]))
            elif message.lower() == '/server':
                self.client.send("server".encode('utf-8'))
            elif message.lower() == '/lista':
                self.client.send("files".encode('utf-8'))
            elif message.lower().split()[0] == '/leer':
                nombre = message.lower().split()[1]
                self.client.send(("read "+nombre).encode('utf-8'))
            elif message.lower().split()[0] == '/procesar':
                nombre = message.lower().split()[1]
                self.client.send(("procces "+nombre).encode('utf-8'))
            elif message.lower().split()[0] == '/subir':
                nombre = message.split()[1]
                dir_actual = os.getcwd()
                
                #base = os.path.dirname(dir_actual)
                lista = os.scandir(dir_actual)
                
                file_obj = ""                
                for objeto in lista:                       
                    if(objeto.name == nombre):                        
                        file_obj = os.path.join(dir_actual,nombre)                        
                        break
                if(file_obj != ""):
                    try:
                        bytesize = os.path.getsize(file_obj)
                        #avisamos que los siguientes datos de este cliente son los bytes
                        self.client.send(f"upload {nombre} {bytesize}".encode('utf-8'))
                        with open(file_obj,'rb') as file:
                            bytesEnviar = file.read()
                            self.client.sendall(bytesEnviar)
                            
                    except Exception as e:
                        print(f"SYS >> El archiv {nombre} no a sido cargado/enviado::  {e}")
                else:
                    print("SYS >> El archivo no a sido encontrado en la carpeta")
            elif message.lower().split()[0] == '/descarga': 
                nombre = message.split()[1]
                self.client.send(f"download {nombre}".encode('utf-8'))
            elif message.lower().split()[0] == '/logs':
                date = message.split()[1]
                self.client.send(f"log {date}".encode('utf-8'))
            else:
                # Enviar mensaje normal al servidor
                self.client.send(f'{self.nickname}: {message}'.encode('utf-8'))
    def endThreads(self):
        try:
            if(hasattr(self, 'receive_thread') and self.receive_thread.is_alive()):
                self.endSignal = 1
                self.receive_thread.join()
            if(hasattr(self, 'write_thread') and self.write_thread.is_alive()):
                self.endSignal = 1
                self.write_thread.join()
            self.endSignal = 0 # si señan final es 1, verdadero, entonces en "recieve" terminara antes de recibir cualquier error    
        except:
            print("aqui")
    def start(self):
        if(self.estadoConexion==0): return
        ##self.endThreads()
        self.nickname = input("Elige un nickname: ")
        self.endSignal = 0 # si señan final es 1, verdadero, entonces en "recieve" terminara antes de recibir cualquier error
        
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

if __name__ == "__main__":
    client = ChatClient()
    client.start()