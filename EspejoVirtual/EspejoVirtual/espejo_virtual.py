from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np
from webcam import Webcam
from cargador_obj import OBJ
import time
import pygame

class EspejoVirtual:
    def __init__(self):
        self.cam = Webcam()
        self.textura_cam = 0
        self.ancho = 640
        self.alto = 480
        self.obj= None
        self.x =-5
        self.y = 0.1

    def iniciar_opengl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        self.textura_cam = glGenTextures(1)
        self.obj = OBJ('data/gafas4.obj',True)

    def iniciar_opencv(self):
        self.cam.iniciar()

    def pintar_escena(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, self.ancho, self.alto)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.ancho, 0.0, self.alto, 0.1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

        self.pintar_video(self.cam.obtener_imagen())
        if True or self.cam.ojos_detectados:
            self.pintar_objeto()

        glutSwapBuffers()

    def pintar_video(self,imagen):
        pillow_img = Image.fromarray(imagen) # giro la imagen
        ancho = pillow_img.size[0]
        alto = pillow_img.size[1]

        bytes_img = pillow_img.tobytes('raw','BGRX',0,-1)
        
        glEnable(GL_TEXTURE_2D)
        glColor3fv((1,1,1))

        glBindTexture(GL_TEXTURE_2D, self.textura_cam)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ancho, alto, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes_img)

        glBindTexture(GL_TEXTURE_2D, self.textura_cam)
        
        glTranslatef(0.0,0.0,-99)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0);
        glVertex3f(0, self.alto, 0.0)
        #glVertex3f(-4.0, -3.0, 0.0)

        glTexCoord2f(1.0, 1.0);
        glVertex3f( self.ancho, self.alto, 0.0)
        #glVertex3f( 4.0, -3.0, 0.0)

        glTexCoord2f(1.0, 0.0);
        glVertex3f( self.ancho,  0, 0.0)
        #glVertex3f( 4.0,  3.0, 0.0)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(0,  0, 0.0)
        #glVertex3f(-4.0,  3.0, 0.0)

        glEnd()

    def draw_rect(self,x, y, width, height):
        glDisable(GL_TEXTURE_2D)
        glTranslatef(0,0,1)

        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y) 
        glVertex2f(x + width, y + height)                 
        glVertex2f(x, y + height)                          
        glEnd()                        


    def pintar_objeto(self):
        glDisable(GL_TEXTURE_2D)
        glLoadIdentity()
        glTranslatef(self.cam.coordenadas_gafas[0],415-self.cam.coordenadas_gafas[1],0)

        glColor3fv((1, 1, 1))
        
        ##glRectf(100, 100, 0, 0.5)
        #glRotate(90, 0, 1, 0)
        glRotate(180, 1, 0, 0)
        glRotate(180,0,0,1)

        glRotate(self.cam.angulo_ojos,0,0,1)

        glCallList(self.obj.gl_list)
        
    def comenzar(self):
        glutInit()

        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.ancho, self.alto)
        glutCreateWindow('Espejo virtual')
        glutDisplayFunc(self.pintar_escena)
        glutIdleFunc(self.pintar_escena)

        self.iniciar_opengl()
        self.iniciar_opencv()

        glutMainLoop()

espejo = EspejoVirtual()
espejo.comenzar()