import numpy as np

def MatrixTranslacao(vec: np.ndarray) -> np.ndarray:
    """Gera a matrix Translaçao"""
    dim = len(vec)
    mat = np.eye(dim+1)
    mat[:dim, dim] = vec
    return mat

def MatrixEscala(vec: np.ndarray) -> np.ndarray:
    """Gera a matrix Escala"""
    dim = len(vec)
    mat = np.eye(dim+1) 
    mat[:dim, :dim] = np.diag(vec)
    return mat

def matrixRotacao(N:int, x:int, y:int, theta:float) -> np.ndarray:
    """Gera a matrix Rotação"""
    mat=np.eye(N)
    mat[x][x] = np.cos(theta)
    mat[y][y] = np.cos(theta)
    mat[x][y] = np.sin(theta)
    mat[y][x] = -np.sin(theta)
    return mat


def VetorOrtogonal(mat:np.ndarray) -> np.ndarray:
    """Receba uma matriz N-1xN
       Retorna um vetor em RN ortogonal as N-1 linhas da matriz.
       Gera resultado errado se as linhas da matriz forem LD"""
    if mat.shape[1]-mat.shape[0] != 1: 
        raise ValueError(f"matriz deve ser N-1xN, mas eh {mat.shape[0]}x{mat.shape[1]}")
    return np.array([(-1)**i*np.linalg.det(np.delete(mat, i, 1)) for i in range(mat.shape[1])])


if __name__ == "__main__":
    print(MatrixTranslacao(np.array([1, 2, 3])))