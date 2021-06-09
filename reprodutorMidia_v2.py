# =========== VERSÃO BETA ==========
import sys

from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, \
    QStyle, QSizePolicy, QFileDialog

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Media Player")
        self.setGeometry(160, 40, 1080, 720)
        self.setWindowIcon(QIcon('ic_video_library.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        self.init_ui()
        app.installEventFilter(self)
        self.show()

    def init_ui(self):

        # objeto Media Player
        # self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer = QMediaPlayer()
        # self.mediaPlayer.mediaStatusChanged.connect(self.getDuration())
        self.mediaPlayer.volumeChanged.connect(self.status_volume)
        self.mediaPlayer.setVolume(30)

        # objeto videowidget
        videowidget = QVideoWidget()

        # botão para selecionar mídia
        openBtn = QPushButton('Open')
        openBtn.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        openBtn.clicked.connect(self.abrir_ficheiro)
        openBtn.setStyleSheet("background-color:#74992e;\n"
                              "color: black;\n"
                              "border-style: outset;\n"
                              "border-width: 1px;\n"
                              "border-radius: 3px;\n"
                              "border-color:white;\n"
                              "padding :6px;\n"
                              "min-width:5px;\n"
                              "\n"
                              "\n"
                              "")

        volumeIncBtn = QPushButton(' V [ + ] ')  # Aumentar Volume
        volumeIncBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        volumeIncBtn.setStyleSheet("background-color:white;\n"
                                   "color: black;\n"
                                   "border-style: outset;\n"
                                   "border-width: 1px;\n"
                                   "border-radius: 3px;\n"
                                   "border-color:white;\n"
                                   "padding :6px;\n"
                                   "min-width:5px;\n"
                                   "\n"
                                   "\n"
                                   "")

        volumeDescBtn = QPushButton(' V [ - ] ')  # Diminuir Volume
        volumeDescBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        volumeDescBtn.setStyleSheet("background-color:white;\n"
                                    "color: black;\n"
                                    "border-style: outset;\n"
                                    "border-width:1px;\n"
                                    "border-radius: 3px;\n"
                                    "border-color:white;\n"
                                    "padding :6px;\n"
                                    "min-width:5px;\n"
                                    "\n"
                                    "\n"
                                    "")

        volumeDescBtn.clicked.connect(self.diminuirVolume)
        volumeIncBtn.clicked.connect(self.aumentarVolume)
        # creating playlist controls
        prevBtn = QPushButton('Prev')
        prevBtn.setStyleSheet("background-color:white;\n"
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

        nextBtn = QPushButton('Next')
        nextBtn.setStyleSheet("background-color:white;\n"
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

        # prevBtn.clicked.connect(self.prevItemPlaylist)
        # nextBtn.clicked.connect(self.nextItemPlaylist)

        # criação do botão para reprodução de áudio e vídeo
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
        # s_Slider = QSlider()
        # s_Slider = QSlider(Qt.Horizontal)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        # s_Slider.setOrientation(Qt.Horizontal)
        self.slider.setTracking(False)
        self.slider.sliderMoved.connect(self.selecionar_posicao)
        self.slider.setRange(0, 0)
        # self.slider.setRange(0, 0)
        # self.slider.sliderMoved.connect(self.selecionar_posicao)
        self.slider.setStyleSheet("background-color:darkGray ;\n"
                                  "color: white;\n"
                                  "border-style: outset;\n"
                                  "border-width:1px;\n"
                                  "border-radius:4px;\n"
                                  "border-color:white;\n"
                                  "padding :3px;\n"
                                  "min-width:5px;\n"
                                  "")

        # criação do label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # controle botão playlist
        prevBtn.clicked.connect(self.previous_Playlist)
        nextBtn.clicked.connect(self.next_Playlist)

        # criação do layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(60, -10, 60, -10)
        seekSliderLayout = QHBoxLayout()
        # hboxLayout.setContentsMargins(0, 0, 0, 0)

        # definição dos widgets para o layout
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
        print(f'{position}')

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
        # self.aumentarVolume.setEnabled(True)

    def diminuirVolume(self):
        vol = self.mediaPlayer.volume()
        vol = max(vol - 5, 0)
        self.mediaPlayer.setVolume(vol)
        # self.diminuirVolume.setEnabled(True)

    def getDuration(self, d):
        self.altera_duracao().setRange(0, d)
        self.altera_duracao().setEnabled(True)
        self.displayTime(d)

    # processo de testes
    def qmp_mediaStatusChanged(self):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia and self.userAction == 1:
            durationT = self.mediaPlayerplayer.duration()
            self.video_play().widget().setRange(0, durationT)
            self.video_play().layout().itemAt(0).layout().itemAt(2).widget().setText(
                '%d:%02d' % (int(durationT / 60000), int((durationT / 1000) % 60)))
            self.mediaPlayer.play()

    def previous_Playlist(self):
        self.mediaPlayer.playlist().previous()

    def next_Playlist(self):
        self.mediaPlayer.playlist().next()

    def playHandler(self):
        self.userAction = 1
        self.statusBar().showMessage('Reproduzindo no volume %d' % self.mediaPlayer.volume())
        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            if self.mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
                # self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.currentFile)))
                print(self.currentPlaylist.mediaCount())
                if self.currentPlaylist.mediaCount() == 0:
                    self.openFile()
                if self.currentPlaylist.mediaCount() != 0:
                    self.mediaPlayer.setPlaylist(self.currentPlaylist)
            elif self.mediaPlayer.mediaStatus() == QMediaPlayer.LoadedMedia:
                self.mediaPlayer.play()
            elif self.mediaPlayer.mediaStatus() == QMediaPlayer.BufferedMedia:
                self.mediaPlayer.play()
        elif self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            pass
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.mediaPlayer.play()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()

            if key == Qt.Key_A:  # aumento de velocidade de reprodução
                self.mediaPlayer.setPlaybackRate(1.6)
            elif key == Qt.Key_D:  # diminui a velocidade de reprodução
                self.mediaPlayer.setPlaybackRate(0.8)
            elif key == Qt.Key_N:  # velocidade normal
                self.mediaPlayer.setPlaybackRate(1.0)

            # seleciona posição - argumento em milissegundos -.
            elif key == Qt.Key_R:  # retrocede o audio/video
                self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000)
            elif key == Qt.Key_P:  # avança o audio/video
                self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000)

        return super().eventFilter(source, event)

    def fecharEvent(self, event):
        self.mediaPlayer.setMedia(QMediaContent())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('"Plastique"')
    window = Window()
    sys.exit(app.exec_())
