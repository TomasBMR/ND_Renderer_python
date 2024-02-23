import numpy as np
import pygame

from pyEngine.Cena import Cena
from pyEngine.Quadro import Quadro

from Camera3D import Camera3D
from Objetos import Objeto3D

class Bussola3D(Cena):
    def __init__(self, largura: int, altura: int,  pos: tuple, direc: np.ndarray):
        super().__init__(largura, altura)
        self.direc = direc

        self.camera = Camera3D(largura, altura, 90, 1.2, -2*direc)
        self.camera.setEstiloProj(0, 3)
        self.camera.LookAt((0,0,0))

        self.verts = np.zeros((4, 3))
        self.verts[1:, :3] = np.eye(3)

        circ = [[np.cos(2*np.pi*t/30), 0, np.sin(2*np.pi*t/30)] for t in range(30)]
        self.verts = np.concatenate([self.verts, np.array(circ)])

        self.arestas = [[0,1],
                        [0,2],
                        [0,3]]
        
        self.arestas += [[4 + i, 4 + i + 1] for i in range(29)] + [[33, 4]]
        
        self.corArestas = [(255, 0, 0),
                           (0, 255, 0),
                           (0, 0, 255)] + [(125, 125, 125)]*30

        self.bussola = Objeto3D(self.verts, self.arestas, corFaces=self.corArestas)

        self.vec4D = Objeto3D(np.zeros((2, 3)), [[0,1]], corFaces=(1,0,0))

        self.objs = [self.bussola, self.vec4D]
        self.pos = pos
        self.quadro = Quadro(pygame.Surface((largura, altura)), pos=self.pos)

    def setDiretores(self, direc:np.ndarray):
        self.direc = direc

    def Update(self, direc:np.ndarray, vec4d:np.ndarray):
        self.camera.pos=-2*direc
        self.camera.LookAt((0, 0, 0))
        self.vec4D.vertices[1] = vec4d

    def Draw(self) -> Quadro:
        img = pygame.Surface((self.largura_tela, self.altura_tela))
        img.set_colorkey((0, 0, 0))
        self.quadro.setSurf(self.camera.Draw(self.objs).surf)
        pygame.draw.rect(self.quadro.surf, (200, 200, 200), (0, 0, self.largura_tela, self.altura_tela), 1)
        #pygame.draw.circle(self.quadro.surf, (200, 200, 200), (self.largura_tela*0.5, self.altura_tela*0.5), self.largura_tela*0.5, 1)
        return self.quadro