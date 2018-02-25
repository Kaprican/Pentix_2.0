#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Pentominoes import Pentominoes
from shapes import Shape


class Game:

    def __init__(self, width, height, board=None, score=0):

        self.width = width
        self.height = height
        self.speed = 500
        self.is_over = False
        self.is_paused = False
        self.next_piece = Shape()
        self.current_piece = Shape()
        self.next_piece.set_random_shape()

        self.score = score
        self.removed_l = 0
        self.added_points = 1
        self.n_lines_to_up_lvl = 2

        self.cur_x = 0
        self.cur_y = 0
        if board is None:
            self.board = []
        else:
            self.board = board
        self.clear_board()

    # определяет тип фигуры в данном блоке
    def shape_at(self, x, y):
        return self.board[(y * self.width) + x]

    def set_shape_at(self, x, y, shape):
        self.board[(y * self.width) + x] = shape

    def start(self):
        if self.is_paused:
            return
        self.clear_board()
        self.new_piece()

    def pause(self):
        self.is_paused = not self.is_paused

    def clear_board(self):
        for i in range(self.height * self.width):
            self.board.append(Pentominoes.NoShape)

    def drop_down(self):
        new_y = self.cur_y
        while new_y > 0:
            if not self.try_move(self.current_piece, self.cur_x, new_y - 1):
                break
            new_y -= 1
        self.piece_dropped()

    def one_line_down(self):
        if not self.try_move(self.current_piece, self.cur_x, self.cur_y - 1):
            self.piece_dropped()

    def piece_dropped(self):
        for i in range(5):
            x = self.cur_x + self.current_piece.x(i)
            y = self.cur_y - self.current_piece.y(i)
            self.set_shape_at(x, y, self.current_piece.shape())
        self.remove_full_lines()
        self.new_piece()

    def remove_full_lines(self):
        num_full_lines = 0
        rows_to_remove = []

        for i in range(self.height):
            n = 0
            for j in range(self.width):
                if not self.shape_at(j, i) == Pentominoes.NoShape:
                    n += 1
            if n == self.width:
                rows_to_remove.append(i)
        rows_to_remove.reverse()

        for m in rows_to_remove:
            for k in range(m, self.height):
                for l in range(self.width):
                        self.set_shape_at(l, k, self.shape_at(l, k + 1))
        num_full_lines += len(rows_to_remove)
        if num_full_lines > 0:
            self.score = self.score + num_full_lines * self.added_points
            self.removed_l += num_full_lines
            self.added_points += self.removed_l // self.n_lines_to_up_lvl
            if self.speed > 200:
                self.speed -= 100 * (self.removed_l // self.n_lines_to_up_lvl)
            self.removed_l %= self.n_lines_to_up_lvl

            # self.is_waiting_after_line = True
            self.current_piece.set_shape(Pentominoes.NoShape)

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Shape()
        self.next_piece.set_random_shape()
        self.cur_x = self.width // 2 + 1
        self.cur_y = self.height - 1 + self.current_piece.min_y()

        if not self.try_move(self.current_piece, self.cur_x, self.cur_y):
            self.current_piece.set_shape(Pentominoes.NoShape)
            self.is_over = True

    def try_move(self, new_piece, new_x, new_y):
        for i in range(5):
            x = new_x + new_piece.x(i)
            y = new_y - new_piece.y(i)
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            if self.shape_at(x, y) != Pentominoes.NoShape:
                return False
            if (y == (self.height // 2 - 1) and
                    self.width // 3 < x < (self.width // 3 * 2)):
                return False

        self.current_piece = new_piece
        self.cur_x = new_x
        self.cur_y = new_y
        return True

    def try_rotate_left(self):
        data_for_rotate = self._check_rotate_left()
        self.current_piece.rotate_left(data_for_rotate)
        return self.current_piece

    def _check_rotate_left(self):
        min_y = self.height
        min_x = self.width
        for i in range(5):
            if self.current_piece.y(i) < min_y:
                min_y = self.current_piece.y(i)
            if self.current_piece.x(i) < min_x:
                min_x = self.current_piece.x(i)

        new_min_y = self.height
        new_min_x = self.width
        new_coords = []
        for i in range(5):
            new_y = min_y - (self.current_piece.x(i) - min_x)
            new_column = self.current_piece.y(i) - min_y + min_x

            new_coords.append([new_column, new_y])

            if new_y < new_min_y:
                new_min_y = new_y
            if new_column < new_min_x:
                new_min_x = new_column

        if new_min_y < min_y:
            for new_coord in new_coords:
                new_coord[1] += min_y - new_min_y
        if new_min_x < min_x:
            for new_coord in new_coords:
                new_coord[0] += min_x - new_min_x

        return new_coords
