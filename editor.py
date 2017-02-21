#!/usr/bin/env python

"""
editor.py - A level editor for a MODE 2 vertical scrolling game.

Copyright (C) 2017 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import Tools.graphics
import Tools.levels

__version__ = "0.1"

default_palette = [
    (0,0,0), (255,0,0), (0,255,0), (255,255,0),
    (0,0,255), (255,0,255), (0,255,255), (255,255,255),
    (255,0,255), (192,40,40), (40,192,40), (192,192,40),
    (0,0,255), (192,40,192), (40,192,192), (192,192,192)
    ]

class LevelWidget(QWidget):

    xs = 4
    ys = 2
    
    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.tw = 8
        self.th = 8
        
        self.rows = 128
        self.columns = 20
        
        self.palettes = [default_palette]
        self.levels = [self.newLevel()]
        
        self.level_number = 1
        self.tile_images = {}
        self.currentTile = 0
        self.highlight = None
        
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        
        self.pen = QPen(Qt.white)
        self.pen.setWidth(2)
        self.pen.setJoinStyle(Qt.RoundJoin)
        self.pen.setCapStyle(Qt.RoundCap)
        
        self.setMouseTracking(True)
        
        self.loadImages(default_palette)
    
    def newLevel(self):
    
        level = []
        i = 0
        while i < 128:
            level.append([0] * 20)
            i += 1
        
        return level
    
    def loadLevels(self, file_name):
    
        palette, level = Tools.levels.read_levels(file_name)
        
        self.palettes = [palette]
        self.levels = [level]
        self.rows = len(level)
    
    def saveLevels(self, file_name):
    
        try:
            f = open(file_name, "w")
            for palette, level in zip(self.palettes, self.levels):
            
                f.write(" ".join(map(lambda x: "%i,%i,%i" % x, palette[:8])))
                f.write("\n")
                f.write(" ".join(map(lambda x: "%i,%i,%i" % x, palette[8:])))
                f.write("\n")

                for line in level:
                    f.write(" ".join(map(str, line)) + "\n")
            
            f.close()
            return True
        
        except IOError:
            return False
    
    def loadImages(self, level_palette):
    
        decode_palette = [None] * 16
        for key, value in Tools.graphics.palette.items():
            decode_palette[value] = qRgb(*tuple(map(ord, key)))
        
        encode_palette = []
        for r, g, b in level_palette:
            encode_palette.append(qRgb(r, g, b))
        
        number = 0
        for sprite in Tools.graphics.sprites:
        
            image = QImage(os.path.join("images", sprite + ".png"))
            image = image.convertToFormat(QImage.Format_Indexed8, decode_palette)
            image = image.scaled(self.xs * self.tw, self.ys * self.th)
            image.setColorTable(encode_palette)
            self.tile_images[number] = image
            number += 1
    
    def setTileImages(self, tile_images):
    
        self.tile_images = tile_images
    
    def clearLevel(self):
    
        for row in range(self.rows):
            for column in range(self.columns):
                self.writeTile(column, row, self.currentTile)
    
    def setLevel(self, number):
    
        self.level_number = number
        
        self.loadImages(self.palettes[number - 1])
        self.rows = len(self.levels[number - 1])
        self.adjustSize()
        self.update()
    
    def saveImage(self, path):
    
        image = QImage(self.sizeHint(), QImage.Format_RGB16)
        self.paint(image, QRect(QPoint(0, 0), image.size()))
        return image.save(path)
    
    def mousePressEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if event.button() == Qt.LeftButton:
            self.writeTile(c, r, self.currentTile)
        elif event.button() == Qt.MiddleButton:
            self.writeTile(c, r, 0)
        else:
            event.ignore()
    
    def mouseMoveEvent(self, event):
    
        r = self._row_from_y(event.y())
        c = self._column_from_x(event.x())
        
        if event.buttons() & Qt.LeftButton:
            self.writeTile(c, r, self.currentTile)
        elif event.buttons() & Qt.MiddleButton:
            self.writeTile(c, r, 0)
        else:
            event.ignore()
    
    def paintEvent(self, event):
    
        self.paint(self, event.rect())
    
    def paint(self, device, rect):
    
        painter = QPainter()
        painter.begin(device)
        painter.fillRect(rect, QBrush(Qt.black))
        
        if not self.levels:
            return
        
        painter.setPen(self.pen)
        
        y1 = rect.top()
        y2 = rect.bottom()
        x1 = rect.left()
        x2 = rect.right()
        
        r1 = min(max(0, self._row_from_y(y1)), self.rows - 1)
        r2 = min(max(0, self._row_from_y(y2)), self.rows - 1)
        c1 = self._column_from_x(x1)
        c2 = self._column_from_x(x2)
        
        if self.rows > 0:
        
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                
                    tile = self.levels[self.level_number - 1][r][c]
                    tile_image = self.tile_images[tile]
                    
                    painter.drawImage(c * self.tw * self.xs,
                                      r * self.th * self.ys,
                                      tile_image)
        painter.end()
    
    def sizeHint(self):
    
        return QSize(self.columns * self.tw * self.xs,
                     max(self.columns, self.rows) * self.th * self.ys)
    
    def _row_from_y(self, y):
    
        return y/(self.th * self.ys)
    
    def _column_from_x(self, x):
    
        return x/(self.tw * self.xs)
    
    def _y_from_row(self, r):
    
        return r * self.th * self.ys
    
    def _x_from_column(self, c):
    
        return c * self.tw * self.xs
    
    def updateCell(self, c, r):
    
        self.update(QRect(self._x_from_column(c), self._y_from_row(r),
              self.tw * self.xs, self.th * self.ys))
    
    def writeTile(self, c, r, tile):
    
        if not (0 <= r < self.rows and 0 <= c < self.columns):
            return
        
        self.levels[self.level_number - 1][r][c] = tile
        self.updateCell(c, r)


class EditorWindow(QMainWindow):

    def __init__(self):
    
        QMainWindow.__init__(self)
        
        self.path = ""
        
        area = QScrollArea()
        self.setCentralWidget(area)
        
        self.loadLevels()
        
        self.createToolBars()
        self.createMenus()
    
    def openFile(self):
    
        path = QFileDialog.getOpenFileName(self, self.tr("Open File"),
                                           self.path, self.tr("Level files (*.levels)"))
        if not path.isEmpty():
            try:
                self.loadLevels(path)
                
                # Regenerate the symbols toolbar and levels menu.
                self.addSymbolsToToolbar()
                self.addLevelMenus()
            
            except:
                QMessageBox.warning(self, self.tr("Open File"),
                    self.tr("Couldn't read the UEF file '%1'.\n").arg(path))
                raise
    
    def saveAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save As"),
                                           self.path, self.tr("Level files (*.levels)"))
        if not path.isEmpty():
        
            if self.saveLevels(unicode(path)):
                self.path = path
                self.setWindowTitle(self.tr(path))
            else:
                QMessageBox.warning(self, self.tr("Save Levels"),
                    self.tr("Couldn't write the new executable to %1.\n").arg(path))
    
    def saveImageAs(self):
    
        path = QFileDialog.getSaveFileName(self, self.tr("Save Image As"),
                                           self.path, self.tr("PNG files (*.png)"))
        if not path.isEmpty():
        
            if not self.levelWidget.saveImage(unicode(path)):
                QMessageBox.warning(self, self.tr("Save Image"),
                    self.tr("Couldn't save the image '%1'.\n").arg(path))
    
    def loadLevels(self, file_name = None):
    
        self.levelWidget = LevelWidget()
        self.centralWidget().setWidget(self.levelWidget)
        
        if file_name:
            self.levelWidget.loadLevels(file_name)
            self.path = file_name
    
    def saveLevels(self, path):
    
        return self.levelWidget.saveLevels(path)
    
    def createToolBars(self):
    
        self.tileGroup = QActionGroup(self)
        
        self.tilesToolBar = QToolBar(self.tr("Tiles"))
        self.addToolBar(Qt.TopToolBarArea, self.tilesToolBar)
        self.addSymbolsToToolbar()
    
    def addSymbolsToToolbar(self):
    
        for action in self.tileGroup.actions():
            self.tileGroup.removeAction(action)
            self.tilesToolBar.removeAction(action)
        
        symbols = self.levelWidget.tile_images.keys()
        symbols.sort()
        
        for symbol in symbols:
        
            icon = QIcon(QPixmap.fromImage(self.levelWidget.tile_images[symbol]))
            action = self.tilesToolBar.addAction(icon, str(symbol))
            action.setData(QVariant(symbol))
            action.setCheckable(True)
            self.tileGroup.addAction(action)
            action.triggered.connect(self.setCurrentTile)
        
        if self.tileGroup.actions():
            self.tileGroup.actions()[0].trigger()
    
    def createMenus(self):
    
        fileMenu = self.menuBar().addMenu(self.tr("&File"))
        
        newAction = fileMenu.addAction(self.tr("&New"))
        newAction.setShortcut(QKeySequence.New)
        newAction.setEnabled(False)
        
        openAction = fileMenu.addAction(self.tr("&Open"))
        openAction.setShortcut(QKeySequence.Open)
        openAction.triggered.connect(self.openFile)
        
        self.saveAsAction = fileMenu.addAction(self.tr("Save &As..."))
        self.saveAsAction.setShortcut(QKeySequence.SaveAs)
        self.saveAsAction.triggered.connect(self.saveAs)
        self.saveAsAction.setEnabled(True)
        
        self.saveImageAsAction = fileMenu.addAction(self.tr("Save &Image As..."))
        self.saveImageAsAction.triggered.connect(self.saveImageAs)
        self.saveImageAsAction.setEnabled(False)
        
        quitAction = fileMenu.addAction(self.tr("E&xit"))
        quitAction.setShortcut(self.tr("Ctrl+Q"))
        quitAction.triggered.connect(self.close)
        
        editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.clearAction = editMenu.addAction(self.tr("&Clear"))
        self.clearAction.triggered.connect(self.clearLevel)
        self.clearAction.setEnabled(False)
        
        self.levelsMenu = self.menuBar().addMenu(self.tr("&Levels"))
        self.levelsMenu.triggered.connect(self.selectLevel)
        self.levelsGroup = QActionGroup(self)
        self.addLevelMenus()
    
    def addLevelMenus(self):
    
        for action in self.levelsGroup.actions():
            self.levelsGroup.removeAction(action)
            self.levelsMenu.removeAction(action)
        
        for i in range(len(self.levelWidget.levels)):
            levelAction = self.levelsMenu.addAction(str(i + 1))
            levelAction.setData(QVariant(i + 1))
            levelAction.setCheckable(True)
            self.levelsGroup.addAction(levelAction)
        
        if self.levelsGroup.actions():
            self.levelsGroup.actions()[0].trigger()
    
    def setCurrentTile(self):
    
        self.levelWidget.currentTile = self.sender().data().toInt()[0]
    
    def selectLevel(self, action):
    
        number = action.data().toInt()[0]
        self.levelWidget.highlight = None
        self.setLevel(number)
        self.clearAction.setEnabled(True)
        self.saveImageAsAction.setEnabled(True)
        #self.saveAsAction.setEnabled(True)
    
    def setLevel(self, number):
    
        self.levelWidget.setLevel(number)
        
        # Also change the sprites in the toolbar.
        for action in self.tileGroup.actions():
        
            symbol = action.data().toInt()[0]
            icon = QIcon(QPixmap.fromImage(self.levelWidget.tile_images[symbol]))
            action.setIcon(icon)
    
    def clearLevel(self):
    
        answer = QMessageBox.question(self, self.tr("Clear Level"),
            self.tr("Clear the current level?"), QMessageBox.Yes | QMessageBox.No)
        
        if answer == QMessageBox.Yes:
            self.levelWidget.clearLevel()
    
    def sizeHint(self):
    
        levelSize = self.levelWidget.sizeHint()
        menuSize = self.menuBar().sizeHint()
        scrollBarSize = self.centralWidget().verticalScrollBar().size()
        
        return QSize(max(levelSize.width(), menuSize.width(), levelSize.width()),
                     levelSize.height() + menuSize.height() + scrollBarSize.height())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    
    window = EditorWindow()
    window.show()
    sys.exit(app.exec_())
