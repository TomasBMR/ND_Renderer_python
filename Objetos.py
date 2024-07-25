import numpy as np
import random

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
    def __init__(self, N:int, K:int, vertices:np.ndarray, facesND:list[list[int]], origem=None, corArestas=(12, 34, 160)):
        self.N = N
        self.K = K
        if origem is None:self.origem = np.zeros(N)
        self.vertices = np.array(vertices)
        self.faces = facesND
        self.corArestas = [corArestas]*len(self.faces[0]) #if isinstance(corArestas, tuple) and len(corArestas)==3 else corArestas
        
        for i, face in enumerate(self.faces[0]):
            #print(vertices[face[0]])
            cor = (vertices[face[0]][3] + vertices[face[1]][3]) * 0.5 * 255
            #corw = (vertices[face[0]][3] + vertices[face[1]][3]) * 0.5 * 255
            #corv = (vertices[face[0]][4] + vertices[face[1]][4]) * 0.5 * 255
            #cor = np.clip(cor * np.ones(self.N)*255, 0, 255)[:3]
            cor = np.clip(np.array([cor, -cor, 0]), 0, 255)
            #cor = np.clip(np.array([corw, corw, 0]), 0, 255)
            #print(cor[:3])
            self.corArestas[i] = cor


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
    return ObjetoND(N, K, vrts, facesDims, (12, 34, 56))


def importpol(path: str) -> ObjetoND:
    #limpar essa função, foi feita com mt pressa
    try:
        with open(path, 'r') as file:
            pol = str(file.read())
    except Exception as e:
        print(e)

    linhas = pol.split("\n")

    N, K = tuple(map(int, linhas[0].strip().split()))
    print(N, K)
    
    divs = list(map(int, linhas[1].strip().split()))
    print(divs)

    hypercubos = []
    for i, lin in enumerate(linhas):
        verts = []
        arestas = []
        if len(lin) == 0:
            if linhas[i+1] == "-1": break
            num_verts = int(linhas[i+3])
            for j in range(num_verts):
                verts.append(tuple(map(float, linhas[i+4+j].strip().split()[K+1:])))

            num_arestas = int(linhas[i+3+num_verts+1])
            for j in range(num_arestas):
                arestas.append(list(map(lambda t: int(t)-1, linhas[i+5+num_verts+j].strip().split())))
            #origem = sum([np.array(vert) for vert in verts])/len(verts)
            hypercubos.append([verts, arestas])

            
    #Junta os vários objetos em um só
    
    verts_dic = {}# Chave é o vertice e conteudo é o indice do vertice
    verts = []
    arestas = []

    #print(len(hypercubos))

    num_verts_original = 0

    for hcubo in hypercubos:#random.sample(hypercubos, 5000):
        for vert in hcubo[0]:
            num_verts_original += 1
            if verts_dic.get(vert) is None:
                verts_dic[vert] = len(verts)
                verts.append(np.array(vert))

        ligacoes = [[]]*len(hcubo[1])
        for aresta in hcubo[1]:
            a, b = tuple(aresta)
            a -= 1
            b -= 1
            ligacoes[a].append(b)
            ligacoes[b].append(a)
        visitados = [0]*len(hcubo[1])
        caminho = [0]
        #for i in range(len(hcubo[1])):
            #caminho.append(mat[])
        
        arestas.append((verts_dic[hcubo[0][a]], verts_dic[hcubo[0][b]]))

    print(f"De {num_verts_original} para {len(verts)} vertices")
    print(f"De {len(arestas)} para {len(set(arestas))} arestas")
    #return hypercubos[]
    #hypercubo = hypercubos[0]
    #print(hypercubo)
    #return [ObjetoND(N, K, hypercubo[0], [hypercubo[1]]) for hypercubo in random.sample(hypercubos, 500)]
    #return ObjetoND(N, K, verts, [arestas])
    return ObjetoND(N, K, verts, [list(set(arestas))], (12, 34, 56))


if __name__ == "__main__":
    a = importNDP("Objetos/hypercube5.ndp")
    #print(a.faces[0])
    #a = importpol("Objetos/kleinBottle_4.pol")

    #print(a)

    #print(a.faces[0])

    #print(a.faces[0])
    

    