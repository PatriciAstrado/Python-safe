import os
import threading
import time
import Server
class Demon:
    def __init__(self, server):
        dir_actual = os.path.dirname(__file__)
        base = os.path.dirname(dir_actual)
        self.dir_entrada = os.path.join(base,'entrada')
        self.dir_procces = os.path.join(base,'procesados')
        os.makedirs(self.dir_entrada, exist_ok=True)
        os.makedirs(self.dir_procces, exist_ok=True)
        self.filesInQueque = []
        self.processQueque =[]
        self.encendido = True
        self.mutex = threading.Lock()
        self.serverRef = server
        
    def moverProcess(self,dirname):
        with self.mutex:
            try:
                self.serverRef.saveLogs(f"El demonio empezo a mover {dirname} hacia procesados")
                dir_actual_file = os.path.join(self.dir_entrada,dirname)
                dir_process = os.path.join(self.dir_procces,dirname)
                os.rename(dir_actual_file,dir_process)
                self.filesInQueque.remove(dirname)
                self.serverRef.saveLogs(f"El demonio termino de mover {dirname} hacia procesados")
            except Exception as e:
                print(e)          
                print("error al mover archivos --demon")
    def terminateSelf(self):
        self.encendido = False
    def monitorea(self):
        

        while self.encendido:
            lista = os.scandir(self.dir_entrada)
            for objeto in lista:
                if objeto.is_file() and (objeto.name not in self.filesInQueque):
                    procesar = threading.Thread(target= self.moverProcess,args=(objeto.name,),name=f"{objeto.name}")
                    self.filesInQueque.append(objeto.name)
                    self.processQueque.append(procesar  )
                    procesar.start()
                    
            time.sleep(10)
        
    def start(self):
        self.monitorea()
