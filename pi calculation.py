from mpi4py import MPI
from numba import jit
import math

@jit(nopython=True)
def calc(r,n,s):
    pi = 1.0
    for i in range(r+1, n, s):
        pi = pi*(4.0*i*i)/(4.0*i*i-1)
    return pi    

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    print("Enter repeats n: ")
    n = int(input())
else:
    n = None

t1 = MPI.Wtime()
n = comm.bcast(n, root=0)

Pi = 1.0

Pi = comm.reduce(calc(rank, n, size), op=MPI.PROD, root=0)

if rank == 0:
    Pi = Pi * 2
    t2 = MPI.Wtime()
    print("pi calculation: %.16f" %(Pi))
    print("Time: %.5f" %(t2-t1))
