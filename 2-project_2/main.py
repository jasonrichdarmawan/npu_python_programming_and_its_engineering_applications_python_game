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

  def __init__(self):
    """
    feat 2: add volume slider
    """
    super().__init__()
    self.setWindowTitle("PyQt5 Media Player") 

    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.Flag.VideoSurface)
    self.mediaPlayer.stateChanged.connect(self.__mediaPlayerStateChanged__)
    self.mediaPlayer.positionChanged.connect(self.__mediaPlayerPositionChanged__)
    self.mediaPlayer.durationChanged.connect(self.__mediaPlayerDurationChanged__)
    self.mediaPlayer.error.connect(self.__handleError__)

    self.__setup_ui__()

  def __setup_ui__(self):
    """
    chore 1: reoganize the code by separating concerns into dedicated methods
    """
    # Video widget
    videoWidget = QVideoWidget()

    # Play button
    self.playButton = QPushButton()
    self.playButton.setEnabled(False)
    self.playButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
    self.playButton.clicked.connect(self.__playMediaPlayer__)

    # Position slider
    self.positionSlider = QSlider(Qt.Orientation.Horizontal)
    self.positionSlider.setRange(0, 0)
    self.positionSlider.sliderMoved.connect(self.__setMediaPlayerPosition__)

    # volume control
    volumeSlider = QSlider(Qt.Orientation.Horizontal)
    volumeSlider.setRange(0, 100)
    volumeSlider.setValue(100)
    volumeSlider.sliderMoved.connect(self.mediaPlayer.setVolume)
    volumeIcon = QLabel()
    volumeIcon.setPixmap(self.style().standardPixmap(QStyle.StandardPixmap.SP_MediaVolume))
    volumeLayout = QHBoxLayout()
    volumeLayout.addWidget(volumeIcon)
    volumeLayout.addWidget(volumeSlider)

    # Error label
    self.error = QLabel()
    self.error.setSizePolicy(QSizePolicy.Policy.Preferred, 
                             QSizePolicy.Policy.Maximum)
    
    # Open Media File button
    openMediaFileButton = QPushButton("Open Medila File")   
    openMediaFileButton.setToolTip("Open Media File")
    openMediaFileButton.setFixedHeight(24)
    openMediaFileButton.clicked.connect(self.__openMediaFile__)

    # Layout for controls
    controlLayout = QHBoxLayout()
    controlLayout.setContentsMargins(0, 0, 0, 0)
    controlLayout.addWidget(self.playButton)
    controlLayout.addWidget(self.positionSlider)

    mainLayout = QVBoxLayout()
    mainLayout.addWidget(videoWidget)
    mainLayout.addLayout(controlLayout)
    mainLayout.addLayout(volumeLayout)
    mainLayout.addWidget(self.error)
    mainLayout.addWidget(openMediaFileButton)

    # Create a widget for window contents
    centralWidget = QWidget(self)
    centralWidget.setLayout(mainLayout)
    self.setCentralWidget(centralWidget)

    # Set video output
    self.mediaPlayer.setVideoOutput(videoWidget)

  def __resetState__(self):
    """
    fix 1: error message is not cleared
    fix 2: position slider is not hidden when media is not loaded
    """
    self.playButton.setEnabled(False)
    self.positionSlider.setRange(0, 0)
    self.error.setText("")

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

      self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
      self.playButton.setEnabled(True)

  def __playMediaPlayer__(self):
    """
    chore 2: rename play to __playMediaPlayer__ to make it more specific
    """
    if self.mediaPlayer.state() == QMediaPlayer.State.PlayingState:
      self.mediaPlayer.pause()
    else:
      self.mediaPlayer.play()

  def __mediaPlayerStateChanged__(self, state: QMediaPlayer.State):
    if state == QMediaPlayer.State.PlayingState:
      self.playButton.setIcon(self.style()
                                  .standardIcon(QStyle.StandardPixmap.SP_MediaPause))
    else:
      self.playButton.setIcon(self.style()
                                  .standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

  def __mediaPlayerPositionChanged__(self, position: int):
    self.positionSlider.setValue(position)

  def __mediaPlayerDurationChanged__(self, duration: int):
    self.positionSlider.setRange(0, duration)

  def __setMediaPlayerPosition__(self, position: int):
    self.mediaPlayer.setPosition(position)

  def __handleError__(self):
    self.playButton.setEnabled(False)
    self.error.setText("Error: " + self.mediaPlayer.errorString())
 
app = QApplication(sys.argv)
mediaPlayer = MediaPlayer()
mediaPlayer.resize(640, 480)
mediaPlayer.show()
sys.exit(app.exec_())