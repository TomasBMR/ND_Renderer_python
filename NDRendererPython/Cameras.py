import numpy as np

import Transformacoes as trn

from Objetos import Objeto3D
from Objetos import ObjetoND



class CameraND:
    def __init__(self, N:int, tam=1, pos:np.ndarray=None):
        self.N = N
        self.pos = np.array(pos) if pos is not None else np.zeros((1, N))
        if len(pos) != N: 
            raise ValueError(f"posição deve ter dimensão {self.N}, tem dimensão {len(pos)}")
        
        self.tam = tam

        self.LookAt((0, 0, 0, 0))
        #self.LookAtmat = np.eye(N)

        #temp = np.copy(self.LookAtmat[N-1, :])
        #self.LookAtmat[N-1, :] = self.LookAtmat[0, :]
        #self.LookAtmat[0, :] = temp

        self.FoV = 90
        self.CotFoV = 1/np.tan(self.FoV*0.5*np.pi/180)

        self.matProjPerspectiva: np.ndarray = np.eye(N+1)*self.CotFoV
        self.matProjPerspectiva[N-1][N-1] = 1
        self.matProjPerspectiva[N][N-1] = 1

        #Talvez fazer uma função só para isso??
        self.matProjPerspectivaEscala = np.dot(trn.MatrixEscala(np.ones(self.N)*self.tam), self.matProjPerspectiva)

        self.funcProj:callable[[np.ndarray], np.ndarray] = self.ProjPerspectiva

        self.CalculaMatrizProjOrtogonal()

        #self.Camera3D = Camera3D(largura, altura, 3)

    def RotVecPos(self, x, y, theta):
        self.pos = np.dot(trn.matrixRotacao(self.N, x, y, theta),self.pos.transpose()).transpose()
        self.pos /= np.linalg.norm(self.pos)
        #print(self.LookAtmat[:2])
        #ups = np.dot(matrixRotacao(self.N, x, y, theta), self.LookAtmat[:2].transpose()).transpose()
        #print(ups)
        #self.LookAt((0,0,0,0), ups)

    def setEstiloProj(self, estilo: int, tam: float=1):
        """estilo=0 -> projeção ortogonal
           estilo=1 -> projeção perspectiva"""
        self.funcProj = self.ProjOrtogonal if estilo==0 else self.ProjPerspectiva
        self.tam = tam
        self.matProjPerspectiva = np.dot(trn.MatrixEscala(np.ones(self.N)*self.tam), self.matProjPerspectiva)
        
    def ProjOrtogonal(self, pnts:np.ndarray) -> np.ndarray:
        """Toma pontos em ND e os projeta no hypervolume em (N-1)D"""

        pntsH = np.concatenate([pnts, np.ones((len(pnts), 1))], 1).transpose()

        return np.dot(self.matProjOrtogonal, pntsH)
    
    def ProjPerspectiva(self, pnts:np.ndarray) -> np.ndarray:
        """Toma pontos em ND e os projeta no hypervolume em (N-1)D com perspectiva"""
        return np.dot(self.matProjPerspectivaEscala, self.ProjOrtogonal(pnts)) 
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

    def LookAt(self, pos, viewUps:list[np.ndarray]=None):
        """Aponta a camera para a posição dada e calcula os vetores largura e altura ortogonais a direcao que definem a """
        #Não funciona se a direcao e viewUp forem LD
        if viewUps is None:
            viewUps = np.eye(self.N)[1:-1]

        direcao = np.array(pos) - self.pos
        Ups = np.array(viewUps)

        if np.linalg.norm(direcao) == 0: raise ValueError("posicao e direcao são iguais")
        self.dir = direcao/np.linalg.norm(direcao)

        #Verifica se viewUps e self.dir são linearmente independentes
        mat = np.concatenate([Ups, [self.dir]])
        ortogonal = trn.VetorOrtogonal(mat)

        determinante = np.linalg.det(np.concatenate([mat, [ortogonal]]))
        if not determinante:
            raise ValueError("viewUps e vetor direcao são linearmente dependentes")
        
        self.LookAtmat = np.zeros((self.N, self.N))

        self.LookAtmat[self.N-1, :] = np.array(self.dir)
        for i in range(self.N-1):
            mat = np.concatenate([Ups[i:], self.LookAtmat[-i-1:]])
            vetOrtogonal = trn.VetorOrtogonal(mat)
            self.LookAtmat[-i-2] = vetOrtogonal/np.linalg.norm(vetOrtogonal)

        
        #self.LookAtmat = np.array(LookAtmat)
        #self.LookAtmat[:self.N, :self.N] = np.array(LookAtmat)

        self.CalculaMatrizProjOrtogonal()


    def CalculaMatrizProjOrtogonal(self):
        self.matProjOrtogonal = np.eye(self.N+1)
        self.matProjOrtogonal[:self.N, :self.N] = self.LookAtmat
        self.matProjOrtogonal = np.dot(self.matProjOrtogonal, trn.MatrixTranslacao(-self.pos))

class ProjetorND:
    """Projeta objetos de dim N para dimensao 3 usando N-3 cameras"""
    def __init__(self, N:int):
        self.N = N
        self.cameras:list[CameraND] = [CameraND(i, 3, np.array([0]*(i-1) + [-1]))  for i in range(4, N+1)]
        self.cameras.reverse()

    def setEstiloProj(self, estilo:int, tam:float):
        """estilo=0 -> projeção ortogonal
           estilo=1 -> projeção perspectiva"""
        for camera in self.cameras:
            camera.setEstiloProj(estilo, tam)


    def ProjetaObjs(self, objs:list[ObjetoND]) -> list[Objeto3D]:
        projetados = []
        for obj in objs:
            pnts = obj.vertices
            for camera in self.cameras:
                verts = camera.funcProj(obj.vertices).transpose()
                pnts = np.array([vert[:-2]/vert[self.N] for vert in verts])
            projetados.append(Objeto3D(pnts, obj.faces[0]))
        return projetados

        
