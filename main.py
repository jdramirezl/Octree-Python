from Octree import Octree, Box, Point, Sphere
import random
import math
import pygame
import time
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from itertools import product, combinations


def time_info(points, query):
    time_tot = 0
    ind = 0

    print("Octree", query)

    for point in points:
        ind += 1
        print("Iteration:", ind) if ind % 1000 == 0 else None

        x_local, y_local, z_local = point.x, point.y, point.z
        pnts = []
        start = time.time()
        for pnt in points:
            x2, y2, z2 = pnt.x, pnt.y, pnt.z
            difx, dify, difz = abs(
                x_local - x2), abs(y_local - y2), abs(z_local - z2)
            dis = math.sqrt(pow(difx, 2) + pow(dify, 2) + pow(difz, 2))
            if dis > 100:
                continue
            pnts.append(pnt)

        time_tot += time.time() - start

    print("O(n^2)", time_tot)


def info(in_range_local, x_local, y_local, z_local, points_local):
    print()
    print("Points in range of [" + str(x_local) +
          "," + str(y_local) + "," + str(z_local) + "]")
    print("With Oct")
    for pnt in in_range_local:
        x2, y2, z2 = pnt.x, pnt.y, pnt.z
        dis = math.sqrt(pow((x_local - x2), 2) +
                        pow(y_local - y2, 2) + pow(z_local - z2, 2))
        print("\tpoint: [" + str(x2) + "," +
              str(y2) + "," + str(z2) + "]", end=" ")
        print("-> distance:", dis)

    print("With O(n2)")
    for pnt in points_local:
        x2, y2, z2 = pnt.x, pnt.y, pnt.z
        difx, dify, difz = abs(
            x_local - x2), abs(y_local - y2), abs(z_local - z2)
        dis = math.sqrt(pow(difx, 2) + pow(dify, 2) + pow(difz, 2))
        if dis > 100:
            continue
        print("\tpoint: [" + str(x2) + "," +
              str(y2) + "," + str(z2) + "]", end=" ")
        print("-> distance:", dis, "dif in cords:", difx, dify, dify)


def pygame_show(screen, ot: Octree, points_in_range: list, point: Point, query: tuple):
    # Colors
    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (204, 0, 0)
    black = (0, 0, 0)
    green = (65, 199, 52)

    clock = pygame.time.Clock()
    fps = 3

    # Refill Screen
    screen.fill(white)
    canvas = pygame.Rect((0, 0), (1200, 800))
    pygame.draw.rect(screen, black, canvas)

    ot.show(screen, points_in_range, point, query)

    run = True
    counter = 0

    pygame.draw.line(screen, green, (0, 400), (1200, 400), 5)
    pygame.draw.line(screen, green, (400, 0), (400, 800), 5)
    pygame.draw.line(screen, green, (800, 0), (800, 800), 5)

    while run:
        clock.tick(fps)

        pygame.draw.circle(screen, red, (point.x, point.y), 7)
        # pygame.draw.rect(screen, blue, query, 1)

        if counter == 5:
            run = False
        counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pygame.display.update()


def with_visualization():
    # Data for pygame
    pygame.init()
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Data for Octree
    width, height, depth = 4000, 40000, 4000
    is_box_collider = False
    # Range of search (Or radius)
    limit_query = (200, 200, 200) if is_box_collider else 100

    # Create Octree
    limit = Box(0, 0, 0, width, height, depth)
    ot = Octree(limit, 4)

    # Generate Points
    n_of_points = 100
    points = [
        Point(-75.5495499995, 6.33545000045, 1378.75),
        Point(-75.5504500004, 6.33545000045, 1326.07),
        Point(-75.5495499995, 6.33454999955, 1318.85),
        Point(-75.5504500004, 6.33454999955, 1377.63)
    ]

    # Insert points in tree
    for point in points:
        ot.insert(point)

    tot_time, ind = 0, 0
    for point in points:
        ind += 1
        print("Iteration:", ind) if ind % 1000 == 0 else None

        # Data of current point
        x, y, z = point.x, point.y, point.z

        # Create box or sphere range for point
        if is_box_collider:
            query = Box(x, y, z, *limit_query)
        else:
            query = Sphere(x, y, z, limit_query)

        # Get points in range
        start = time.time()
        in_range = ot.query(query, set())
        dif = time.time() - start

        tot_time += dif

        # Get info of Points
        info(in_range, x, y, z, points)

        # Visualize
        pygame_show(screen, ot, in_range, point, limit_query)

    time_info(points, tot_time)
    pygame.quit()


def only_tree():
    # Create Octree
    width, height, depth = 0, 0, 0
    limit = Box(0, 0, 0, width, height, depth)
    ot = Octree(limit, 4)

    # Create query
    box_measures = [0, 0, 0]
    radius = 0
    x, y, z = 0, 0, 0
    box_query = Box(x, y, z, *box_measures)
    sphere_query = Sphere(x, y, z, radius)

    list_of_points_in_range = ot.query(box_query)


if __name__ == "__main__":
    with_visualization()
