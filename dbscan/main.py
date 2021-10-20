import numpy as np
import pygame

def dbscan(points_data, eps):
    labels = [0] * len(points_data)
    cluster_idx = 0
    minimum_points = 1
    for i in range(0, len(points_data)):
        if not (labels[i] == 0):
            continue
        near_points = getNear(points_data, i, eps)
        if len(near_points) < minimum_points:
            labels[i] = -1
        else:
            cluster_idx += 1
            labels[i] = cluster_idx
            i = 0
            while i < len(near_points):
                point = near_points[i]
                if labels[point] == -1:
                    labels[point] = cluster_idx

                elif labels[point] == 0:
                    labels[point] = cluster_idx
                    point_near = getNear(points_data, point, eps)
                    if len(point_near) >= minimum_points:
                        near_points = near_points + point_near
                i += 1

    return labels

def getNear(points_data, idx, eps):
    near = []
    for point_idx in range(0, len(points_data)):
        if np.linalg.norm(points_data[idx] - points_data[point_idx]) < eps:
            near.append(point_idx)
    return near

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
points = []
screen.fill((255, 255, 255))

eps = 40

def colors(colors_arr):
    if colors_arr == 1:
        return (255, 0, 0)
    if colors_arr == 2:
        return (0, 255, 0)
    if colors_arr == 3:
        return (0, 0, 255)
    if colors_arr == 4:
        return (0, 0, 0)
    return (125, 125, 125)


def draw(points_arr, clusters):
    for point, cluster in zip(points_arr, clusters):
        color = colors(cluster)
        radius = 10
        pygame.draw.circle(screen, color, point, radius)



done = False
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            points.append(pygame.mouse.get_pos())
            screen.fill((255, 255, 255))
            prediction = dbscan(np.array(points), eps)
            draw(points_arr=points, clusters=prediction)

    pygame.display.update()