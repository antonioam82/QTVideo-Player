#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout, QFileDialog, QLabel)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        #self.media_player.setMedia(
            #QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
        #self.media_player.setVideoOutput(self.video_widget)

        self.search_button = QPushButton("Buscar",self)
        self.play_button = QPushButton("Iniciar Vídeo", self)
        self.stop_button = QPushButton("Iniciar", self)
        #self.title_label = QLabel("VIDEO:",self)
        self.title_label = QLabel("",self)
        self.tittle_label.setStyleSheet('QLabel {background-color: black; color: green;}')
        #self.title_label.setStyleSheet("background-color : gold")
        self.title_label.setFixedWidth(190)
        self.volume_label = QLabel("VOLUMEN:",self)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        self.seek_slider.sliderMoved.connect(self.media_player.setPosition)
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        self.media_player.positionChanged.connect(self.seek_slider.setValue)
        self.media_player.durationChanged.connect(
            partial(self.seek_slider.setRange, 0))

        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(self.bottom_layout)
        self.bottom_layout.addWidget(self.search_button)
        self.bottom_layout.addWidget(self.title_label)
        
        self.bottom_layout.addWidget(self.play_button)
        self.bottom_layout.addWidget(self.stop_button)
        self.bottom_layout.addWidget(self.volume_label)
        self.bottom_layout.addWidget(self.volume_slider)
        self.layout.addWidget(self.seek_slider)

        self.search_button.clicked.connect(self.openFile)
        self.play_button.clicked.connect(self.play_clicked)
        self.stop_button.clicked.connect(self.stop_clicked)
        self.media_player.stateChanged.connect(self.state_changed)

        self.video_widget.installEventFilter(self)
        ####label2.setFont(QtGui.QFont("Sanserif", 20))
        #
        self.setWindowTitle("Reproductor de video")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
    
    def play_clicked(self):
        if (self.media_player.state() in
            (QMediaPlayer.PausedState, QMediaPlayer.StoppedState)):
            print("Lets go")
            self.media_player.play()
        else:
            self.media_player.pause()
    
    def stop_clicked(self):
        self.media_player.stop()
    
    def state_changed(self, newstate):
        states = {
            QMediaPlayer.PausedState: "Resumir",
            QMediaPlayer.PlayingState: "Pausa",
            QMediaPlayer.StoppedState: "Reproducir"
        }
        self.play_button.setText(states[newstate])
        self.stop_button.setEnabled(newstate != QMediaPlayer.StoppedState)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False

    def openFile(self):
        print("Done")
        fileName,_ = QFileDialog.getOpenFileName(self, "Archivo de video", '/home')#QDir.homePath())
        if fileName != '':
            videoName = fileName.split("/")[-1]
            #self.title_label.setText('VIDEO: {}'.format(videoName))
            self.title_label.setText(videoName)
            VIDEO_PATH = fileName
            self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
            self.media_player.setVideoOutput(self.video_widget)
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
sys.exit(app.exec_())

    
