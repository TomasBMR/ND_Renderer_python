import numpy as np
from GUI import GUI

# "Produto vetorial" de N-1 vetores em RN

v1 = np.array([1, 0, 0, 0, 0])
v2 = np.array([1, 1, 0, 0, 0])
v3 = np.array([1, 1, 1, 0, 0])
v4 = np.array([1, 1, 1, 1, 0])


mat = np.array([v1, v2, v3, v4])

v5 = [(-1)**i*np.linalg.det(np.delete(mat, i, 1)) for i in range(mat.shape[1])]

#print(v5)

print(np.linalg.det(np.array([v1, v2, v3, v4, v5])))


"""try:
    sol = np.linalg.solve(np.array([v1, v2, v3, v4, v5]), np.zeros((5, 1)))
except np.linalg.LinAlgError as err:
    if 'Singular matrix' in str(err):
        raise "vetores LD"
    else:
        raise"""

#print(all(sol == 0))

