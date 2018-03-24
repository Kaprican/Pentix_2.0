#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest

from Pentominoes import Pentominoes
from game import Game
from shapes import Shape
from pentix import convert_str_to_records_list, convert_str_to_game


class GameTests(unittest.TestCase):

    GAME = Game(10, 15)

    def test_create_game(self):
        self.assertEqual(self.GAME.width, 10)
        self.assertEqual(self.GAME.height, 15)
        self.assertEqual(self.GAME.score, 0)
        self.assertFalse(self.GAME.is_paused)
        self.assertFalse(self.GAME.is_over)
        self.assertEqual(self.GAME.cur_x, 0)
        self.assertEqual(self.GAME.cur_y, 0)

    def test_shape_at(self):
        for i in self.GAME.board:
            self.assertEqual(Pentominoes.NoShape, i)

    def test_set_shape(self):
        game = Game(10, 15)
        game.set_shape_at(0, 1, Pentominoes.NShape)
        self.assertEqual(Pentominoes.NShape, game.shape_at(0, 1))

    def test_pause(self):
        game = Game(10, 15)
        game.pause()
        self.assertTrue(game.is_paused)

    def test_new_piece(self):
        game1 = Game(10, 15)
        game2 = Game(5, 12)
        game3 = Game(15, 20)
        game1.new_piece()
        game2.new_piece()
        game3.new_piece()
        self.assertEqual(game1.cur_x, 6)
        self.assertEqual(game2.cur_x, 3)
        self.assertEqual(game3.cur_x, 8)

    def test_game_over(self):
        game = Game(10, 15)
        for i in range(10):
            game.set_shape_at(i, 14, Pentominoes.NShape)
        game.new_piece()
        self.assertTrue(game.is_over)

    def test_is_square_movable(self):
        game = Game(10, 15)
        game.set_shape_at(5, 10, Pentominoes.NShape)
        self.assertFalse(game.is_square_movable(-1, 5))
        self.assertFalse(game.is_square_movable(1, 15))
        self.assertFalse(game.is_square_movable(1, -15))
        self.assertFalse(game.is_square_movable(20, 15))

        self.assertFalse(game.is_square_movable(5, 10))
        self.assertFalse(game.is_square_movable(4, 6))

        self.assertTrue(game.is_square_movable(2, 3))
        self.assertTrue(game.is_square_movable(1, 6))

    def test_is_on_lath(self):
        game1 = Game(10, 15)
        game2 = Game(15, 12)

        self.assertTrue(game1.is_on_lath(4, 6))
        self.assertTrue(game2.is_on_lath(6, 5))

        self.assertFalse(game1.is_on_lath(4, 4))
        self.assertFalse(game2.is_on_lath(12, 5))

    def test_remove_full_lines(self):
        game = Game(10, 15)
        score = game.score + game.added_points
        for i in range(10):
            game.set_shape_at(i, 0, Pentominoes.NShape)
        game.remove_full_lines()

        board = []
        for i in range(game.height * game.width):
            board.append(Pentominoes.NoShape)

        self.assertTrue(game.score, score)
        self.assertEqual(game.board, board)


class ShapeTests(unittest.TestCase):

    def test_NoShape(self):
        shape = Shape()
        self.assertEqual(Pentominoes.NoShape, shape.shape())

    def test_CShape(self):
        shape = Shape()
        shape.set_shape(Pentominoes.CShape)
        self.assertEqual(Pentominoes.CShape, shape.shape())

    def test_LineShape_at(self):
        shape = Shape()
        shape.set_shape(Pentominoes.LineShape)
        self.assertEqual(Pentominoes.LineShape, shape.shape())

    def test_check_NoShape_x_y(self):
        shape = Shape()
        for i in range(5):
            self.assertEqual(shape.coordsTable[Pentominoes.NoShape][i][0],
                             shape.x(i))
            self.assertEqual(shape.coordsTable[Pentominoes.NoShape][i][1],
                             shape.y(i))

    def test_check_LineShape_x_y(self):
        shape = Shape()
        shape.set_shape(Pentominoes.LineShape)
        for i in range(5):
            self.assertEqual(shape.coordsTable[Pentominoes.LineShape][i][0],
                             shape.x(i))
            self.assertEqual(shape.coordsTable[Pentominoes.LineShape][i][1],
                             shape.y(i))

    def test_set_x(self):
        shape = Shape()
        for i in range(5):
            shape.set_x(i, i)
            self.assertEqual(i, shape.x(i))

    def test_set_y(self):
        shape = Shape()
        for i in range(5):
            shape.set_y(i, i)
            self.assertEqual(i, shape.y(i))

    @staticmethod
    def create_2_shapes():
        shape_z = Shape()
        shape_z.set_shape(Pentominoes.ZShape)
        shape_n = Shape()
        shape_n.set_shape(Pentominoes.NShape)
        return shape_n, shape_z

    def test_min_x(self):
        shape_n, shape_z = self.create_2_shapes()
        z_min_x = shape_z.min_x()
        n_min_x = shape_n.min_x()
        self.assertEqual(-1, z_min_x)
        self.assertEqual(0, n_min_x)

    def test_max_x(self):
        shape_n, shape_z = self.create_2_shapes()
        z_max_x = shape_z.max_x()
        n_max_x = shape_n.max_x()
        self.assertEqual(1, z_max_x)
        self.assertEqual(1, n_max_x)

    def test_min_y(self):
        shape_n, shape_z = self.create_2_shapes()
        z_min_y = shape_z.min_y()
        n_min_y = shape_n.min_y()
        self.assertEqual(-1, z_min_y)
        self.assertEqual(-1, n_min_y)

    def test_max_y(self):
        shape_n, shape_z = self.create_2_shapes()
        z_max_y = shape_z.max_y()
        n_max_y = shape_n.max_y()
        self.assertEqual(1, z_max_y)
        self.assertEqual(2, n_max_y)

    def test_rotate_left(self):
        shape_n, shape_z = self.create_2_shapes()
        rotated_shape_z = shape_z.rotate_left()
        rotated_shape_n = shape_n.rotate_left()
        self.assertEqual(rotated_shape_z.coords, [[-1, -1], [0, 0], [1, 0], [-1, 0], [1, 1]])
        self.assertEqual(rotated_shape_n.coords, [[-2, 1], [0, 0], [1, 0], [0, 1], [-1, 1]])


class ReadInfoAndConvertTests(unittest.TestCase):

    def test_read_and_convert_records(self):
        records = '23\n23\n6'
        list_of_records = convert_str_to_records_list(records)
        self.assertEqual([23, 23, 6], list_of_records)

    def test_read_and_convert_empty_highscores(self):
        records = ''
        list_of_records = convert_str_to_records_list(records)
        self.assertEqual([], list_of_records)

    def test_read_invalid_string(self):
        records = 'sdjcosdc'
        with self.assertRaises(ValueError):
            list_of_records = convert_str_to_records_list(records)

    def test_read_field(self):
        field = '''
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                ..........
                .M........
                .MM.....H.
                ..M..JJ.H.
                .MM.JJJHHH
                LLMLJJHC.E
                6
                '''
        _field = [11, 11, 12, 11, 9, 9, 7, 2, 0, 4,
                  0, 12, 12, 0, 9, 9, 9, 7, 7, 7,
                  0, 0, 12, 0, 0, 9, 9, 0, 7, 0,
                  0, 12, 12, 0, 0, 0, 0, 0, 7, 0,
                  0, 12, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        game, score = convert_str_to_game(field.replace(' ', ''))
        self.assertEqual(_field, game)
        self.assertEqual(6, score)

    def test_read_empty_field(self):
        field = '''..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    ..........
                    0'''
        width = len(field.split('\n')[0])
        height = len(field.split('\n')) - 1
        game, score = convert_str_to_game(field.replace(' ', ''))
        empty_field = [0 for _ in range(width * height)]
        self.assertEqual(empty_field, game)
        self.assertEqual(0, score)


if __name__ == '__main__':
    unittest.main()
