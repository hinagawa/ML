from dataclasses import dataclass
import numpy as np
import pygame
import random
from collections import Counter


@dataclass
class Point:
    x: int
    y: int
    cluster: int
    color: str = 'red'


clock = pygame.time.Clock()
FPS = 60

def set_points(numberOfClassEl, numberOfClasses):
    data = []
    colors = ['red', 'green', 'blue']
    for classNum in range(numberOfClasses):
        centerX, centerY = random.randint(50, 550), random.randint(50, 350)
        for rowNum in range(numberOfClassEl):
            data.append(Point(random.gauss(centerX, 20), random.gauss(centerY, 20), classNum, colors[classNum]))
    return data


def dist(a, b):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def nearest_neighbors(points, test_sample, k):
    distances = []
    for i in range(len(points)):
        distances.append((points[i], dist(points[i], test_sample)))
    distances.sort(key=lambda x: x[1])
    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])
    return neighbors


def train(arr, points, test_sample, k):
    neighbors = nearest_neighbors(points, test_sample, k)
    for i in range(k):
        c = 0
        for j in range(i):
            if neighbors[j].color == test_sample.color:
                c = c + 1
        if c >= (i // 2):
            arr[i] = arr[i] + 1

def get_max(arr):
    max = 0
    index = 0
    for i in range(5, len(arr)):
        if arr[i] > max:
            max = arr[i]
            index = i
    return index

def get_colors(points):
    colors = []
    for point in points:
        colors.append(point.color)
    return colors

def predict(arr, points, point):
    maxv = get_max(arr)
    if maxv == 0:
        maxv = 1
    neighbors = nearest_neighbors(points,point, maxv)
    colors = get_colors(neighbors)
    c = Counter(colors)
    value = max(c.values())
    return list(c.keys())[list(c.values()).index(value)]


def draw_pygame():
    screen = pygame.display.set_mode((600, 400))
    play = True
    curr_point = None
    while play:
        clock.tick(FPS)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.draw.circle(screen, 'grey', event.pos, 5)
                    x, y = pygame.mouse.get_pos()
                    curr_point = Point(x, y, 0, 'grey')
                if event.button == 3:
                    x, y = pygame.mouse.get_pos()
                    color = predict(arr, points, Point(x, y, 0, 'pink'))
                    pygame.draw.circle(screen, color, event.pos, 5)
                    points.append(Point(x, y, 0, color))
                    curr_point = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    curr_point.color = 'red'
                if event.key == pygame.K_2:
                    curr_point.color = 'green'
                if event.key == pygame.K_3:
                    curr_point.color = 'blue'
                if curr_point is not None:
                    train(arr, points, curr_point, k)
                    points.append(curr_point)
                    curr_point = None
        for point in points:
            pygame.draw.circle(screen, point.color, (point.x, point.y), 5)
        if curr_point is not None:
            pygame.draw.circle(screen, 'grey', (curr_point.x, curr_point.y), 5)
        pygame.display.update()


if __name__ == '__main__':
    pnt, clst = 10, 3
    k = 15
    arr = [0] * k
    points = set_points(pnt, clst)
    draw_pygame()
