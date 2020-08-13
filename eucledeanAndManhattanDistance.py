#Calculation of eucledean and manhattan distance using mpi4py and numba to achieve better execution times

import numpy as np
from mpi4py import MPI
from numba import jit

@jit(nopython=True)
def ea(r, n, p):
    sum_ea = 0
    for i in range(r, n, p):
        sum_ea += ((X[i]-Y[i])*(X[i]-Y[i]))
    return sum_ea

@jit(nopython=True)
def ma(r, n, p):
    sum_ma = 0
    for i in range(r, n, p):
        if X[i] > Y[i]: 
            sum_ma += (X[i]-Y[i])
        else:
            sum_ma += (Y[i]-X[i]) 
    return sum_ma

X = None
Y = None
N = None

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
total_procs = comm.Get_size()
        
if rank == 0:  
    print("Give N:")
    N = int(input())            

t1 = MPI.Wtime()       
N = comm.bcast(N, root=0)
t2 = MPI.Wtime()
X = np.random.randint(10, size=N)
Y = np.random.randint(100, size=N)

t3 = MPI.Wtime() 
sum = comm.reduce(ea(rank, N, total_procs), root=0, op=MPI.SUM)
man = comm.reduce(ma(rank, N, total_procs), root=0, op=MPI.SUM)
t4 = MPI.Wtime()

if rank == 0:
    ea = np.sqrt(sum)
    
    # print(X)
    # print(Y)
    print("\nEuclidean dist is: %.4f\n" %ea)
    print("\nManhattan dist is: %.4f\n" %man)
    print("Execution time: %.6f\n" %(t2-t1+t4-t3))
        


