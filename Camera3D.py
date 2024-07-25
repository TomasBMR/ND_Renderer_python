import numpy as np
import pygame

from pyEngine.Quadro import Quadro
import Transformacoes as trn

from Objetos import Objeto3D
#from Objetos import ObjetoND


class Camera3D:
    def __init__(self, largura_tela, altura_tela, FoV, tamanho=1, pos=[.0, .0, .0]):
        self.pos = np.array(pos)
        #self.cena = cena

        #Proporcoes da imagem gerada pela camera
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        #Aspect ratio camera
        self.tamanho = tamanho
        self.aspectRatio = self.altura_tela/self.largura_tela

        self.largura_camera = self.tamanho
        self.altura_camera = self.tamanho * self.aspectRatio

        #Direção que a camera aponta
        self.dir = np.array([0, 0, 1])
        self.vet_larg = np.array([1, 0, 0])# Aponta para a direita da camera
        self.vet_alt = np.array([0, 1, 0])# Aponta para cima da camera

        self.znear = 0.01
        self.zfar = 1000
        
        self.FoV = FoV #Em graus
        self.CotFoV = 1/np.tan(self.FoV*0.5*np.pi/180)

        #Matriz projecao perspectiva
        self.matrizPerspectiva = np.array([[self.CotFoV, 0, 0, 0],
                                           [0, self.CotFoV, 0, 0],
                                           [0, 0, (self.znear+self.zfar)/(self.znear-self.zfar), -2*(self.znear*self.zfar)/(self.znear-self.zfar)],
                                           [0 ,0 ,1 ,0]])

        #Matriz que reescala e centraliza a imagem na tela
        self.reescalaeCentraliza = np.dot(trn.MatrixTranslacao([self.largura_tela*0.5, self.altura_tela*0.5, 0]), trn.MatrixEscala([self.largura_tela, self.altura_tela, 1]))

        #Define o estilo de projeção usado
        self.funcProj: callable[[np.ndarray], np.ndarray] = self.ProjPerspectiva

        #Matriz usada na projeção Ortogonal
        self.CalculaMatrizProjOrtogonal()

        self.quadro:Quadro = Quadro(pygame.Surface((largura_tela, altura_tela)))

    def RotVecPos(self, x, y, theta):
        self.pos = np.dot(trn.matrixRotacao(3, x, y, theta),self.pos.transpose()).transpose()
        #self.pos /= np.linalg.norm(self.pos)

    def setEstiloProj(self, estilo:int, tamanho:float):
        """estilo=0 -> projeção ortogonal
           estilo=1 -> projeção perspectiva"""
        self.funcProj = self.ProjOrtogonal if estilo==0 else self.ProjPerspectiva
        self.tamanho = tamanho
        self.largura_camera = self.tamanho
        self.altura_camera = self.tamanho * self.aspectRatio

    def ProjOrtogonal(self, pnts:np.ndarray) -> np.ndarray:
        """Toma pontos em 3D e os projeta no segmento retangular
          do plano dado pelo vetor dir e orientado pelos vetores 
          larg e alt, em seguida, normaliza a projeção à um volume [-1, 1]X[-1, 1]X[-1, 1].
          Faz isso usando as seguintes transformações:
          RxT Translaçao e Rotação para levar os pontos para a base ortonormal dir, vet_larg, vet_alt
          escala os pontos para leva-los ao volume projetivo.
          Essas três operações estão contidas em uma única matriz transformação."""
        
        """transformações em forma mais explicita
        #matRot = np.eye(4)
        #matRot[:3,:3] = np.array([self.vet_larg, self.vet_alt, self.dir])

        ##Matriz que leva para o sistema de coordenadas da camera
        #transformacao = np.dot(matRot, MatrixTranslacao(-self.pos))

        ##Matriz que normaliza os pontos para o volume de projeçao
        #escala_camera = MatrixEscala([1/self.largura_camera, 1/self.altura_camera, 1])
        
        #transformacao = np.dot(escala_camera, transformacao)"""

        pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()

        return np.dot(self.matProjOrtogonal, pntsH)
    
    def ProjPerspectiva(self, pnts:np.ndarray) -> np.ndarray:
        """Transformações ProjOrtogonal
        #matRot = np.eye(4)
        #matRot[:3,:3] = np.array([self.vet_larg, self.vet_alt, self.dir])

        #Matriz que leva para o sistema de coordenadas da camera
        #transformacao = np.dot(matRot, MatrixTranslacao(-self.pos))

        #Matriz que normaliza os pontos para o volume de projeçao
        #escala_camera = MatrixEscala([1/self.largura_camera, 1/self.altura_camera, 1])
        
        #perspectiva_escala = np.dot(self.matrizPerspectiva, escala_camera)

        #transformacao = np.dot(perspectiva_escala, transformacao)

        #pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()"""

        return np.dot(self.matrizPerspectiva, self.ProjOrtogonal(pnts))

    def Draw(self, objs:list[Objeto3D]) -> Quadro:
        img = pygame.Surface((self.largura_tela, self.altura_tela))
        img.fill((1, 0, 0))
        img.set_colorkey((1, 0, 0))
        for obj in objs:
            #Matriz que converte para o tamanho da tela e centraliza nela
            verts = np.dot(self.reescalaeCentraliza, self.funcProj(obj.vertices)).transpose()
            verts = [vert[:3]/vert[3] for vert in verts]

            
            orderedFaces = []
            for i, face in enumerate(obj.faces):
                #if np.dot(obj.getFaceNormal(face), self.dir)<0: #BackfaceCulling
                pnts = [verts[pnt][:2] for pnt in face]
                z = sum([verts[pnt][2] for pnt in face])/len(face)
                orderedFaces.append((pnts, z, i))
            orderedFaces.sort(key=lambda t: t[1])
            for face in orderedFaces:
                pygame.draw.lines(img, obj.corFaces[face[2]], True, face[0], 1)
            """
            for i, face in enumerate(obj.faces):
                pnts = [verts[pnt][:2] for pnt in face]
                pygame.draw.lines(img, obj.corFaces[i], True, pnts, 1)
            """
        self.quadro.setSurf(img)
        return self.quadro
    
    def LookAt(self, alvo, viewUp=[0, 1, 0]):
        """Aponta a camera para a direcao dada e calcula os vetores largura e altura ortogonais a direcao que definem a """
        #Não funciona se a direcao e viewUp forem LD
        direcao = np.array(alvo) - self.pos
        Up = np.array(viewUp)

        if np.linalg.norm(direcao) == 0:
            raise ValueError("Alvo e posicao da camera são iguais")
        
        self.dir = direcao/np.linalg.norm(direcao)
        lado = np.cross(self.dir, Up) #Mudar o nome lado kkkk
        if np.linalg.norm(lado) == 0:
            raise ValueError("Vetor viewUp e direcao linearmente dependentes")
        
        self.vet_larg = lado/np.linalg.norm(lado)
        self.vet_alt = np.cross(self.dir, self.vet_larg)

        self.CalculaMatrizProjOrtogonal()
    
    def CalculaMatrizProjOrtogonal(self):
        #Monta a matriz usada na projeção Ortogonal
        self.matProjOrtogonal = np.eye(4)
        self.matProjOrtogonal[:3,:3] = np.array([self.vet_larg/self.largura_camera, self.vet_alt/self.altura_camera, self.dir])
        self.matProjOrtogonal[0][3] = -np.dot(self.vet_larg, self.pos)
        self.matProjOrtogonal[1][3] = -np.dot(self.vet_alt, self.pos)
        self.matProjOrtogonal[2][3] = -np.dot(self.dir, self.pos)
