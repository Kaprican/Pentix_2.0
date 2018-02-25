#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QBasicTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame
from Pentominoes import Pentominoes
import pentix


class Board(QFrame):

    statusbar_msg = pyqtSignal(str)

    def __init__(self, parent, game):
        super().__init__()

        self.setStyleSheet("background-color: rgb(220, 220, 220); "
                           "margin:5px; "
                           "border:1px solid rgb(47, 79, 79); ")
        self.timer = QBasicTimer()
        self.game = game
        self.square = 20
        self.width = self.game.width * self.square
        self.height = self.game.height * self.square
        self.parent = parent
        self.resize(self.width, self.height)

        self.setFocusPolicy(Qt.StrongFocus)

    def restart(self, game):
        self.game = game
        self.update()

    def square_width(self):
        return self.square

    def square_height(self):
        return self.square

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.game.is_paused:
                self.timer.stop()
            elif self.game.is_over:
                self.statusbar_msg.emit('Game over')
                self.timer.stop()
                self.parent.highscores = \
                    pentix.update_records(self.parent.highscores,
                                          self.parent.game.score)
            else:
                self.timer.start(self.game.speed, self)
                self.game.one_line_down()
        self.parent.on_board_signal()
        self.parent.next_figure.update()
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_P:
            self.game.pause()
            if self.game.is_paused:
                self.statusbar_msg.emit('Pause')
            else:
                self.timer.start(self.game.speed, self)
                self.statusbar_msg.emit('Play')
            return

        if self.game.is_paused \
                or self.game.current_piece.shape() == Pentominoes.NoShape:
            return
        elif key == Qt.Key_Left:
            self.game.try_move(self.game.current_piece,
                               self.game.cur_x - 1,
                               self.game.cur_y)
        elif key == Qt.Key_Right:
            self.game.try_move(self.game.current_piece,
                               self.game.cur_x + 1,
                               self.game.cur_y)
        elif key == Qt.Key_Down:
            self.game.one_line_down()
        elif key == Qt.Key_Up:
            self.game.try_move(self.game.current_piece.rotate_left(),
                               self.game.cur_x,
                               self.game.cur_y)
        elif key == Qt.Key_Space:
            self.game.drop_down()
        self.parent.next_figure.update()
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()
        self.drawFrame(painter)

        boardTop = rect.bottom() - self.game.height * self.square_height()
        boardTop1 = rect.bottom()
        boardLeft = rect.left()
        boardRight = rect.right()
        boardBottom = rect.top()

        for i in range(self.game.height):
            for j in range(self.game.width):
                shape = self.game.shape_at(j, self.game.height - i - 1)

                if shape != Pentominoes.NoShape:
                    self.draw_square(painter,
                                     rect.left() + j * self.square_width(),
                                     boardTop + i * self.square_height(),
                                     shape)

        if self.game.current_piece.shape() != Pentominoes.NoShape:

            for i in range(5):

                x = self.game.cur_x + self.game.current_piece.x(i)
                y = self.game.cur_y - self.game.current_piece.y(i)
                self.draw_square(painter,
                                 rect.left() + x * self.square_width(),
                                 boardTop + (self.game.height - y - 1)
                                 * self.square_height(),
                                 self.game.current_piece.shape())
        self.draw_line(painter)

    def draw_line(self, painter):
        rect = self.contentsRect()
        y = rect.bottom() - self.game.height // 2 * self.square
        x1 = rect.left() + (self.game.width // 3 + 1) * self.square
        x2 = rect.left() + self.game.width // 3 * 2 * self.square
        painter.drawLine(x1, y, x2, y)

    def draw_square(self, painter, x, y, shape):
        color_table = [0x000000, 0xCC6666, 0x66CC66, 0x0F66CC,
                       0xCCCC66, 0xCC66A4, 0x66CCCC, 0xDAAA00,
                       0x66CDAA, 0x83471D, 0x4682B4, 0x800080,
                       0xF4A460]
        color = QColor(color_table[shape])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1,
                         x + self.square_width() - 1,
                         y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1,
                         y + self.square_height() - 1,
                         x + self.square_width() - 1,
                         y + 1)
