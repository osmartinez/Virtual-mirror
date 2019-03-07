import cv2
from threading import Thread
   
class Webcam:
   
    def __init__(self):
        self.capturador = cv2.VideoCapture(0)
        self.imagen = self.capturador.read()[1]
        self.interrumpir = False

    def iniciar(self):
        Thread(target=self.refrescar, args=()).start()
   
    def refrescar(self):
        while(not self.interrumpir):
            self.imagen = self.capturador.read()[1]
                   
    def obtener_imagen(self):
        return self.imagen

    def terminar(self):
        self.interrumpir = True
        self.capturador.release()