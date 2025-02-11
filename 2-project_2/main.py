"""
Original author: CodersLegacy [1]

Reference:
[1] https://coderslegacy.com/python/pyqt5-video-player-with-qmediaplayer/
"""

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, 
                             QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton
import sys

class MediaPlayer(QMainWindow):
  """
  chore 1: remove exitCall(self) function
  """

  a: QPushButton

  def __init__(self):
    """
    feat 2: add volume slider
    """
    super().__init__()
    self.setWindowTitle("PyQt5 Media Player") 

    self.__mediaPlayer__ = QMediaPlayer(None, QMediaPlayer.Flag.VideoSurface)
    self.__mediaPlayer__.stateChanged.connect(self.__mediaPlayerStateChanged__)
    self.__mediaPlayer__.positionChanged.connect(self.__mediaPlayerPositionChanged__)
    self.__mediaPlayer__.durationChanged.connect(self.__mediaPlayerDurationChanged__)
    self.__mediaPlayer__.error.connect(self.__handleError__)

    self.__setup_ui__()

  def __setup_ui__(self):
    """
    chore 1: reoganize the code by separating concerns into dedicated methods
    """
    # Video widget
    videoWidget = QVideoWidget()

    # Play button
    self.__mediaPlayerPlayButton__ = QPushButton()
    self.__mediaPlayerPlayButton__.setEnabled(False)
    self.__mediaPlayerPlayButton__.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
    self.__mediaPlayerPlayButton__.clicked.connect(self.__playMediaPlayer__)

    # Position slider
    self.__mediaPlayerPositionSlider__ = QSlider(Qt.Orientation.Horizontal)
    self.__mediaPlayerPositionSlider__.setRange(0, 0)
    self.__mediaPlayerPositionSlider__.sliderMoved.connect(self.__setMediaPlayerSetPosition__)

    # volume control
    volumeSlider = QSlider(Qt.Orientation.Horizontal)
    volumeSlider.setRange(0, 100)
    volumeSlider.setValue(100)
    volumeSlider.sliderMoved.connect(self.__mediaPlayer__.setVolume)
    volumeIcon = QLabel()
    volumeIcon.setPixmap(self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaVolume))
    volumeLayout = QHBoxLayout()
    volumeLayout.addWidget(volumeIcon)
    volumeLayout.addWidget(volumeSlider)

    # Error label
    self.__error__ = QLabel()
    self.__error__.setSizePolicy(QSizePolicy.Policy.Preferred, 
                             QSizePolicy.Policy.Maximum)
    
    # Open Media File button
    openMediaFileButton = QPushButton("Open Medila File")   
    openMediaFileButton.setToolTip("Open Media File")
    openMediaFileButton.setFixedHeight(24)
    openMediaFileButton.clicked.connect(self.__openMediaFile__)

    # Layout for controls
    controlLayout = QHBoxLayout()
    controlLayout.setContentsMargins(0, 0, 0, 0)
    controlLayout.addWidget(self.__mediaPlayerPlayButton__)
    controlLayout.addWidget(self.__mediaPlayerPositionSlider__)

    mainLayout = QVBoxLayout()
    mainLayout.addWidget(videoWidget)
    mainLayout.addLayout(controlLayout)
    mainLayout.addLayout(volumeLayout)
    mainLayout.addWidget(self.__error__)
    mainLayout.addWidget(openMediaFileButton)

    # Create a widget for window contents
    centralWidget = QWidget(self)
    centralWidget.setLayout(mainLayout)
    self.setCentralWidget(centralWidget)

    # Set video output
    self.__mediaPlayer__.setVideoOutput(videoWidget)

  def __resetState__(self):
    """
    fix 1: error message is not cleared
    fix 2: position slider is not hidden when media is not loaded
    """
    self.__mediaPlayerPlayButton__.setEnabled(False)
    self.__mediaPlayerPositionSlider__.setRange(0, 0)
    self.__error__.setText("")

  def __openMediaFile__(self):
    """
    feat 1: add file filter
    fix 1: error message is not cleared
    """
    fileFilter = "Media Files (*.mp3 *.wav *.flac *.aac *.mp4 *.avi *.mkv *.wmv)"
    fileName, _ = QFileDialog.getOpenFileName(self, "Open Media File",
                                              None, fileFilter)

    if fileName != '':
      self.__resetState__()

      self.__mediaPlayer__.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
      self.__mediaPlayerPlayButton__.setEnabled(True)

  def __playMediaPlayer__(self):
    """
    chore 2: rename play to __playMediaPlayer__ to make it more specific
    """
    if self.__mediaPlayer__.state() == QMediaPlayer.State.PlayingState:
      self.__mediaPlayer__.pause()
    else:
      self.__mediaPlayer__.play()

  def __mediaPlayerStateChanged__(self, state: QMediaPlayer.State):
    if state == QMediaPlayer.State.PlayingState:
      self.__mediaPlayerPlayButton__.setIcon(self.style()
                                  .standardIcon(QStyle.StandardPixmap.SP_MediaPause))
    else:
      self.__mediaPlayerPlayButton__.setIcon(self.style()
                                  .standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

  def __mediaPlayerPositionChanged__(self, position: int):
    self.__mediaPlayerPositionSlider__.setValue(position)

  def __mediaPlayerDurationChanged__(self, duration: int):
    self.__mediaPlayerPositionSlider__.setRange(0, duration)

  def __setMediaPlayerSetPosition__(self, position: int):
    self.__mediaPlayer__.setPosition(position)

  def __handleError__(self):
    self.__mediaPlayerPlayButton__.setEnabled(False)
    self.__error__.setText("Error: " + self.__mediaPlayer__.errorString())
 
app = QApplication(sys.argv)
mediaPlayer = MediaPlayer()
mediaPlayer.resize(640, 480)
mediaPlayer.show()
sys.exit(app.exec_())