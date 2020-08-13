from random import randint
import numpy as np
from mpi4py import MPI
from numba import jit

@jit(nopython = True)
def calcSum(r, n, s):
    sum=0
    for i in range(r, n, s):
        sum += A[i]
    return sum    

@jit(nopython = True)
def calcCount(r, n, s):
    count = 0
    for i in range(r, n, s):
        if avg < A[i]:
            count = count + 1
    return count        

A = None
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
tot_procs = comm.Get_size()

if rank == 0: 
        print("Give size of array N: ")
        N = int(input())      
else: 
        N = 0
        

t1 = MPI.Wtime()
N = comm.bcast(N, root=0)
t2 = MPI.Wtime()

A = np.random.randint(10, size=N)

t3 = MPI.Wtime()
tot_sum = comm.allreduce(calcSum(rank, N, tot_procs), op=MPI.SUM)
avg = tot_sum / N
tot_count = comm.reduce(calcCount(rank, N, tot_procs), root=0, op=MPI.SUM)
t4 = MPI.Wtime()

if rank == 0:
    
    # print(A)
    print("\nAvg is: %.2f \n" %avg)
    print("\nElements bigger than avg: %d\n" %tot_count)
    print("Elapsed time is: %.6f\n" %(t2-t1+t4-t3))
