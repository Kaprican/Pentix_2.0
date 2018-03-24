#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Графическая версия игры «Pentix»"""

import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from string import ascii_uppercase as alph

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow,
                             QApplication,
                             QMessageBox,
                             QDesktopWidget,
                             QLabel,
                             QWidget,
                             QAction,
                             qApp,
                             QFileDialog,
                             QGridLayout,
                             QLCDNumber, QDialog, QDialogButtonBox)

from Pentominoes import Pentominoes
import board
from game import Game
from windowNext import Next

if sys.version_info < (3, 4):
    print('Use python >= 3.4', file=sys.stderr)
    sys.exit()

try:
    from PyQt5 import QtGui, QtCore, QtWidgets

    QT_VERSION = tuple(map(int, QtCore.QT_VERSION_STR.split('.')))
    if QT_VERSION < (5, 6):
        from PyQt5.QtWebKitWidgets import QWebView
    else:
        from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
except Exception as e:
    print('PyQt5 not found: "{}"'.format(e), file=sys.stderr)
    sys.exit()

__version__ = '2.0'
__author__ = 'Iljushchenko Anastasia'

HIGHSCORE_TABLE_FILE = "highscores.txt"


def parse_data():
    parser = ArgumentParser(prog='pentix.py',
                            description='This is the \"Pentix\"',
                            formatter_class=RawDescriptionHelpFormatter,
                            fromfile_prefix_chars='@',
                            epilog='Author: {}'.format(__author__),
                            argument_default=None)
    parser.add_argument('--version', action='version', version=__version__,
                        help='Help you to find out the version of program')
    return vars(parser.parse_args())


def read_file(filename):
    string = ''
    if filename is None:
        return
    try:
        with open(filename, 'r') as f:
            string = f.read()
    except FileNotFoundError as e:  # IOError:
        sys.stderr.write(str(e))
        exit()
    return convert_str_to_game(string)


def convert_str_to_game(string):
    lines = string.split("\n")
    game = []
    score = 0
    for line in reversed(lines):
        if line.isdigit():
            score = int(line)
            continue
        for char in line:
            if char == '.':
                game.append(0)
            elif alph.index(char) > 12:
                raise ValueError('Wrong symbol')
            else:
                game.append(alph.index(char))
    return game, score


def convert_board_to_str(board, width):
    lines = []
    line = []
    for i, item in enumerate(board):
        if item == Pentominoes.NoShape:
            line.append('.')
        else:
            line.append(alph[item])
        if (i + 1) % width == 0 and i != 0:
            lines.append(''.join(line))
            line = list()
    return '\n'.join(reversed(lines))


def write_to_file(filename, board, score):
    try:
        with open(filename, 'w') as f:
            f.writelines([board, '\n', str(score)])
    except Exception as e:
        sys.stderr.write(e)


def update_records(records, result):
    new_records = check_records(records, result)
    write_records_in_file(new_records)
    return new_records


def check_records(records, result):
    if not records:
        return [result]
    for i, record in enumerate(records):
        if result > record:
            records.insert(i, result)
            break
    return records[:3]


def write_records_in_file(records):
    try:
        with open(HIGHSCORE_TABLE_FILE, 'w') as f:

            f.write('\n'.join(map(str, records)))
    except Exception as e:
        sys.stderr.write(e)


def read_records():
    try:
        with open(HIGHSCORE_TABLE_FILE, 'r') as f:
            string = f.read()
    except FileNotFoundError as e:  # IOError:
        return []
    try:
        list_of_records = convert_str_to_records_list(string)
    except ValueError:
        return []
    return list_of_records


def convert_str_to_records_list(string):
    if not string:
        return []
    lines = string.split("\n")
    try:
        records = list(map(int, lines))
    except ValueError:
        raise ValueError('Invalid arguments')
    return records


class Pentix(QMainWindow):

    def __init__(self):
        super().__init__()

        self.widget = QWidget(self)
        self.game = Game(10, 22)
        self.board = board.Board(self, self.game)
        self.board.resize(self.board.width, self.board.height)
        self.next_figure = Next(self)
        self.highscores = read_records()
        self.statusBar()
        self.menu = self.menuBar()
        self.score = QLabel('Your score')
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.points = QLCDNumber(self)
        self.best_score = QLabel()
        self.set_best_score()

        self.score.setFrameShape(True)
        self.points.setFrameShape(True)
        self.best_score.setFrameShape(True)

        self.create_menu()
        self.set_window()

        self.board.statusbar_msg[str].connect(self.statusBar().showMessage)
        self.statusBar().showMessage('Let\'s start!')

        self.start()

    def set_best_score(self):
        if not self.highscores:
            self.best_score.setText('Best score is 0')
        else:
            self.best_score.setText('Best score is ' + str(self.highscores[0]))

    def set_window(self):
        add1 = self.menu.frameGeometry().height()
        add2 = self.statusBar().frameGeometry().height()
        self.setFixedSize(self.next_figure.width + self.board.width + 15,
                          self.board.height + add1 + add2)
        self.center()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.make_layout())
        # self.make_layout()
        self.setWindowTitle('Pentix')
        self.setWindowIcon(QIcon('images\icon.png'))
        self.show()

    def make_layout(self):

        _layout = QGridLayout()
        _layout.setSpacing(3)
        _layout.addWidget(self.board, 0, 0, 5, 2)
        _layout.addWidget(self.next_figure, 0, 3, 2, 1)
        _layout.addWidget(self.score, 2, 3)
        _layout.addWidget(self.points, 3, 3)
        _layout.addWidget(self.best_score, 4, 3)

        return _layout

    def create_menu(self):

        self.restart_action = QAction(QIcon('images/restart'), 'Rest', self)
        self.restart_action.setShortcut('Ctrl+R')
        self.restart_action.setStatusTip('Restart game')
        self.restart_action.triggered.connect(self.on_restart_click)

        self.score_action = QAction('Highscores', self)
        self.score_action.setShortcut('Ctrl+H')
        self.score_action.setStatusTip('Show highscore table')
        self.score_action.triggered.connect(self.on_score_click)

        self.save_action = QAction(QIcon('images/save.png'), 'Save', self)
        self.save_action.setStatusTip('Save current game')
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.on_save_click)

        self.open_action = QAction(QIcon('images/open.jpg'), 'Open', self)
        self.open_action.setStatusTip('Open saved game')
        self.open_action.setShortcut('Ctrl+O')
        self.open_action.triggered.connect(self.on_open_click)

        self.menu.addAction(self.restart_action)
        self.menu.addAction(self.save_action)
        self.menu.addAction(self.open_action)
        self.menu.addAction(self.score_action)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start(self):
        self.game.start()
        self.board.timer.start(self.game.speed, self.board)

    def on_restart_click(self):
        self.restart()

    def restart(self, game=None, score=0):
        self.board.timer.stop()
        self.highscores = update_records(self.highscores, self.game.score)
        if game is None:
            self.game = Game(10, 22)
        else:
            self.game = Game(10, 22, game, score)
        self.board.restart(self.game)

        self.game.start()
        self.board.timer.start(self.game.speed, self.board)

    def on_score_click(self):
        self.game.pause()
        QMessageBox.about(self,
                          "Highscores",
                          '\n'.join(map(str, self.highscores)))

    def on_save_click(self):
        self.game.pause()
        filename = QFileDialog.getSaveFileName(self, 'Save file', '/saved')[0]
        if filename == '':
            self.statusBar().showMessage('Pause')
            return
        board = convert_board_to_str(self.game.board, self.game.width)
        try:
            write_to_file(filename, board, self.game.score)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
        self.statusBar().showMessage('Pause')

    def on_open_click(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if filename == '':
            return
        try:
            game, score = read_file(filename)
        except ValueError:
            sys.stderr.write('Wrong file. Choose another one')
        except Exception as e:
            sys.stderr.write(str(e))
        self.restart(game, score)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.highscores = update_records(self.highscores, self.game.score)
            event.accept()
        else:
            event.ignore()

    def on_board_signal(self):
        self.points.display(self.game.score)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Pentix()
    sys.exit(app.exec_())
