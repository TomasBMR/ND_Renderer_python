import numpy as np

class Objeto3D():
    def __init__(self, vertices, faces, origem=(.0, .0, .0), corFaces=(12, 34, 160)):
        self.origem = np.array(origem)
        self.vertices = np.array(vertices)
        self.faces = np.array(faces) #Faces devem ter todas o mesmo numero de vertices
        self.corFaces = [corFaces]*len(self.faces) if isinstance(corFaces, tuple) and len(corFaces)==3 else corFaces

    def getFaceNormal(self, face):
        AB = self.vertices[face[1]] - self.vertices[face[0]]
        AC = self.vertices[face[2]] - self.vertices[face[0]]
        vec = np.cross(AB, AC)
        return vec/np.linalg.norm(vec)
    
    def importObj(self, path):
        pass

    def Update(self, dt):
        pass

class ObjetoND():
    def __init__(self, N:int, K:int, vertices:np.ndarray, facesND:list[list[int]], origem=None):
        self.N = N
        self.K = K
        if origem==None:self.origem = np.zeros(N)
        self.vertices = np.array(vertices)
        self.faces = facesND

    def getFaceNormal(self, face):
        raise "Nao implementei kkk"
        AB = self.vertices[face[1]] - self.vertices[face[0]]
        AC = self.vertices[face[2]] - self.vertices[face[0]]
        vec = np.cross(AB, AC)
        return vec/np.linalg.norm(vec)

    def Update(self, dt):
        pass


def importNDP(path:str) -> ObjetoND:
    try:
        with open(path, 'r') as file:
            ndp = str(file.read())
    except Exception as e:
        print(e)

    ndp = list(filter(len, ndp.split("\n")))
    N, K = tuple(map(int, ndp[0].split(" ")))

    nVrts = int(ndp[1])
    pos = 2
    vrts = list(map(lambda strg: strg.split(" "), ndp[pos:pos+nVrts]))
    vrts = [list(map(float, filter(len, vrt))) for vrt in vrts] #Remove strings vazias e transforma strings em floats
    vrts = np.array(vrts)
    pos += nVrts
    
    facesDims = []
    for _ in range(N):
        nFaces = int(ndp[pos])
        faces = ndp[pos+1:pos+1+nFaces]
        faces = [list(map(int, filter(len, face.split(" ")))) for face in faces]
        #faces = np.array(faces, dtype=int)
        facesDims.append(faces)
        pos+=1+nFaces
    return ObjetoND(N, K, vrts, facesDims, )


if __name__ == "__main__":
    a = importNDP("Objetos/cubeIn4Space.ndp")
    print(a.faces[0])
    

    