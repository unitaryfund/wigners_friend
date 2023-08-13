from toqito.matrices import standard_basis
import numpy as np

e0, e1 = standard_basis(2, 1)
phi0 = 1/np.sqrt(2) * (e0 + e1)
phi1 = 1/np.sqrt(2) * (e0 - e1)
sys = 1/np.sqrt(3) * (np.kron(e0, e0) + np.kron(e0, e1) + np.kron(e1, e1))

def obs(v):
    return [e0, e1] if v == 1 else [phi0, phi1]

def prob(proj, state):
    return state.conj().T @ proj @ state

def experiment(a, b, x, y):
    proj_a = np.outer(obs(x)[a], obs(x)[a])
    proj_b = np.outer(obs(y)[b], obs(y)[b])

    proj = np.kron(proj_a, proj_b)

    return prob(proj, sys)

#print(experiment(1,1,2,2))

def phi(x, angles):
    e0, e1 = standard_basis(2)
    return 1/np.sqrt(2) * (e0 + np.exp(1j * angles[x]) * e1)

def psi(y, angles, beta):
    e0, e1 = standard_basis(2)
    return 1/np.sqrt(2) * (e0 + np.exp(1j * (beta - angles[y])) * e1)

def a(x, angles):
    return 2 * np.outer(phi(x, angles), phi(x, angles)) - np.outer(e0, e0) - np.outer(e1, e1)

def b(y, angles, beta):
    return 2 * np.outer(psi(y, angles, beta), psi(y, angles, beta)) - np.outer(e0, e0) - np.outer(e1, e1)


beta = 175
angles = [168, 0, 118]
#z = np.outer(psi(0, angles, beta), psi(0, angles, beta))
#print(z)
#z = phi(0, angles)
#print(z)
#x = b(1, angles, beta)
#print(x.shape)
#print(np.around(b(1, angles, beta), decimals=8))

c = np.exp(1j * (beta))
print(c)

idx = 0
#a0 = a(idx, angles)
#print(np.around(a0, decimals=5))
#c = np.exp(1j * angles[idx])
#
##b0 = b(1, angles, beta)
##print(np.around(b0, decimals=5))
#
#print(c)
#print(c**2 - 1)

b0 = b(idx, angles, beta)
print(np.around(b0, decimals=5))

c = np.exp(1j * (beta - angles[idx]))
print(c)
print(c**2 - 1)