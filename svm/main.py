import pygame
import numpy as np
from sklearn.datasets import make_blobs
from sklearn import svm


class SVM:
    def __init__(self, c=1.0):
        self.c = c
        self.model = svm.SVC(kernel='linear', C=self.c)

    def fit(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    def calculate_lines(self):
        w = self.model.coef_[0]
        b = self.model.intercept_[0]
        x_points = np.linspace(0, 1024)
        y_points = -(w[0] / w[1]) * x_points - b / w[1]
        main_line_arr = []
        for x, y in zip(x_points, y_points):
            main_line_arr.append([x, y])

        w_hat = self.model.coef_[0] / (np.sqrt(np.sum(self.model.coef_[0] ** 2)))
        margin = 1 / np.sqrt(np.sum(self.model.coef_[0] ** 2))
        dsbp = np.array(list(zip(x_points, y_points)))
        points_of_line_above = dsbp + w_hat * margin
        points_of_line_below = dsbp - w_hat * margin

        return main_line_arr, points_of_line_below, points_of_line_above

pygame.init()
screen = pygame.display.set_mode((1280, 720))
white = (255, 255, 255)
colors = []

def reload_colors():
    global colors
    colors = []
    for i in range(1, 255):
        colors.append(tuple(np.random.choice(range(256), size=3)))
    colors.append((187, 187, 187))
    colors.append((125, 125, 125))

reload_colors()
screen.fill(white)

class Scene:

    def __init__(self):
        self.k = None
        self.curr_cluster = 0
        self.curr_point = None
        self.clusters = []
        self.points = []
        self.still_training = True
        self.init_clusters()
        self.line_arr = []
        self.above_line_arr = []
        self.below_line_arr = []

    def init_clusters(self):
        points, clusters = make_blobs(n_samples=50, centers=2,
                                      cluster_std=30, center_box=(100, 620))
        self.points = list(map(lambda x: [x[0], x[1]], points))
        self.clusters = list(map(lambda x: x + 1, clusters))

    def add_point(self, cluster):
        if self.curr_point is not None:
            self.points.append(self.curr_point)
            self.clusters.append(cluster)
            self.curr_point = None

    @staticmethod
    def draw_circles(points_arr, clusters):
        for point, cluster in zip(points_arr, clusters):
            pygame.draw.circle(screen, colors[int(cluster)], point, 7)

    @staticmethod
    def draw_lines(line_arr, color):
        for line_idx in range(len(line_arr) - 1):
            pygame.draw.line(screen, colors[color], line_arr[line_idx], line_arr[line_idx + 1], 3)

    def start(self):
        self.curr_point = None
        self.still_training = False
        screen.fill(white)

        svm = SVM(c=1.0)
        svm.fit(self.points, self.clusters)
        self.line_arr, self.below_line_arr, self.above_line_arr = svm.calculate_lines()

    def restart(self):
        self.curr_cluster = 0
        self.curr_point = None
        self.points = []
        self.k = None
        self.still_training = True
        self.init_clusters()
        reload_colors()
        self.line_arr = []
        self.above_line_arr = []
        self.below_line_arr = []
        screen.fill(white)

    def run(self):
        q = False

        while not q:
            pygame.time.Clock().tick(30)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    q = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.start()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart()

                if event.type == pygame.KEYDOWN and '1' <= event.unicode <= '2':
                    self.curr_cluster = int(event.unicode)

                left = pygame.mouse.get_pressed()[0]
                right = pygame.mouse.get_pressed()[2]
                if left or right:
                    self.curr_point = pygame.mouse.get_pos()
                    if self.still_training:
                        if self.curr_cluster != 0:
                            if self.curr_point is not None:
                                self.points.append(self.curr_point)
                                self.clusters.append(self.curr_cluster)
                                self.curr_point = None

            font = pygame.font.SysFont('Arial', 24, True)
            if self.still_training:
                surf = font.render('Hello!  S = start, R = restart, Esc = exit',
                                   False, colors[-1])
                screen.blit(surf, (3, 0))
            else:
                surf = font.render('UHUUU! SVM start. R = restart, Esc =  exit.', False, colors[-1])
                screen.blit(surf, (3, 0))

            for i in range(1, 2 + 1):
                surf = font.render(str(i) + ' ', False, colors[i])
                screen.blit(surf, (2 * 24 * (i - 1), 24))
            pygame.display.update()

            if len(self.line_arr) > 0:
                self.draw_lines(self.line_arr, -1)

            if len(self.below_line_arr) > 0:
                self.draw_lines(self.below_line_arr, -2)

            if len(self.above_line_arr) > 0:
                self.draw_lines(self.above_line_arr, -2)

            if len(self.points) > 0:
                for point, cluster in zip(self.points, self.clusters):
                    pygame.draw.circle(screen, colors[int(cluster)], point, 7)


scene = Scene()
scene.run()

