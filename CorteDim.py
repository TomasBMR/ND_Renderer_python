import numpy as np

import Transformacoes as trn

from Cameras import CameraND
from Objetos import ObjetoND
from Objetos import Objeto3D


#Recebe um Objeto ND e ger um objeto N-1D
class CorteND:
    def __init__(self, N:int, pos:np.ndarray, base:np.ndarray):
        self.N:int = N

        if pos.shape != (N,): raise ValueError("Posição deve ter formato (N,)")
        self.pos:np.ndarray = pos
        if base.shape != (N-1,N): raise ValueError("Base deve ter formato (N-1, N)")
        self.base:np.ndarray = base

        self.cameraND:CameraND = CameraND(N, pos=self.pos)
        self.cameraND.setEstiloProj(0)

    def CortarObj(self, obj:ObjetoND) -> Objeto3D:
        pntsProjetados = self.Projecao(obj.vertices)
        pnts = []
        #arestas = [-1]
        for face in obj.faces[0]:
            p1, p2 = pntsProjetados[face[0]], pntsProjetados[face[1]]
            if p1[-1] * p2[-1] < 0: #Verifica se a aresta tem um vertice de cada lado do hypervolume
                # Interpolação linear para encontrar interseção da aresta com o hypervolume
                pntInter = p1 + p2 - p1 * (- p1[-1] / (p2[-1] - p1[-1]))
                pnts.append(pntInter)
        return Objeto3D(self.N-1, obj.K, pnts, [[]])
                

            

    def Projecao(self, pnts:np.ndarray) -> np.ndarray:
        vetNormal = trn.VetorOrtogonal(self.base)#Vetor ortogonal a todos os vetores da base | vetor normal ao hypervolume

        baseComNormal = np.concatenate([self.base, vetNormal])

        determinante = np.linalg.det(baseComNormal)

        if not determinante:
            raise ValueError("Base não LD")
        
        pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()

        matProjOrtogonal = np.eye(self.N+1)
        matProjOrtogonal[:self.N, :self.N] = baseComNormal
        np.dot(matProjOrtogonal, trn.MatrixTranslacao(-self.pos))

        return np.dot(matProjOrtogonal, pntsH)[:-1].transpose()


        
        

