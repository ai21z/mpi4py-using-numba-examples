from random import randint
from mpi4py import MPI
from numba import jit
import numpy

@jit(nopython=True)
def calcCount(r, n, s):
    count = 0
    for i in range(r, n, s):
        if A[i] == x:
            count = count + 1
    return count

N = None
x = None
A = None

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print("Enter size of array: ")
    N = int(input())
    print("Enter the element to search within the array (0 to 9): ")
    x = int(input())
else:
    N = 0
    x = 0

t1 = MPI.Wtime()
N = comm.bcast(N, root=0)
x = comm.bcast(x, root=0)
t2 = MPI.Wtime() 

A = numpy.random.randint(10, size=N)

t3 = MPI.Wtime()
sum = comm.reduce(calcCount(rank, N, size), root=0, op=MPI.SUM)
t4 = MPI.Wtime()
if rank == 0:
    
    # print(A)
    print("%d found %d times in array " % (x, sum))
    print("Elapsed time is: %.6f\n" % (t2-t1+t4-t3))
