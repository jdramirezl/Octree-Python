from Octree import Octree, Box, Point, Sphere
import math
import pygame
import time
import os


def save_res(in_range_local, x_local, y_local, z_local, filename):
    destination = './result'
    dir = os.getcwd()
    os.chdir(destination)
    file_name = filename.split("/")[-1]

    # Open file
    f = open(file_name, "a")

    # Process text
    res = ""
    res += "For point: [{}, {}, {}]\n".format(x_local, y_local, z_local)
    res += "Points in range:\n"
    for pnt in in_range_local:
        line = "[{}, {}, {}]\n".format(pnt.x, pnt.y, pnt.z)
        res += line
    res += "Total: {} points\n\n".format(len(in_range_local))

    # Write to file and close
    f.write(res)
    f.close()
    os.chdir(dir)


def main(points, mins, maxs, name):
    print("Alive")
    # Data for Octree
    # abs(maxs[0] - mins[0]), abs(maxs[1] - mins[1]), abs(maxs[2] - mins[2])
    width, height, depth = maxs[0] + 10, maxs[1] + 10, maxs[2] + 10
    width, height, depth = width * 2, height * 2, depth * 2
    # Range of search (Or radius)
    limit_query = 100

    # Create Octree
    limit = Box(0, 0, 0, width, height, depth)
    ot = Octree(limit, 4)

    # Insert points in tree
    for point in points:
        ot.insert(point)

    for point in points:
        # Data of current point
        x, y, z = point.x, point.y, point.z
        query = Sphere(x, y, z, limit_query)

        # Get points in range
        in_range = ot.query(query, set())

        # Get info of Points
        save_res(in_range, x, y, z, name)


def process_points():
    # Generate Points
    directory = './datasets'
    files = [f"{directory}/{file}" for file in os.listdir(directory) if file.endswith(("txt",))]
    print(files)
    for file in files:
        print(file)
        f = open(file)
        f.readline()
        points = []
        min_vals = [math.inf, math.inf, math.inf]
        max_vals = [0, 0, 0]

        # Create files
        dir = os.getcwd()
        os.chdir('./result')
        file_name = file.split("/")[-1]
        direc = open(file_name, "w")
        direc.write("")
        direc.close()
        os.chdir(dir)

        while True:
            line = f.readline()
            if not line:
                break
            x, y, z = map(float, line.split(','))
            min_vals = [min(x, min_vals[0]), min(y, min_vals[1]), min(z, min_vals[2])]
            max_vals = [max(abs(x), max_vals[0]), max(abs(y), max_vals[1]), max(abs(z), max_vals[2])]
            p = Point(x, y, z)
            points.append(p)

        f.close()
        main(points, min_vals, max_vals, file)


if __name__ == "__main__":
    process_points()
