#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Pentominoes import Pentominoes
import random


class Shape(object):

    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0),    (0, 0)),
        ((-1, 0),    (0, 0),     (0, -1),    (0, 1),    (1, 1)),   # F  +
        ((-1, 1),    (-1, 0),    (0, 0),     (1, 0),    (1, 1)),   # C
        ((-2, 0),    (-1, 0),    (0, 0),     (1, 0),    (2, 0)),   # I +
        ((1, -1),    (0, 0),     (0, -1),    (0, 1),    (0, 2)),   # L
        ((-1, 0),    (0, 0),     (1, 0),     (1, 1),    (1, 2)),   # V
        ((1, 0),     (0, 0),     (0, -1),    (0, 1),    (1, 1)),   # P
        ((-1, 1),    (0, 0),     (0, -1),    (0, 1),    (1, 1)),   # T +
        ((-1, 1),    (0, 0),     (0, -1),    (0, 1),    (1, -1)),  # Z
        ((-1, -1),   (0, 0),     (0, -1),    (1, 0),    (1, 1)),   # W +
        ((-1, 0),    (0, 0),     (0, -1),    (0, 1),    (1, 0)),   # X +
        ((-1, 1),    (0, 2),     (0, 1),     (0, 0),    (0, -1)),  # Y
        ((1, 2),     (0, 0),     (0, -1),    (1, 0),    (1, 1))    # N
    )

    def __init__(self):
        self.coords = [[0, 0] for i in range(5)]
        self.piece_shape = Pentominoes.NoShape
        self.set_shape(Pentominoes.NoShape)

    def shape(self):
        return self.piece_shape

    def set_shape(self, shape):
        table = Shape.coordsTable[shape]
        for i in range(5):  # 5 квадратиков
            for j in range(2):  # 2 координаты
                self.coords[i][j] = table[i][j]
        self.piece_shape = shape

    def set_new_shape(self):
        pass

    def set_random_shape(self):
        self.set_shape(random.randint(1, 12))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def set_x(self, index, x):
        self.coords[index][0] = x

    def set_y(self, index, y):
        self.coords[index][1] = y

    def min_x(self):
        m = self.coords[0][0]
        for i in range(5):
            m = min(m, self.coords[i][0])
        return m

    def max_x(self):
        m = self.coords[0][0]
        for i in range(5):
            m = max(m, self.coords[i][0])
        return m

    def min_y(self):
        m = self.coords[0][1]
        for i in range(5):
            m = min(m, self.coords[i][1])
        return m

    def max_y(self):
        m = self.coords[0][1]
        for i in range(5):
            m = max(m, self.coords[i][1])
        return m

    def rotate_left(self):
        if self.piece_shape == Pentominoes.XShape:
            return self
        result = Shape()
        result.piece_shape = self.piece_shape
        for i in range(5):
            result.set_x(i, -self.y(i))
            result.set_y(i, self.x(i))
        return result

    '''
    def rotate_left(self, data_for_rotate):
        if self.piece_shape == Pentominoes.XShape:
            return self
        result = Shape()
        result.piece_shape = self.piece_shape
        if data_for_rotate is not None:
            self.coords = data_for_rotate
        return result

    '''
    def rotate_clockwise(self, shape):
        return [[shape[y][x] for y in range(len(shape))]
                for x in range(len(shape[0]) - 1, -1, -1)]

    def check_collision(self, board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False
