import pygame
import math


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Sphere:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.r = radius

    def contains(self, point):
        dis = math.sqrt(pow(point.x - self.x, 2) + pow(point.y - self.y, 2) + pow(point.z - self.z, 2))
        return dis <= self.r


class Box:
    def __init__(self, x, y, z, width, height, depth):
        self.x, self.y, self.z = x, y, z
        self.w = width
        self.h = height
        self.d = depth

        self.left = x - width / 2
        self.right = x + width / 2
        self.top = y - height / 2
        self.bot = y + height / 2
        self.back = z - depth / 2
        self.front = z + depth / 2

    def contains(self, point: Point):
        x, y, z = point.x, point.y, point.z

        return (
                self.left <= x <= self.right and
                self.top <= y <= self.bot and
                self.back <= z <= self.front
        )

    def sphere_collides(self, other: Sphere):
        distancex = abs(other.x - self.x)
        distancey = abs(other.y - self.y)
        distancez = abs(other.z - self.z)

        if distancex > (self.w / 2 + other.r):
            return False
        if distancey > (self.h / 2 + other.r):
            return False
        if distancez > (self.d / 2 + other.r):
            return False

        if distancex <= (self.w / 2):
            return True
        if distancey <= (self.h / 2):
            return True
        if distancez <= (self.d / 2):
            return True

        corner_distance = math.sqrt(
            pow(distancex - self.w / 2, 2) + pow(distancey - self.h / 2, 2) + pow(distancez - self.d / 2, 2))

        return corner_distance <= other.r ** 2

    def collides(self, other):
        if type(other) == Sphere:
            return self.sphere_collides(other)

        return not (
                other.left > self.right or
                other.right < self.left or
                other.top > self.bot or
                other.bot < self.top or
                other.front < self.back or
                other.back > self.front
        )


def get_images():
    # Load Images
    bee = pygame.image.load("bee.png")
    bee_blue = pygame.image.load("bee_blue.png")
    bee_red = pygame.image.load("bee_red.png")
    bee = pygame.transform.scale(bee, (25, 20))
    bee_blue = pygame.transform.scale(bee_blue, (35, 30))
    bee_red = pygame.transform.scale(bee_red, (40, 35))
    bee_rect = bee.get_rect()
    bee_blue_rect = bee_blue.get_rect()
    bee_red_rect = bee_red.get_rect()

    return (bee, bee_rect), (bee_blue, bee_blue_rect), (bee_red, bee_red_rect)


class Octree:
    def __init__(self, limit: Box, capacity):
        self.perimeter = limit
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.children = None

    def insert(self, point: Point):
        if not (self.perimeter.contains(point)):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return

        if not self.divided:
            self.divide()

        for node in self.children:
            node.insert(point)

        return

    def divide(self):
        x, y, z = self.perimeter.x, self.perimeter.y, self.perimeter.z
        w, h, d = self.perimeter.w / 2, self.perimeter.h / 2, self.perimeter.d / 2

        xp, xm = x + w / 2, x - w / 2
        yp, ym = y + h / 2, y - h / 2
        zp, zm = z + d / 2, z - d / 2

        self.children = []

        for i in range(1, 9):
            xval = xm if i % 2 != 0 else xp  # xm -> xp -> xm...
            yval = ym if (i // 2) % 2 != 0 else yp  # ym every 2 times
            zval = zp if i < 5 else zm  # 4 zp, 4 zm

            temp_box = Box(xval, yval, zval, w, h, d)
            self.children.append(Octree(temp_box, self.capacity))

        self.divided = True

    def query(self, query: Box, points_in_range):
        if not self.perimeter.collides(query):
            return points_in_range

        for point in self.points:
            if query.contains(point):
                points_in_range.add(point)

        if self.divided:
            for node in self.children:
                node.query(query, points_in_range)

        return points_in_range

    def show(self, screen, points_in_range, queried_point, dimensions, face_to_show=(1, 1, 1, 1, 1, 1)):
        # Faces of the cube to show
        # Front, right, back, left, top, bottom
        faces = [(0, 0, 0, 1), (1, 0, 1, 2), (2, 0, 0, 1), (0, 1, 1, 2), (1, 1, 0, 2), (2, 1, 0, 2)]

        # Pygames
        blue = (0, 0, 255)
        red = (204, 0, 0)
        white = (255, 255, 255)
        green = (84, 199, 55)

        # Get Images
        normal_bee, blue_bee, red_bee = get_images()

        # Values for the cube of the actual Octree
        x, y, z = self.perimeter.x, self.perimeter.y, self.perimeter.z
        w, h, d = self.perimeter.w, self.perimeter.h, self.perimeter.d

        # Tuple of the values
        trio = (x, y, z)
        ms = (w, h, d)

        for i in range(6):
            modx, mody, index1, index2 = faces[i][0], faces[i][1], faces[i][2], faces[i][3]
            move_in_x = modx * 400
            move_in_y = mody * 400
            d1, d2 = ms[index1], ms[index2]

            # Draw points
            if face_to_show[i]:
                for point in self.points:
                    # Coords of actual point
                    coords = (point.x, point.y, point.z)
                    currx, curry = coords[index1] + move_in_x, coords[index2] + move_in_y

                    # Draw the point, pygame. Blue if in range, else white
                    if point in points_in_range:
                        pygame.draw.circle(screen, blue, (currx, curry), 5)

                        blue_bee[1].center = (currx, curry)
                        screen.blit(blue_bee[0], blue_bee[1])

                    else:
                        pygame.draw.circle(screen, white, (currx, curry), 3)

                # If queried point is present in face, draw
                if self.perimeter.contains(queried_point):
                    three = (queried_point.x, queried_point.y, queried_point.z)
                    cx, cy = three[index1] + move_in_x, three[index2] + move_in_y

                    # Circle for sphere, square for box
                    if type(dimensions) == list:
                        query_dimension_x, query_dimension_y = dimensions[index1], dimensions[index2]
                        query = pygame.Rect((0, 0), (query_dimension_x, query_dimension_y))
                        query.center = (cx, cy)
                        pygame.draw.rect(screen, green, query, 3)
                    else:
                        pygame.draw.circle(screen, green, (cx, cy), dimensions, width=4)

                    # Draw queried point
                    pygame.draw.circle(screen, red, (cx, cy), 5)

                    red_bee[1].center = (cx, cy)
                    screen.blit(red_bee[0], red_bee[1])

                # Draw Rect of side
                query_rect = pygame.Rect((0, 0), (d1, d2))
                query_rect.center = trio[faces[i][2]] + move_in_x, trio[faces[i][3]] + move_in_y
                pygame.draw.rect(screen, white, query_rect, 1)

        if self.divided:
            moves = [
                (0, 0, 1, 1, 1, 0), (0, 1, 1, 0, 1, 0),
                (1, 0, 0, 1, 1, 0), (1, 1, 0, 0, 1, 0),
                (0, 0, 1, 1, 0, 1), (0, 1, 1, 0, 0, 1),
                (1, 0, 0, 1, 0, 1), (1, 1, 0, 0, 0, 1)
            ]
            for i, node in enumerate(self.children):
                node.show(screen, points_in_range, queried_point, dimensions, moves[i])
