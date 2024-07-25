import numpy as np
from enum import Enum

import Transformacoes as trn

from Objetos import Objeto3D
from Objetos import ObjetoND


class EstiloProjetivo(Enum):
    Ortogonal = 0
    Perspectiva = 1


class CameraND:
    def __init__(self, N:int, tam:float=1, pos_esferica:np.ndarray=None, raio:float=2):#pos:np.ndarray=None):
        self.N = N

        ##Controle Orbital ND, posicao da camera em coordenadas esfericas
        self.raio = raio#np.linalg.norm(self.pos)
        self.esfericas = np.array(pos_esferica) if pos_esferica is not None else np.zeros(N-1)#np.array([0] * (self.N - 2) + [np.pi*0.5]) * self.raio
        self.pos:np.ndarray = None
        self.UpdatePos()
        #print(self.pos)
        """self.pos = np.array(pos) if pos is not None else np.zeros((1, N))
        if len(pos) != N: 
            raise ValueError(f"posição deve ter dimensão {self.N}, tem dimensão {len(pos)}")
        """
        self.tam = tam
        
        self.direcao = - self.pos

        self.FoV = 90
        self.CotFoV = 1/np.tan(self.FoV*0.5*np.pi/180)

        self.matPerspectiva: np.ndarray = np.eye(N+1)*self.CotFoV
        self.matPerspectiva[N-1][N-1] = 1
        self.matPerspectiva[N][N-1] = 1

        #Talvez fazer uma função só para isso??
        self.matPerspectivaEscala = np.dot(trn.MatrixEscala(np.ones(self.N)*self.tam), self.matPerspectiva)

        #self.funcProj:callable[[np.ndarray], np.ndarray] = self.ProjPerspectiva

        self.matProjOrtogonal = None
        self.matProjPerspectiva = None

        self.precisaUpdate = True

        self.estiloProj = EstiloProjetivo.Perspectiva
        self.matProj = self.matProjPerspectiva

        self.LookAt(np.zeros(self.N), recalcular=True)



    def UpdatePos(self):
        """Usa as coordenas esfericas para determinar a posicao da camera"""
        pos = np.ones(self.N)
        for i, coord in enumerate(self.esfericas):
            if i == self.N-2:
                #Ultima coordenada esta em [0, 2pi]
                if coord > 2*np.pi:
                    self.esfericas[i] = ((coord/np.pi) % 2)*np.pi
                elif coord < 0:
                    self.esfericas[i] = ((coord/np.pi) % 2 + 2)*np.pi
            else:
                #Outras estão em [-pi/2, pi/2]
                if coord > np.pi*0.5:
                    self.esfericas[i] = np.pi*0.5
                elif coord < np.pi*-0.5:
                    self.esfericas[i] = np.pi*-0.5

        """if coord > 2*np.pi:
            coord = 0
        elif coord < 0:
            coord = 2*np.pi"""
        #print(self.esfericas)
        for i, coord in enumerate(self.esfericas):
            #print(-1-i)
            pos[-1-i] *= np.sin(coord)
            pos[:-1-i] *= np.cos(coord)
            #print(pos)
        """y = pos[1]
        temp = pos[2:].copy()
        pos[1:-1] = temp
        pos[-1] = y"""
        #print(pos)
        self.pos = pos * self.raio
        #return self.pos

    def RotVecPos(self, x, y, theta):
        #print(self.pos)
        self.pos = np.dot(trn.matrixRotacao(self.N, x, y, theta),self.pos.transpose()).transpose()
        #print(self.pos)
        #self.pos /= np.linalg.norm(self.pos)
        #print(self.LookAtmat[:2])
        #ups = np.dot(matrixRotacao(self.N, x, y, theta), self.LookAtmat[:2].transpose()).transpose()
        #print(ups)
        #self.LookAt((0,0,0,0), ups)

    def setEstiloProj(self, estilo: EstiloProjetivo, tam: float=1):
        """estilo=0 -> projeção ortogonal
           estilo=1 -> projeção perspectiva"""
        self.estiloProj = EstiloProjetivo(estilo)
        #if estilo == EstiloProjetivo.Ortogonal:
        #    self.matProj = self.matProjOrtogonal
        #elif estilo == EstiloProjetivo.Perspectiva:
        #    self.matProj = self.matProjPerspectiva
        
        #Ainda n sei oq fazer com relacao a isso
        #self.tam = tam
        #self.matPerspectiva = np.dot(trn.MatrixEscala(np.ones(self.N)*self.tam), self.matPerspectiva)
    
    def getMatProj(self) -> np.ndarray:
        if self.estiloProj == EstiloProjetivo.Ortogonal:
            return self.matProjOrtogonal
        elif self.estiloProj == EstiloProjetivo.Perspectiva:
            return self.matProjPerspectiva
    
    """
    def ProjOrtogonal(self, pnts:np.ndarray) -> np.ndarray:
        #"Toma pontos em ND e os projeta no hypervolume em (N-1)D"
        pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()

        return np.dot(self.matProjOrtogonal, pntsH)
    
    def ProjPerspectiva(self, pnts:np.ndarray) -> np.ndarray:
        #"Toma pontos em ND e os projeta no hypervolume em (N-1)D com perspectiva"
        pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()

        #Matriz perspectiva composta com viewModel
        perspectivaViewModel = np.dot(self.matPerspectivaEscala, self.matProjOrtogonal)
        return np.dot(perspectivaViewModel, pntsH)  
        #return np.dot(self.matProjPerspectiva, self.ProjOrtogonal(pnts))
    
    def ProjOrtogonalObj(self, objs:list[ObjetoND]) -> Objeto3D:
        return [Objeto3D(self.ProjOrtogonal(obj.vertices)[:-2].transpose(), obj.faces[0]) for obj in objs]
    
    def ProjPerspectivaObj(self, objs:list[ObjetoND]) -> Objeto3D:
        lst = []
        for obj in objs:
            pnts = self.ProjPerspectiva(obj.vertices).transpose()
            pnts = [pnt[:self.N-1]/pnt[self.N] for pnt in pnts]
            lst.append(Objeto3D(pnts, obj.faces[0]))
        return lst
    """


    
    def LookAt(self, alvo:np.ndarray, viewUps:list[np.ndarray]=None, recalcular:bool=False):
        """Aponta a camera para a posição dada e calcula os vetores largura e altura ortogonais a direcao que definem a """
        direcao = np.array(alvo) - self.pos

        if np.linalg.norm(self.direcao - direcao) < 1e-12 and not recalcular:
            return
        
        self.precisaUpdate = True
        self.direcao = direcao

        #Não funciona se a direcao e viewUp forem LD
        if viewUps is None:
            #viewUps = np.eye(self.N)[1:-1]
            viewUps = np.eye(self.N)[2:]

        Ups = np.array(viewUps)

        if np.linalg.norm(direcao) == 0:
            raise ValueError("Posicao e alvo são iguais")
        self.dir = direcao/np.linalg.norm(direcao)

        #Verifica se viewUps e self.dir são linearmente independentes
        mat = np.concatenate([Ups, [self.dir]])
        ortogonal = trn.VetorOrtogonal(mat)

        determinante = np.linalg.det(np.concatenate([mat, [ortogonal]]))
        if not determinante:
            raise ValueError("ViewUps e vetor direcao são linearmente dependentes")
        
        self.LookAtmat = np.zeros((self.N, self.N))

        self.LookAtmat[self.N-1, :] = np.array(self.dir)
        for i in range(self.N-1):
            mat = np.concatenate([Ups[i:], self.LookAtmat[-i-1:]])
            vetOrtogonal = trn.VetorOrtogonal(mat)
            self.LookAtmat[-i-2] = vetOrtogonal/np.linalg.norm(vetOrtogonal)

        
        #self.LookAtmat = np.array(LookAtmat)
        #self.LookAtmat[:self.N, :self.N] = np.array(LookAtmat)

        if self.estiloProj == EstiloProjetivo.Ortogonal:
            self.CalculaMatrizProjOrtogonal()
        else:
            self.CalculaMatrizesProj()
        

    def CalculaMatrizProjOrtogonal(self):
        self.matProjOrtogonal = np.eye(self.N+1)
        self.matProjOrtogonal[:self.N, :self.N] = self.LookAtmat
        self.matProjOrtogonal = np.dot(self.matProjOrtogonal, trn.MatrixTranslacao(-self.pos))
        #self.matProjOrtogonal = np.dot(trn.MatrixEscala(np.ones(self.N)*self.tam), self.matProjOrtogonal)


    def CalculaMatrizesProj(self):
        self.CalculaMatrizProjOrtogonal()
        self.matProjPerspectiva = np.dot(self.matPerspectivaEscala, self.matProjOrtogonal)


class ProjetorND:
    """Projeta objetos de dim N para dimensao 3 usando N-3 cameras"""
    def __init__(self, N:int):
        self.N = N
        self.cameras:list[CameraND] = [CameraND(i, 4, np.array([0]*(i-2)+[np.pi*0.5]), 2)  for i in range(4, N+1)]
        self.cameras.reverse()
        self.precisaUpdate = True
        self.projetados = None

    def setEstiloProj(self, estilo:EstiloProjetivo, tam:float):
        """estilo=0 -> projeção ortogonal
           estilo=1 -> projeção perspectiva"""
        for camera in self.cameras:
            camera.setEstiloProj(estilo, tam)

    def _setprecisaUpdate(self, precisa:bool):
        for camera in self.cameras:
            camera.precisaUpdate = precisa

    def LookAt(self, alvo:np.ndarray=None):
        if alvo is None:
            alvo = np.zeros(self.N)
        for camera in self.cameras:
            camera.LookAt(alvo[:camera.N])

    def ProjetaObjs(self, objs:list[ObjetoND]) -> list[Objeto3D]:
        projetados = []
        #if self.precisaUpdate: #Parar de projetar pnts todo frame!!
        if any(map(lambda cam: cam.precisaUpdate, self.cameras)) or self.projetados is None:
            for obj in objs:
                pnts = obj.vertices
                for camera in self.cameras:
                    pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()
                    verts = np.dot(camera.getMatProj(), pntsH).transpose()
                    #verts = camera.funcProj(obj.vertices).transpose()
                    #verts = np.delete(verts, -2, axis=1)
                    pnts = np.array([vert[:-2]/vert[camera.N] for vert in verts]) #Talvez so dividir tudo e pronto #talvez so cortar a linha "w" e manter H
                projetados.append(Objeto3D(pnts, obj.faces[0], corFaces=obj.corArestas))
            #print("atualizou!")
            #for a #camera.needsupdate = true

            self.projetados = projetados
            self._setprecisaUpdate(False)
            #self.precisaUpdate = False
            return projetados
        return self.projetados

        