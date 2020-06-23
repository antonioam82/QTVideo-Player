#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.setWindowTitle("Reproductor de video")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
