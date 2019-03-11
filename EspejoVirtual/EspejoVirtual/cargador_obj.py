import pygame
from OpenGL.GL import *

class OBJ:
    def __init__(self, fichero, girarYZ=False):

        self.vertices = []
        self.normales = []
        self.texturas = []
        self.caras = []

        for linea in open(fichero, "r"):
            if linea.startswith('#'): continue
            trozos = linea.split()
            if not trozos: continue
            if trozos[0] == 'v':
                v = map(float, trozos[1:4])
                for i in range(len(v)):
                    v[i] = v[i]*8
                if girarYZ:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif trozos[0] == 'vn':
                v = map(float, trozos[1:4])
                if girarYZ:
                    v = v[0], v[2], v[1]
                self.normales.append(v)
            elif trozos[0] == 'vt':
                self.texturas.append(map(float, trozos[1:3]))

            elif trozos[0] == 'f':
                cara = []
                texturas = []
                normales = []
                for v in trozos[1:]:
                    w = v.split('/')
                    cara.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texturas.append(int(w[1]))
                    else:
                        texturas.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        normales.append(int(w[2]))
                    else:
                        normales.append(0)
                self.caras.append((cara, normales, texturas))

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for cara in self.caras:
            vertices, normales, texturas = cara

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normales[i] > 0:
                    glNormal3fv(self.normales[normales[i] - 1])
                if texturas[i] > 0:
                    glTexCoord2fv(self.texturas[texturas[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

        print 'Objeto cargado'