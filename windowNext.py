#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QColor


class Next(QFrame):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setStyleSheet("background-color: rgb(220, 220, 220); "
                           "margin:5px; "
                           "border:1px solid rgb(47, 79, 79); ")
        self.setToolTip("next figure")
        self.square = 20
        self.width = 6 * self.square
        self.height = 6 * self.square
        self.resize(self.width, self.height)
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        self.drawFrame(painter)

        boardTop = (rect.bottom() - rect.top()) // 2

        for i in range(5):
            x = self.parent.game.next_piece.x(i)
            y = self.parent.game.next_piece.y(i)
            new_x = (rect.right() - rect.left()) // 2 + x * self.square
            new_y = boardTop + y * self.square
            self.draw_square(painter,
                             new_x,
                             new_y,
                             self.parent.game.next_piece.shape())

    def draw_square(self, painter, x, y, shape):
        color_table = [0x000000, 0xCC6666, 0x66CC66, 0x0F66CC,
                       0xCCCC66, 0xCC66A4, 0x66CCCC, 0xDAAA00,
                       0x66CDAA, 0x83471D, 0x4682B4, 0x800080,
                       0xF4A460]
        color = QColor(color_table[shape])
        painter.fillRect(x + 1, y + 1, self.square - 2,
                         self.square - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square - 1, x, y)
        painter.drawLine(x, y, x + self.square - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square - 1,
                         x + self.square - 1,
                         y + self.square - 1)
        painter.drawLine(x + self.square - 1,
                         y + self.square - 1,
                         x + self.square - 1,
                         y + 1)
