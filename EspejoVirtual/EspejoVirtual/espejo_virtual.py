from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
from PIL import Image
import numpy as np
from webcam import Webcam

class EspejoVirtual:
    def __init__(self):
        self.cam = Webcam()
        self.textura_cam = 0
        self.ancho = 640
        self.alto = 480

    def iniciar_opengl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(33.7, 1.3, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        self.textura_cam = glGenTextures(1)

    def iniciar_opencv(self):
        self.cam.iniciar()

    def pintar_escena(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.pintar_video(self.cam.obtener_imagen())
        self.pintar_objeto()

        glutSwapBuffers()

    def pintar_video(self,imagen):
        pillow_img = Image.fromarray(cv2.flip(imagen,0)) # giro la imagen
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
        
        glTranslatef(0.0,0.0,-10.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 1.0); glVertex3f( 4.0, -3.0, 0.0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 4.0,  3.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.0,  3.0, 0.0)
        glEnd()

    def pintar_objeto(self):
        glDisable(GL_TEXTURE_2D)
        glTranslatef(0,0,2)
        glColor3fv((1, 0, 0))
        glRectf(-1, 1, 0, 0.5)

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