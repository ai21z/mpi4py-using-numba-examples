import numpy as np
from mpi4py import MPI
from numba import jit

# Uncomment/comment @jit(nopython=True) to add/remove numba python compiler
# @jit(nopython=True)
def addV(z, x, y):
    for i in range(0, part, 1):
        z[i] = x[i] + y[i]
    return z

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
tot_procs = comm.Get_size()

if rank == 0: 
        print("Give size of arrays N: ")
        N = int(input())

        X = np.random.randint(1, 10, size=N, dtype = np.int64)
        Y = np.random.randint(1, 10, size=N, dtype = np.int64)
        Z = np.random.randint(1, size=N, dtype = np.int64)  
        part = N // tot_procs
else: 
        X = None
        Y = None
        Z = None
        N = 0
        part = 0

t1 = MPI.Wtime()
part = comm.bcast(part, root=0)
N = comm.bcast(N, root=0)

Xw = np.zeros(part, dtype = np.int64)
Yw = np.zeros(part, dtype = np.int64)
Zw = np.zeros(part, dtype = np.int64)

comm.Scatter(X, Xw, root=0)
comm.Scatter(Y, Yw, root=0)

comm.Gather(addV(Zw, Xw, Yw),Z,root=0)
t2 = MPI.Wtime()

if rank == 0:

        # print(X)
        # print(Y)
        # print(Z)
        print("Execution time: %.6f\n" %(t2-t1))
        


