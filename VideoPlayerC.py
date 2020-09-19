#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import partial
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QTime
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QPushButton, QSlider,
                             QVBoxLayout, QFileDialog, QLabel)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.bottom_layout = QHBoxLayout()
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()

        #self.min = 0
        #self.sec = 0
        #self.hrs = 0

        self.search_button = QPushButton("Buscar",self)
        self.play_button = QPushButton("Iniciar Vídeo", self)
        self.stop_button = QPushButton("Volver al principio", self)
        self.title_label = QLabel("",self)
        self.time_label = QLabel('00:00:00',self)#("{}:{}:{}".format(self.form(self.hrs),self.form(self.min),self.form(self.sec),self))
        self.title_label.setStyleSheet('QLabel {background-color: black; color: green;}')
        self.time_label.setStyleSheet('QLabel {background-color: black; color: red;}')
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setFixedWidth(68)
        #self.title_label.setFixedWidth(150)
        self.volume_label = QLabel("VOLUMEN:",self)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.timeCounting = False

        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        self.seek_slider.sliderMoved.connect(self.media_player.setPosition)
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        self.media_player.positionChanged.connect(self.seek_slider.setValue)
        self.media_player.durationChanged.connect(partial(self.seek_slider.setRange, 0))

        self.layout.addWidget(self.video_widget)
        self.layout.addLayout(self.bottom_layout)
        
        self.bottom_layout.addWidget(self.search_button)
        self.bottom_layout.addWidget(self.title_label)
        self.bottom_layout.addWidget(self.time_label)
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
        self.setWindowTitle("Reproductor de video (.avi)")
        self.resize(800, 515)#600
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        timer2 = QTimer(self)
        
        timer2.timeout.connect(self.displayTime)
        timer2.start(1000)        

        self.active_timer = False


    def move_text(self):
        if self.text != "":
            lista = list(self.text)
            dele = lista.pop(0)
            lista.append(dele)
            tf = "".join(lista)
            self.title_label.setText(tf)
            self.text = tf
        
    
    def play_clicked(self):
        if (self.media_player.state() in
            (QMediaPlayer.PausedState, QMediaPlayer.StoppedState)):
            self.timeCounting = True
            self.media_player.play()
            print(self.media_player.state())
            
        else:
            self.media_player.pause()
            print(self.media_player.state())
            self.timeCounting = False
    
    def stop_clicked(self):
        print(self.media_player.state())
        self.media_player.stop()
        self.min = 0
        self.sec = 0
        self.hrs = 0
        self.time_label.setText("{}:{}:{}".format(self.form(self.hrs),self.form(self.min),self.form(self.sec),self))
        self.timeCounting = False
        
        
    def state_changed(self, newstate):
        states = {
            QMediaPlayer.PausedState: "Continuar",
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
        fileName,_ = QFileDialog.getOpenFileName(self, "Archivo de video", '/home')
        if fileName != '':
            self.min = 0
            self.sec = 0
            self.hrs = 0
            timer = QTimer(self)
            self.videoName = fileName.split("/")[-1]
            self.text = "-"+self.videoName+"-"
            if self.active_timer == False:
                timer.timeout.connect(self.move_text)
                self.active_timer = True
                timer.start(650)#650
            VIDEO_PATH = fileName
            self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
            self.media_player.setVideoOutput(self.video_widget)
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)

    def form(self,n):
        if n<10:
            n="0"+str(n)
        return n

    def displayTime(self):
        if self.timeCounting == True:
            if self.sec == 60:
                self.min += 1
                self.sec = 0
            if self.min == 60:
                self.hrs += 1
                self.min = 0
            
            if self.media_player.state() == 0:
                self.timeCounting = False
                self.min = 0
                self.sec = 0
                self.hrs = 0
            else:
                self.time_label.setText("{}:{}:{}".format(self.form(self.hrs),self.form(self.min),self.form(self.sec),self))
                self.sec+=1
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
sys.exit(app.exec_())
