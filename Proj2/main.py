# Requirement: Python Interpreter version >= 3.10
# run this file to get the running time for the divide and conquer algorithm
# If you want to check the correctness of the algorithm, you can run the check_consistency function.

import alg
import random
import timeit
import functools
import csv

data_file = "./data/Proj2_data.csv"

def time_alg(N):
    n = 10 ** N
    point_sets = [(0.5,0.5),(5,0.5),(5,5),(0.5,5),(10,10),(10,0.5),(0.5,10),(5,11),(5,12),(5,13),(5,14),(11,11),(11,12)]
    point_sets += generate_points(n)
    alg.conv_hull(point_sets)

# Generate random points within the convex hull of the above points.
# This makes it easier to check the correctness of the algorithm.
# Feel free to change the convex hull points above so that 
# the result will be different.
def generate_points(n):
    points = []
    for i in range(n):
        points.append((random.random()*9.5+0.5,random.random()*9.5+0.5))
    return points


# This funtion is for checking the consistency of the two algorithms
# Bruteforce and Divide & Conquer
# The result may not be perfectly the same,
# because they will treat the points on the same line differently.
# One may include the points on the same line, while the other may not.
def check_consistency(points_sets):
    print(alg.conv_hull(points_sets))
    print(alg.convex_hull(points_sets))

def experiment(max):
    timelist = []
    datafile = open(data_file,"w")
    writer = csv.writer(datafile)
    writer.writerow("e")
    for N in range(1,max):
        partial_time_alg = functools.partial(time_alg,N)
        duration = timeit.timeit(partial_time_alg,number = 1)
        print("When the number of points n is : 10 ** " + str(N) + ", the program takes " + str(duration) + " seconds to get the result.")
        timelist.append(duration)
    writer.writerow(timelist)
    datafile.close()

experiment(9)