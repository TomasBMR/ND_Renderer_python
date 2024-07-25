import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

def importNDP(path, novo):
    try:
        with open(path, 'r') as file:
            ndp = str(file.read())
    except Exception as e:
        raise e

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
        facesDims.append(np.array(faces, dtype="int"))
        pos+=1+nFaces

    print(f"N:{N},")
    novo.write(f"N:{N},\n")
    print(f"K:{K},")
    novo.write(f"K:{K},\n")
    print(f"vertices:")
    novo.write(f"vertices:")
    print("[", end="")
    novo.write("[")
    for vrt in vrts:
        print("[", end="")
        novo.write("[")
        for i, cord in enumerate(vrt):
            print(f"{cord}", end="")
            novo.write(f"{cord}")
            if i<K-1:
                print(", ", end="")
                novo.write(", ")
        print("],")
        novo.write("],\n")
    print("],")
    novo.write("],")

    #for dim in facesDims:
    #    print(f"faces: {dim}")
    print(f"faces:")
    novo.write("faces:")
    """    print("[", end="")
    for face in facesDims:
        print("[", end="")
        for i in face:
            print(i, ",")
        print("],")
    print("]")"""
    print(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))
    novo.write(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))


def importpol(path: str, novo):
    #limpar essa função, foi feita com mt pressa
    try:
        with open(path, 'r') as file:
            pol = str(file.read())
    except Exception as e:
        print(e)

    linhas = pol.split("\n")

    N, K = tuple(map(int, linhas[0].strip().split()))
    
    divs = list(map(int, linhas[1].strip().split()))

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

    print(f"N:{N},")
    novo.write(f"N:{N},\n")
    print(f"K:{K},")
    novo.write(f"K:{K},\n")
    print(f"vertices:")
    novo.write(f"vertices:")
    print("[", end="")
    novo.write("[")
    for vrt in verts:
        print("[", end="")
        novo.write("[")
        for i, cord in enumerate(vrt):
            print(f"{cord}", end="")
            novo.write(f"{cord}")
            if i<N-1:
                print(", ", end="")
                novo.write(", ")
        print("],")
        novo.write("],\n")
    print("],")
    novo.write("],")

    #for dim in facesDims:
    #    print(f"faces: {dim}")
    print(f"faces:")
    novo.write("faces:")
    print(f"[{list(map(list, arestas))}]".replace("],", "],\n"))
    novo.write(f"[{list(map(list, arestas))}]".replace("],", "],\n"))
    #print(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))
    #novo.write(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))


    #return hypercubos[]
    #hypercubo = hypercubos[0]
    #print(hypercubo)
    #return [ObjetoND(N, K, hypercubo[0], [hypercubo[1]]) for hypercubo in random.sample(hypercubos, 500)]
    #return ObjetoND(N, K, verts, [arestas])



def importpol_otimizado(path: str, novo):
    #limpar essa função, foi feita com mt pressa
    try:
        with open(path, 'r') as file:
            pol = str(file.read())
    except Exception as e:
        print(e)

    linhas = pol.split("\n")

    N, K = tuple(map(int, linhas[0].strip().split()))
    
    divs = list(map(int, linhas[1].strip().split()))

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
            #verts.append(np.array(vert))
            if verts_dic.get(vert) is None:
                verts_dic[vert] = len(verts)
                verts.append(np.array(vert))

        if hcubo == hypercubos[0]:
            print(hcubo[1])
        for aresta in hcubo[1]:
            a, b = tuple(aresta)
            #arestas.append((num_verts_original+a, num_verts_original+b))
            c, d = (verts_dic[hcubo[0][a]], verts_dic[hcubo[0][b]])
            if c>d:
                c,d = d,c
            arestas.append((c, d))
        num_verts_original += len(hcubo[0])
    arestas = list(set(arestas))
    print(f"De {num_verts_original} para {len(verts)} vertices")
    print(f"De {len(arestas)} para {len(set(arestas))} arestas")

    ###print(f"N:{N},")
    novo.write(f"N:{N},\n")
    ###print(f"K:{K},")
    novo.write(f"K:{K},\n")
    ###print(f"vertices:")
    novo.write(f"vertices:")
    ###print("[", end="")
    novo.write("[")
    for vrt in verts:
        ###print("[", end="")
        novo.write("[")
        for i, cord in enumerate(vrt):
            ###print(f"{cord}", end="")
            novo.write(f"{cord}")
            if i<N-1:
                ###print(", ", end="")
                novo.write(", ")
        ###print("],")
        novo.write("],\n")
    ###print("],")
    novo.write("],\n")

    #for dim in facesDims:
    #    print(f"faces: {dim}")
    ###print(f"faces:")
    novo.write("faces:")
    ###print(f"[{list(map(list, arestas))}]".replace("],", "],\n"))
    novo.write(f"[{list(map(list, arestas))}]".replace("],", "],\n"))
    #print(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))
    #novo.write(f"{facesDims}".replace("array", "").replace("(", "\n").replace(")", ""))

def importpol_n_otimizado(path: str, novo):
    #limpar essa função, foi feita com mt pressa
    print("importando de forma nao otimizada")
    try:
        with open(path, 'r') as file:
            pol = str(file.read())
    except Exception as e:
        print(e)

    linhas = pol.split("\n")

    N, K = tuple(map(int, linhas[0].strip().split()))
    
    divs = list(map(int, linhas[1].strip().split()))

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
            verts.append(np.array(vert))
            """if verts_dic.get(vert) is None:
                verts_dic[vert] = len(verts)
                verts.append(np.array(vert))"""

        if hcubo == hypercubos[0]:
            print(hcubo[1])
        for aresta in hcubo[1]:
            a, b = tuple(aresta)
            #if a>b:
                #a, b = b, a
            arestas.append((num_verts_original+a, num_verts_original+b))
            
        num_verts_original += len(hcubo[0])

    print(f"De {num_verts_original} para {len(verts)} vertices")
    print(f"De {len(arestas)} para {len(set(arestas))} arestas")

    ###print(f"N:{N},")
    novo.write(f"N:{N},\n")
    ###print(f"K:{K},")
    novo.write(f"K:{K},\n")
    ###print(f"vertices:")
    novo.write(f"vertices:")
    ###print("[", end="")
    novo.write("[")
    for vrt in verts:
        ###print("[", end="")
        novo.write("[")
        for i, cord in enumerate(vrt):
            ###print(f"{cord}", end="")
            novo.write(f"{cord}")
            if i<N-1:
                ###print(", ", end="")
                novo.write(", ")
        ###print("],")
        novo.write("],\n")
    ###print("],")
    novo.write("],\n")

    #for dim in facesDims:
    #    print(f"faces: {dim}")
    ###print(f"faces:")
    novo.write("faces:")
    ###print(f"[{list(map(list, arestas))}]".replace("],", "],\n"))
    novo.write(f"[{list(map(list, arestas))}]".replace("],", "],\n"))

    #return hypercubos[]
    #hypercubo = hypercubos[0]
    #print(hypercubo)
    #return [ObjetoND(N, K, hypercubo[0], [hypercubo[1]]) for hypercubo in random.sample(hypercubos, 500)]
    #return ObjetoND(N, K, verts, [arestas])


#file = open("600_celljson", "w")
#importNDP("Objetos/600_cell.ndp", file)

#file = open("kleinBottle_otimizado.txt", "w")
#importpol_otimizado("Objetos/kleinBottle_4.pol", file)

#file = open("kleinBottle_n_otimizado.txt", "w")
#importpol_n_otimizado("Objetos/kleinBottle_4.pol", file)

file = open("impr_reorder_otimizado.txt", "w")
importpol_otimizado("Objetos/impr_reorder.pol", file)

#file = open("impr_reorder.txt", "w")
#importpol("Objetos/impr_reorder.pol", file)

