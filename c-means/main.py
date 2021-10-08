import matplotlib.pyplot as plt
import numpy as np
import random


class Point:
    def __init__(self, x, y, cluster=-1):
        self.x = x
        self.y = y
        self.cluster = cluster


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def rand_points(n):
    points = []
    for i in range(n):
        point = Point(np.random.randint(0, 100), np.random.randint(0, 100))
        points.append(point)
    return points


def centroids(points, k, n, new_u, m):
    centers = []
    for j in range(k):
        u_sum_x = 0
        u_sum_y = 0
        u_sum_2 = 0
        for i in range(n):
            u_sum_x += pow(new_u[i][j], m) * points[i].x
            u_sum_y += pow(new_u[i][j], m) * points[i].y
            u_sum_2 += pow(new_u[i][j], m)
        center_x = u_sum_x / u_sum_2
        center_y = u_sum_y / u_sum_2
        center = Point(center_x, center_y)
        centers.append(center)
    return centers


def update_u(distance_matrix, n, k, m):
    u = []
    for i in range(n):
        current = []
        for j in range(k):
            d = 0.0
            current.append((1/distance_matrix[i][j]) ** (2 / (m - 1)))
        u.append(current)
    return normalize_u(u, n, k)

def distance_matrix(points, centers, n, k):
    distance_matrix = []
    for i in range(n):
        current = []
        for j in range(k):
            current.append(distanceBetweenPoints(points[i], centers[j]))
        distance_matrix.append(current)
    return distance_matrix


def membership_random(k, n):
    u = np.zeros((n, k))
    for i in range(n):
        row_sum = 0
        for c in range(k):
            if c == k - 1:  # last iteration
                u[i][c] = 1.0 - row_sum
            else:
                rand_num = random.random()
                rand_num = round(rand_num, 2)
                if rand_num + row_sum <= 1:  # to prevent membership sum for a point to be larger than 1.0
                    u[i][c] = rand_num
                    row_sum += u[i][c]
    return u


def distanceBetweenPoints(pointA, pointB):
    return pow(pointA.x - pointB.x, 2) + pow(pointA.y - pointB.y, 2)


def check_condition(new_u, old_u, epsilon):
    for i in range(0, len(new_u)):
        for j in range(0, len(new_u[0])):
            if abs(new_u[i][j] - old_u[i][j]) > epsilon:
                return 0
    return 1  # условие вып-ся

def normalize_u(new_u, n, k):
    sum = []
    for j in range(k):
        col_sum = 0
        for i in range(n):
            col_sum += new_u[i][j]
        sum.append(col_sum)
    for j in range(k):
        for i in range(n):
            new_u[i][j] = new_u[i][j] / sum[j]
    return new_u

if __name__ == "__main__":
    epsilon = 0.01
    n = 4  # кол-во тчк
    k = 3  # кол-во кластеров
    m = 2  # коэфф неопределенности
    points = rand_points(n)
    old_u = membership_random(k, n)
    new_u = [[]]
    centers = centroids(points, k, n, old_u, m)
    dist_matr = distance_matrix(points, centers, n, k)
    new_u = update_u(dist_matr, n, k, m)
    while not check_condition(new_u, old_u, epsilon):
        old_u = new_u
        centers = centroids(points, k, n, old_u, m)
        dist_matr = distance_matrix(points, centers, n, k)
        new_u = update_u(dist_matr, n, k, m)
print('Finished clustering', new_u)
