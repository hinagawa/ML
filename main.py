import matplotlib.pyplot as plt
import numpy as np


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


def centroids(points, k):
    x_center = np.mean(list(map(lambda p: p.x, points)))
    y_center = np.mean(list(map(lambda p: p.y, points)))
    center = Point(x_center, y_center)
    R = max(map(lambda r: dist(r, center), points))
    centers = []
    for i in range(k):
        x_c = x_center + R * np.cos(2 * np.pi * i / k)
        y_c = y_center + R * np.sin(2 * np.pi * i / k)
        centers.append(Point(x_c, y_c))
    return centers


def new_centroids(points, k):
    centers = []
    cluster_arr = []
    for i in range(k):
        for point in points:
            if (point.cluster == i):
                cluster_arr.append(point)
        x_center = np.mean(list(map(lambda p: p.x, cluster_arr)))
        y_center = np.mean(list(map(lambda p: p.y, cluster_arr)))
        centers.append(Point(x_center, y_center))
        cluster_arr = []
    return centers


def nearest_centroids(points, centroids):
    for point in points:
        min_dist = dist(point, centroids[0])
        point.cluster = 0
        for i in range(len(centroids)):
            temp = dist(point, centroids[i])
            if temp < min_dist:
                min_dist = temp
                point.cluster = i


def color_point(points):
    for point in points:
        if point.cluster == 1:
            plt.scatter(point.x, point.y, c='#84e098')
        elif point.cluster == 2:
            plt.scatter(point.x, point.y, c='#e66ae6')
        elif point.cluster == 3:
            plt.scatter(point.x, point.y, c='#6585c2')
        else:
            plt.scatter(point.x, point.y, c='black')


def equal_centers(prev_center, centers, k):
    for i in range(k):
        if not (prev_center[i].x == centers[i].x and prev_center[i].y == centers[i].y):
            return 0
    return 1


if __name__ == "__main__":
    cluster_1 = []
    cluster_2 = []
    cluster_3 = []
    n = 100  # кол-во тчк
    k = 3  # кол-во кластеров
    points = rand_points(n)
    centers = centroids(points, k)
    prev_center = centers
    plt.scatter(list(map(lambda p: p.x, centers)), list(map(lambda p: p.y, centers)), s=100, marker='*', color='r')
    nearest_centroids(points, centers)
    color_point(points)
    plt.show()
    centers = new_centroids(points, k)
    while not equal_centers(prev_center, centers, k):
        plt.scatter(list(map(lambda p: p.x, centers)), list(map(lambda p: p.y, centers)), s=100, marker='*', color='r')
        nearest_centroids(points, centers)
        color_point(points)
        plt.show()
        prev_center = centers
        centers = new_centroids(points, k)

