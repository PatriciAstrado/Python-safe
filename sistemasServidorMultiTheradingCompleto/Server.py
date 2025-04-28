import socket
import threading
import sys
import os
import demonio
import datetime

    
        
class ChatServer:
    def __init__(self, host='0.0.0.0', port=55555):
        self.fileSave = open("testFile.txt","w")
        self.fileSave.close()
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(1)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.nicknames = []
        self.activo = True
        terminate = threading.Thread(target = self.terminateSelf)
        terminate.start()
        self.personalDemon = demonio.Demon(self)
        self.managerFromHell = threading.Thread(target= self.personalDemon.start)
        self.managerFromHell.start()
        self.mutex = threading.Lock()

    def privateMessage(self,message,client_requester,client_obj,sender_client=None):
        hora = datetime.datetime.now().strftime('%H:%M:%S')
        hora = f"[{hora}] ".encode('utf-8') + message
        self.fileSave = open("testFile.txt","ab")
        self.fileSec = open("grabarSeguridad.txt","ab")
        self.fileSave.write(message)    
        self.fileSave.write(b'\n')
        self.fileSec.write(hora+client_requester+">>"+client_obj+":"+message)    
        self.fileSec.write(b'\n')
        if client_obj in self.clients:
            if client_requester == None:
                msgSYS = "SYS>>"+message
                client_requester.send(msgSYS)
            if(client_requester != sender_client and client_requester != client_obj):
                client_obj.send(message)
                
    def privateBroadcast(self,message,client_requester,sender_client=None):
        hora = datetime.datetime.now().strftime('%H:%M:%S')
        hora = f"[{hora}] ".encode('utf-8') + message
        self.fileSave = open("testFile.txt","ab")
        self.fileSec = open("grabarSeguridad.txt","ab")
        self.fileSave.write(message)    
        self.fileSave.write(b'\n')
        self.fileSec.write(hora+message)    
        self.fileSec.write(b'\n')
        if client_requester == None:
            msgSYS = "SYS>>"+message
            client_requester.send(msgSYS)
        if(client_requester != sender_client):
            client_requester.send(message)
            
    def saveLogs(self,entry,user="SYS"):        
            logTH = threading.Thread(target = self.saveLogsrun,args=(entry,user,),name="log")
            logTH.start()                
        
    def saveLogsrun(self,entry,user="SYS"):
        with self.mutex:
            try:
                dir_actual = os.path.dirname(__file__)
                base = os.path.dirname(dir_actual)
                dir_logs = os.path.join(base,'logs')
                fecha = str(datetime.date.today())
                entry = str(datetime.datetime.now())+" -- "+user+" -- "+entry+"\n"
                lista = os.scandir(dir_logs)
                usedDate =False
                for objeto in lista:
                    if(objeto.name == fecha):
                        usedDate = True
                        break
                fecha = fecha+".txt"
                if(usedDate):
                    dirdate = os.path.join(dir_logs,fecha)
                    with open(dirdate,'a') as file:
                        file.write(entry)
                        file.close()
                else:
                    dirdate = os.path.join(dir_logs,fecha)
                    with open(dirdate,'w') as file:
                        file.write(entry)
                        file.close()
            except Exception as e:
                print(e)
    def broadcast(self, message, sender_client=None):
        hora = datetime.datetime.now().strftime('%H:%M:%S')
        hora = f"[{hora}] ".encode('utf-8') + message
        self.fileSave = open("testFile.txt","ab")
        self.fileSec = open("grabarSeguridad.txt","ab")
        self.fileSave.write(message)    
        self.fileSave.write(b'\n')
        self.fileSec.write(hora+message)    
        self.fileSec.write(b'\n')
        for client in self.clients:
            
            if(client == None):
                msgSYS = "SYS>>"+message
                client.send(msgSYS)
            if client != sender_client:  # Filtro para no enviar el mensaje al cliente que lo envió
                client.send(message)
                
        self.fileSave.close()
        self.fileSec.close()

    def cargarMensajes(self,sender_client = None):
        self.fileSave = open("testFile.txt",'rb')
        if not self.fileSave.read(1):
            return
        lines = self.fileSave.readlines()
        for line in lines:
            sender_client.send(line)
        self.fileSave.close()


    def handle_client(self, client):
        
        while self.activo:
            try:
                message = client.recv(1024).decode('utf-8')
                
                if message.lower() == 'exit':
                    # Desconectar al cliente si envía "exit"
                    self.disconnect_client(client)
                    break
                elif(message.lower()=="server"):
                    msg = "Datos servidor: "+self.host+" "+str(self.port)
                    self.privateBroadcast(msg.encode('utf-8'),client)
                elif(message.lower()=="files"):
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_lista = os.path.join(base,'entrada')
                    lista = os.scandir(dir_lista)
                    i = 0
                    index = self.clients.index(client)
                    nickname = self.nicknames[index]
                    self.saveLogs(f"El usuario reviso los archivos disponibles en el servidor",nickname)

                    for objeto in lista:
                        
                        if(objeto.is_file):
                            msg = "elemento '%s' .. Nombre:  " %i + objeto.name
                            i+=1
                            self.privateBroadcast(msg.encode('utf-8'),client)
        
                elif(message.lower().split()[0]=="read"):
                    nombre = message.lower().split()[1]
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_lista = os.path.join(base,'entrada')
                    
                    lista = os.scandir(dir_lista)
                    dir_obj = ""
                    
                    for path in lista:                        
                        if(path.name == nombre):
                            dir_obj = os.path.join(dir_lista,path)                        
                            break
                    if(dir_obj != ""):
                        try:
                            with open(dir_obj,'r') as file:
                                
                                msg = file.read()
                                print(msg)
                                self.privateBroadcast(msg.encode('utf-8'),client)
                                index = self.clients.index(client)
                                nickname = self.nicknames[index]
                                self.saveLogs(f"El usuario leyo un archivo del servidor: {nombre}",nickname)

                        except:
                            print("error al enviar contenidos files")
                            msg = "SYS>> A ocurrido un error con la lectura del archivo"
                            self.privateBroadcast(msg.encode('utf-8'),client)
                    else:                        
                        msg = "SYS>> El archivo que nombro no existe en el catalogo del servidor"
                        self.privateBroadcast(msg.encode('utf-8'),client)
                
                elif(message.lower().split()[0]=='procces'):
                    
                    nombre = message.split()[1]
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_lista = os.path.join(base,'entrada')
                    
                    lista = os.scandir(dir_lista)
                    dir_obj = ""
                    
                    for path in lista:                        
                        if(path.name == nombre):                        
                            dir_obj = path.path
                            break
                    if(dir_obj != ""):
                        try:                            
                            dir_procces = os.path.join(base,'procesados')
                            dir_procces = os.path.join(dir_procces,os.path.basename(dir_obj))
                            os.rename(dir_obj, dir_procces)
                            index = self.clients.index(client)
                            nickname = self.nicknames[index]
                            self.saveLogs(f"El usuario movio un archivo a procesados: {nombre}",nickname)
                        except:
                            print("error al mover archivos")
                            msg = "SYS>> A ocurrido un error con el movimiento del archivo"
                            self.privateBroadcast(msg.encode('utf-8'),client)
                    else:
                        msg = "SYS>> El archivo que nombro no existe en el catalogo"
                        self.privateBroadcast(msg.encode('utf-8'),client)
                elif(message.split()[0]=='upload'):
                    print("se recibio un archivo..procesando")
                   
                    partes = message.split()
                    nombreFile = partes[1]
                    tamanoFile = int(partes[2])
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_entrada = os.path.join(base,'entrada')
                    
                    os.makedirs(dir_entrada,exist_ok=True)
                    filedir = os.path.join(dir_entrada,nombreFile)
                    
                    with open(filedir,'wb') as file:
                        bytesEscritos = 0
                        while bytesEscritos < tamanoFile:
                            trozo = client.recv(min(4096,tamanoFile-bytesEscritos))
                            if not trozo:
                                break
                            file.write(trozo)
                            bytesEscritos+= len(trozo)
                    try:
                        msg = "SYS >> archivo subido correctamente"
                        self.privateBroadcast(msg.encode('utf-8'),client)
                        index = self.clients.index(client)
                        nickname = self.nicknames[index]
                        self.saveLogs(f"El usuario a subio un archivo al servidor: {nombreFile}",nickname)
                        print("SYS>> Se a descargado un arhcivo en entrada")
                    except:
                        print(Exception)
                elif message.split()[0] == 'log':
                    index = self.clients.index(client)
                    nickname = self.nicknames[index]                    
                    date = message.split()[1]
                    self.saveLogs(f"El usuario accedio a los logs del dia: {date}",nickname)
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_logs = os.path.join(base,'logs')
                    lista = os.scandir(dir_logs)
                    dir_obj = ""
                    for objeto in lista:
                        if(objeto.name == date):
                            dir_obj = objeto
                            break
                    if(dir_obj != ""):
                        try:
                            path = os.path.join(dir_logs,dir_obj.name)
                            with open(path,'r') as file:
                                msg = file.read()
                                self.privateBroadcast(msg.encode('utf-8'),client)
                        except:
                            msg = "SYS>> A ocurrido un error al abrir el archivo..."
                            self.privateBroadcast(msg.encode('utf-8'),client)
                    else:
                        msg = "SYS>> El archivo que busca no se encuentro..."
                        self.privateBroadcast(msg.encode('utf-8'),client)
                elif message == "help":
                    msg = (
    "╔═══════════════ 📜 LISTA DE COMANDOS DISPONIBLES 📜 ═══════════════╗\n"
    "║ /exit           → Salir del chat y desconectarse del servidor.    ║\n"
    "║ /help           → Mostrar esta lista de comandos.                 ║\n"
    "║ /change         → Cambiar de servidor (introducir nueva IP).      ║\n"
    "║ /ip             → Mostrar tu IP actual de conexión.               ║\n"
    "║ /prt            → Mostrar el puerto actual de conexión.           ║\n"
    "║ /server         → Ver la IP y puerto del servidor conectado.      ║\n"
    "║ /lista          → Listar los archivos disponibles en el servidor. ║\n"
    "║ /leer <archivo> → Leer un archivo del servidor y mostrarlo.       ║\n"
    "║ /procesar <archivo> → Mover un archivo a carpeta 'procesados'.    ║\n"
    "║ /subir <archivo> → Subir un archivo al servidor.                  ║\n"
    "║ /descarga <archivo> → Descargar un archivo del servidor.          ║\n"
    "║ /logs <y-m-d.txt>→ Leer el log del servidor de un día específico. ║\n"
    "╚══════════════════════════════════════════════════════════════════╝"
)
                    self.privateBroadcast(msg.encode('utf-8'),client)
                elif message.split()[0] == "download":
                    nombre = message.split()[1]
                    dir_actual = os.path.dirname(__file__)
                    base = os.path.dirname(dir_actual)
                    dir_lista = os.path.join(base, 'entrada')
                    lista = os.scandir(dir_lista)
                    dir_obj = ""

                    for path in lista:
                        if path.name == nombre:
                            dir_obj = os.path.join(dir_lista, path.name)
                            break

                    if dir_obj != "":
                        try:
                            index = self.clients.index(client)
                            nickname = self.nicknames[index]
                            self.saveLogs(f"El usuario a descargo un archivo del servidor :{nombre}",nickname)
                            file_size = os.path.getsize(dir_obj)
                            
                            aviso = f"prepararenviarserver {nombre} {file_size}"
                            client.send(aviso.encode('utf-8'))

                            
                            with open(dir_obj, 'rb') as file:
                                while True:
                                    data = file.read(4096)
                                    if not data:
                                        break
                                    client.sendall(data)
                            
                            print(f"SYS>> Archivo {nombre} enviado correctamente.")
                        except Exception as e:
                            print(f"Error enviando archivo: {e}")
                    else:
                        error = "SYS>> Archivo no encontrado."
                        client.send(error.encode('utf-8'))
                        
                        
                        
                    
                else:
                    # Si no es "exit", se considera un mensaje normal
                    self.broadcast(message.encode('utf-8'), sender_client=client)
            except:
                # Manejar desconexión inesperada
                self.disconnect_client(client)
                break

    def disconnect_client(self, client):
        """Maneja la desconexión de un cliente."""
        if client in self.clients:
            index = self.clients.index(client)
            nickname = self.nicknames[index]
            self.clients.remove(client)
            self.nicknames.remove(nickname)
            client.close()
            self.broadcast(f'{nickname} ha abandonado el chat!'.encode('utf-8'))
            self.saveLogs("El usuario se desconecto",nickname)
            print(f"Cliente {nickname} desconectado")
    
    
    def terminateSelf(self):
        print("terminate en stanby")
        while self.activo:
            tf = input("")
            if tf.strip().upper() == "/EXIT":
                self.personalDemon.terminateSelf()
                self.saveLogs("El servidor a sido cerrado por sistema")
                msg = "SYS>> El servidor a sido cerrado por la maquina Servidor... Adios"
                self.broadcast(msg.encode('utf-8'))
                
                self.activo = False
                
                for client in self.clients:
                    self.disconnect_client(client)
                self.server.close()
                
                sys.exit()
                
                print("servidor finalizado por comando interno")
            else:
                print("...")
                
                
    def receive(self):
        print("Servidor iniciado y escuchando...")
        print(self.host)
        print(self.port)
        while self.activo:
            try:
                client, address = self.server.accept()
                print(f"Conectado con {str(address)}")
                
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                self.nicknames.append(nickname)
                self.clients.append(client)
                
                print(f"Nickname del cliente es {nickname}!")
                self.saveLogs("El usuario a accedido al servidor",nickname)
                self.broadcast(f"{nickname} se ha unido al chat!".encode('utf-8'))
                client.send('Conectado al servidor!'.encode('utf-8'))
                self.cargarMensajes(sender_client=client)
                
                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except socket.timeout:
                continue
            except OSError:
                break
    
    def start(self):
        self.receive()
        

if __name__ == "__main__":
    server = ChatServer()
    server.start()
