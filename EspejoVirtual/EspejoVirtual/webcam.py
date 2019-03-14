import cv2
from threading import Thread
from imutils import face_utils
import numpy as np
import imutils
import dlib
import math
class Webcam:
   
    def __init__(self):
        self.capturador = cv2.VideoCapture('data/obama.mp4')
        self.capturador.set(3, 640)
        self.capturador.set(4, 480)
        self.modelo = "data/face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.modelo)
        
        while not self.capturador.isOpened():
            print 'Abriendo video...'
        self.imagen = self.capturador.read()[1]
        self.interrumpir = False

        self.angulo_ojos = 0
        self.ojos_detectados = False
        self.coordenadas_gafas = (0,0)

    def iniciar(self):
        Thread(target=self.refrescar, args=()).start()
 
    def euclidean_dist(self,p1,p2):
        return math.sqrt(((p1[0]-p2[0])*(p1[0]-p2[0]))+((p1[1]-p2[1])*(p1[1]-p2[1])))

    def refrescar(self):
        while(not self.interrumpir):
            self.ojos_detectados = False
            self.imagen =imutils.resize(self.capturador.read()[1],width=640) 

            contador=0
            total=0
            (lStart,lEnd) = (42,48)#face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (rStart,rEnd) =(36,42) #face_utils.FACIAL_LANDMARKS_IDX["right_eye"]
            rects = self.detector(self.imagen, 0)

            for rect in rects:
                shape = self.predictor(self.imagen, rect)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(self.imagen, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(self.imagen, [rightEyeHull], -1, (0, 255, 0), 1)
                self.coordenadas_gafas = ((leftEye[0][0]+rightEye[len(rightEye)/2][0])/2, (leftEye[0][1]+rightEye[-1][1])/2)
                cv2.circle(self.imagen, self.coordenadas_gafas, 1, (0,255,0),2)
                self.calcular_angulo_ojos(leftEye[0],rightEye[0])
                self.ojos_detectados = True

    def calcular_angulo_ojos(self, pto_izq, pto_dch):
        pto_aux = pto_izq[0],pto_dch[1]
        cateto_opuesto = self.euclidean_dist(pto_izq,pto_aux)
        hipotenusa = self.euclidean_dist(pto_izq,pto_dch)
        seno_alpha = cateto_opuesto/hipotenusa
        self.angulo_ojos = math.degrees(math.asin(seno_alpha))
        if(pto_izq[1]<pto_dch[1]):
            self.angulo_ojos*=-1
        print str(self.angulo_ojos)
    def obtener_imagen(self):
        return self.imagen

    def terminar(self):
        self.interrumpir = True
        self.capturador.release()
