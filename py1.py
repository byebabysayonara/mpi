from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

n = 10**7 # number of points to generate
points_per_process = n // size # number of points for each process to calculate

if rank == 0:
    start_time = time.time()
    points = [(random.uniform(0,1), random.uniform(0,1)) for i in range(n)]
    for i in range(1, size):
        comm.send(points[i*points_per_process: (i+1)*points_per_process], dest=i)
else:
    points = comm.recv(source=0)

count = 0
for point in points:
    if point[0]**2 + point[1]**2 <= 1:
        count += 1

pi = 4 * count / len(points)

if rank == 0:
    pi_values = [pi]
    pi_times = [time.time() - start_time]
    for i in range(1, size):
        pi_values.append(comm.recv(source=i))
        pi_times.append(comm.recv(source=i))
    for i in range(size):
        print("Process", i, "calculated pi as", pi_values[i], "in", pi_times[i], "seconds.")
else:
    comm.send(pi, dest=0)
    comm.send(time.time() - start_time, dest=0)