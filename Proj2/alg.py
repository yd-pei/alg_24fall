# This file stores the implementation of the divide and conquer algorithm for the convex hull problem.
# You should run main.py to test the correctness and efficiency of the algorithm.
# This file should not be modified.

MAX_cordinate = 100
MIN_cordinate = 0

import math

def conv_hull(points_set:list) -> list:
    '''
    Find the convex hull of the input points set.
    '''
    # sort both Y and X coordinate
    points_set.sort(key = lambda x:x[1])
    points_set.sort(key = lambda x:x[0])
    # Set that stores all of the convex hull(edge)
    # Each element is a point, stored in clockwise order
    # and start from the leftmost point
    # print("Sorted list",points_set)
    return divide_points(points_set)


def slope(point1,point2):
    '''
    Calculate the slope of the line determined by point 1 and 2.
    '''
    return (point2[1]-point1[1])/(point2[0]-point1[0]) if point2[0] != point1[0] else float("inf")

def divide_points(pointset:list):
    '''
    Divide the sorted point set into two part and solve it recursively.
    '''

    # Base case
    if len(pointset) <= 6:
        return convex_hull(pointset)
    
    # Divide
    start = int(len(pointset)/2)
    left_points = []
    right_points = []
    for i in range(start):
        left_points.append(pointset[i])
    for i in range(start,len(pointset)):
        right_points.append(pointset[i])

    # Solve recursively
    left_hull = divide_points(left_points)
    right_hull = divide_points(right_points)
    # print("Left Hull",left_hull)
    # print("Right Hull",right_hull)

    # Merge
    return Merge(left_hull,right_hull)
    # return merge_convex_hulls(left_hull,right_hull)

def Merge(left_hull,right_hull):
    # print("Hull",left_hull,right_hull)
    # Merge two point sets
    n_l,n_r = len(left_hull),len(right_hull)
    # left_R: The leftmost point of the right part of convex hull
    left_R = 0
    # right_L: The rightmost point of the left part of convex hull
    right_L = 0
    # Find right_L
    for i in range(1,n_l):
        if left_hull[i][0] > left_hull[right_L][0]:
            right_L = i

    # print("right_L",right_L)
    # print("left_R",left_R)
    # print("left_hull",left_hull)
    # print("right_hull",right_hull)
    top_tan_left = right_L
    top_tan_right = left_R
    while True:
        change = 0
        # Edge is not upper tangent to the left
        while slope(left_hull[top_tan_left - 1],right_hull[top_tan_right]) < slope(left_hull[top_tan_left],right_hull[top_tan_right]):
            top_tan_left -= 1
            change = 1
        while slope(left_hull[top_tan_left],right_hull[(top_tan_right + 1) % len(right_hull)]) > slope(left_hull[top_tan_left],right_hull[top_tan_right]):
            top_tan_right = (top_tan_right + 1) % len(right_hull)
            change = 1
        if change == 0:
            break
    
    bot_tan_left = right_L
    bot_tan_right = left_R
    while True:
        change = 0
        while slope(left_hull[(bot_tan_left + 1) % len(left_hull)],right_hull[bot_tan_right]) > slope(left_hull[bot_tan_left],right_hull[bot_tan_right]):
            bot_tan_left = (bot_tan_left + 1) % len(left_hull)
            change = 1
        while slope(left_hull[bot_tan_left],right_hull[bot_tan_right -1]) < slope(left_hull[bot_tan_left],right_hull[bot_tan_right]):            
            bot_tan_right -= 1
            change = 1
        if change == 0:
            break
    
    
    # top_tan_left,top_tan_right = find_tangent(left_hull, right_hull, True)
    # bot_tan_left,bot_tan_right = find_tangent(left_hull, right_hull, False)
    if bot_tan_right < 0:
        bot_tan_right = len(right_hull) + bot_tan_right
    if bot_tan_left < 0:
        bot_tan_left = len(left_hull) + bot_tan_left
    if top_tan_left < 0:
        top_tan_left = len(left_hull) + top_tan_left
    if top_tan_right < 0:
        top_tan_right = len(right_hull) + top_tan_right
    # print("tangent")
    # print("top_tan_left",top_tan_left)
    # print("top_tan_right",top_tan_right)
    # print("bot_tan_left",bot_tan_left)
    # print("bot_tan_right",bot_tan_right)
    edges = left_hull[:top_tan_left+1]
    if bot_tan_right == 0:
        edges += right_hull[top_tan_right:] + [right_hull[0]]
    else:
        edges += right_hull[top_tan_right:bot_tan_right+1] 
    edges += (left_hull[bot_tan_left:] if bot_tan_left != 0 else [])    
    # print("Edges",edges)
    return edges


def sort_convex_hull(edges):
    '''
    Sort the convex hull in clockwise order, starting from the leftmost point.
    '''
    def calculate_centroid(points):
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        centroid = (sum(x_coords) / len(points), sum(y_coords) / len(points))
        return centroid

    def calculate_angle(point, centroid):
        return math.atan2(point[1] - centroid[1], point[0] - centroid[0])

    def sort_points_clockwise(points):
        centroid = calculate_centroid(points)
        points.sort(key=lambda p: calculate_angle(p, centroid), reverse=True)
        return points
    # Find the leftmost point
    leftmost_point = min(edges, key=lambda p: p[0])
    # edges.remove(leftmost_point)
    
    # Sort the remaining points in clockwise order
    sorted_points = sort_points_clockwise(edges)
    
    # Ensure the leftmost point is the first in the list
    index = sorted_points.index(leftmost_point)
    sorted_points = sorted_points[index:] + sorted_points[:index]
    
    return sorted_points


def convex_hull(points):
    '''
    Solve the base problem brutely when the number of points is less than 6
    '''
    # Function to determine the orientation of the triplet (p, q, r)
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        elif val > 0:
            return 1  # clockwise
        else:
            return 2  # counterclockwise

    # There must be at least 3 points
    if len(points) < 3:
        return []

    # Initialize Result
    hull = []

    # Find the leftmost point
    l = 0
    for i in range(1, len(points)):
        if points[i][0] < points[l][0]:
            l = i

    p = l
    while True:
        # Add current point to result
        hull.append(points[p])

        # Search for a point 'q' such that orientation(p, x, q) is counterclockwise
        q = (p + 1) % len(points)
        for i in range(len(points)):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        # While we don't come to the first point
        if p == l:
            break
    
    hull = sort_convex_hull(hull)
    return hull