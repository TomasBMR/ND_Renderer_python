import numpy as np
import pygame as pg

from Camera3D import Camera3D
from pyEngine.Cena import Cena

#TODO Concertar movimentação da camera no primeiro frame!!
class ControladorOrbital:
    def __init__(self, camera:Camera3D, cena:Cena): #talvez passar a cena e tentar inserir o input na cena por aqui
        self.camera: Camera3D = camera
        self.cena: Cena = cena

        self.alvo = np.array([0, 0, 0])

        self.needsUpdate:bool = False

        self.mousePosInicial = np.array(pg.mouse.get_pos())
        self.vecMouseDrag = np.zeros((2, 1))

        vec = self.alvo - self.camera.pos
        self.raio = np.linalg.norm(vec)
        self.phi = np.pi*0.5
        self.theta = 0

        self.UpdateCameraPos(self.theta, self.phi, self.raio)

    def calcRelativePos(self):
        #coordenadas esfericas
        vec = self.alvo - self.camera.pos
        self.raio = np.linalg.norm(vec)
        self.phi = 0#np.arccos(vec[1]/self.raio)
        self.theta = 0#np.sign(vec[2]/np.arccos(vec[0]/np.linalg.norm(np.array([vec[0], vec[2]]))))

    def InputMouseButtonDown(self):
        #É chamado dentro de pygamemousbuttondow
        self.needsUpdate = True
        self.mousePosInicial = np.array(pg.mouse.get_pos())
        #self.cameraPosInicial = self.camera.pos
        #self.calcRelativePos()

    def InputMouseButtonUp(self):
        #É chamado dentro de pygamemousbuttonup
        self.theta = self.theta + self.vecMouseDrag[1]
        self.phi = self.phi + self.vecMouseDrag[0]
        self.needsUpdate = False

    def UpdateCameraPos(self, theta, phi, raio):
        costheta = np.cos(theta)
        vec = np.array([costheta * np.cos(phi), np.sin(theta), costheta * np.sin(phi)]) * raio
        
        self.camera.pos = vec
        self.camera.LookAt(self.alvo)

    def Update(self, dt):
        if self.needsUpdate:
            mousePosAtual = np.array(pg.mouse.get_pos())
            difPos = mousePosAtual - self.mousePosInicial 
            self.vecMouseDrag = np.divide(difPos, np.array(self.cena.getProporcoes())) * 4

            if self.theta + self.vecMouseDrag[1] > np.pi*0.5:
                self.vecMouseDrag[1] = np.pi*0.5 - self.theta
            elif self.theta + self.vecMouseDrag[1] < - np.pi*0.5:
                self.vecMouseDrag[1] = -np.pi*0.5 - self.theta

            theta = self.theta + self.vecMouseDrag[1]
            phi = self.phi + self.vecMouseDrag[0]
            raio = self.raio

            self.UpdateCameraPos(theta, phi, raio)
            
            

