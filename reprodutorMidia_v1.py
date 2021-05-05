"""
MAURICIO RODRIGUES MENDES
VAGNER VIEIRA DOS SANTOS
"""

import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, \
    QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Media Player")
        self.setGeometry(350, 150, 1080, 720)
        self.setWindowIcon(QIcon('ic_video_library.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.darkGray)
        self.setPalette(p)
        self.init_ui()
        self.show()

    def init_ui(self):

        # objeto Media Player
        # self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.volumeChanged.connect(self.status_volume)
        self.mediaPlayer.setVolume(50)

        # objeto videowidget
        videowidget = QVideoWidget()

        # botão para selecionar mídia
        openBtn = QPushButton('Abrir')
        openBtn.clicked.connect(self.abrir_ficheiro)
        openBtn.setStyleSheet('QPushButton {background-color: #74992e}')

        # self.mediaPlayer.setVolume(60)
        volumeIncBtn = QPushButton(' V [ + ] ')  # Aumentar Volume
        volumeIncBtn.setStyleSheet("background-color:yellow;\n"
                                   "color: black;\n"
                                   "border-style: outset;\n"
                                   "border-width:1px;\n"
                                   "border-radius:5px;\n"
                                   "border-color:white;\n"
                                   "padding :6px;\n"
                                   "min-width:5px;\n"
                                   "\n"
                                   "\n"
                                   "")

        volumeDescBtn = QPushButton(' V [ - ] ')  # Diminuir Volume

        volumeDescBtn.setStyleSheet("background-color:yellow;\n"
                                    "color: black;\n"
                                    "border-style: outset;\n"
                                    "border-width:1px;\n"
                                    "border-radius:5px;\n"
                                    "border-color:white;\n"
                                    "padding :6px;\n"
                                    "min-width:5px;\n"
                                    "\n"
                                    "\n"
                                    "")

        volumeDescBtn.clicked.connect(self.diminuirVolume)
        volumeIncBtn.clicked.connect(self.aumentarVolume)

        # criação do botão para reproodução de áudio e vídeo
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.video_play)
        self.playBtn.setStyleSheet("background-color:brown;\n"
                                   "color: white;\n"
                                   "border-style: outset;\n"
                                   "border-width:1px;\n"
                                   "border-radius:5px;\n"
                                   "border-color:white;\n"
                                   "padding :6px;\n"
                                   "min-width:5px;\n"
                                   "\n"
                                   "\n"
                                   "")
        # controle da barra deslizante
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.selecionar_posicao)
        self.slider.setStyleSheet("background-color:blue;\n"
                                  "color: white;\n"
                                  "border-style: outset;\n"
                                  "border-width:1px;\n"
                                  "border-radius:4px;\n"
                                  "border-color:white;\n"
                                  "padding :3px;\n"
                                  "min-width:5px;\n"
                                  "")
        # label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # criação do layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(60, -10, 60, -10)

        # definiçãao dos widgets para o layout
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(volumeDescBtn)
        hboxLayout.addWidget(volumeIncBtn)

        # layout vbox
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        # vboxLayout.addWidget(self.changeVolume())

        self.setLayout(vboxLayout)
        self.mediaPlayer.setVideoOutput(videowidget)

        # Parâmetros do reprodutor media player

        self.mediaPlayer.stateChanged.connect(self.status_midia_alteracao)
        self.mediaPlayer.positionChanged.connect(self.altera_posicao)
        self.mediaPlayer.durationChanged.connect(self.altera_duracao)

    def abrir_ficheiro(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video/Audio")

        if filename != "":
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def video_play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def status_midia_alteracao(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def altera_posicao(self, position):
        self.slider.setValue(position)

    def altera_duracao(self, duration):
        self.slider.setRange(0, duration)

    def selecionar_posicao(self, position):
        self.mediaPlayer.setPosition(position)

    def erro_manipulador(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Erro na reprodução: " + self.mediaPlayer.errorString())

    # em processo de testes
    def status_volume(self):
        # msg = self.statusBar().currentMessage()
        # msg = msg[:-2] + str(self.mediaPlayer.volume())
        # self.statusBar().showMessage(msg)
        pass

    def aumentarVolume(self):
        vol = self.mediaPlayer.volume()
        vol = min(vol + 5, 100)
        self.mediaPlayer.setVolume(vol)
        # self.increaseVolume.setEnabled(True)

    def diminuirVolume(self):
        vol = self.mediaPlayer.volume()
        vol = max(vol - 5, 0)
        self.mediaPlayer.setVolume(vol)
        # self.decreaseVolume.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    window = Window()
    sys.exit(app.exec_())
