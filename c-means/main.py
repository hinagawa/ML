import numpy as np


def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prob = []


def kf(cluster_num, centers, point, m):
    result = 0
    dist_cluster = dist(centers[cluster_num].x, centers[cluster_num].y, point.x, point.y)
    for center in centers:
        result += pow(dist_cluster / dist(center.x, center.y, point.x, point.y), 2 / (1 - m))
    return result


def norm_kf(prob):
    sum = 0
    for probability in prob:
        sum += probability
    for i in range(0, len(prob)):
        prob[i] /= sum


def calc_decisive(points, centers):
    res_func = 0
    for point in points:
        prob = point.prob
        for i in range(0, len(prob)):
            res_func += prob[i] * dist(point.x, point.y, centers[i].x, centers[i].y)
    return res_func


def calc_c(k, m, points):
    result = []
    for i in range(0, k):
        chis_x = 0
        chis_y = 0
        znam_x = 0
        znam_y = 0

        for point in points:
            chis_x += pow(point.prob[i], m) * point.x
            znam_x += pow(point.prob[i], m)

            chis_y += pow(point.prob[i], m) * point.y
            znam_y += pow(point.prob[i], m)

        x_cluster_c = chis_x / znam_x
        y_cluster_c = chis_y / znam_y

        result.append(Point(x_cluster_c, y_cluster_c))

    return result


def init_c(points, k, x_center, y_center):
    R = 0
    n = len(points)
    for i in range(0, n):
        r = dist(x_center, y_center, points[i].x, points[i].y)
        if r > R:
            R = r
    x_cc = [R * np.cos(2 * np.pi * i / k) + x_center for i in range(k)]
    y_cc = [R * np.sin(2 * np.pi * i / k) + y_center for i in range(k)]
    result = []
    for i in range(0, k):
        result.append(Point(x_cc[i], y_cc[i]))
    return result


def init_in_cluster(points, k):
    for point in points:
        for i in range(0, k):
            point.prob.append(0)


EPSILON = 0.15


def c_means(points, n, k):
    begin = True
    init_in_cluster(points, k)
    x_center = np.mean(list(map(lambda e: e.x, points)))
    y_center = np.mean(list(map(lambda e: e.y, points)))
    decision = 1
    prev_decision = 0
    while abs(prev_decision - decision) > EPSILON:
        prev_decision = decision
        if begin:
            centers = init_c(points, k, x_center, y_center)
            begin = False
        else:
            centers = calc_c(k, n, points)
        for point in points:
            for i in range(0, len(centers)):
                point.prob[i] = kf(i, centers, point, n)
            norm_kf(point.prob)
        decision = calc_decisive(points, centers)


n, k = 20, 4
points = [Point(np.random.randint(1, 100), np.random.randint(1, 100)) for i in range(n)]
c_means(points, 1.5, k)
for point in points:
    print(str(point.x) + ":" + str(point.y) + " " + str(point.prob))