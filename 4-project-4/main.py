import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen

class Gauge(QWidget):
  def __init__(self, lowValue: int, highValue: int, tickmarkStep: int):
    super().__init__()
    self.__low__ = lowValue
    self.__high__ = highValue
    self.__tickmarkStep__ = tickmarkStep
    self.__currentValue__ = lowValue
    self.__animation__ = QPropertyAnimation(self, b"currentValue")
    self.setMinimumSize(400, 300)

  def updateValue(self, new_value: int, stepSpeed: int):
    clampedValue = max(self.__low__, min(new_value, self.__high__))

    # Fix: the needle start from 0 instead of the current value
    self.__animation__.stop()
    self.__animation__.setDuration(stepSpeed)
    self.__animation__.setStartValue(self.__currentValue__)
    self.__animation__.setEndValue(clampedValue)
    self.__animation__.start()

  @pyqtProperty(float)
  def currentValue(self):
    return self.__currentValue__
  @currentValue.setter
  def currentValue(self, value):
    self.__currentValue__ = max(self.__low__, min(value, self.__high__))
    self.update()

  def paintEvent(self, event):
    painter = QPainter(self)

    centerX = self.width() / 2
    centerY = self.height() / 2
    circleDiameter = min(self.width(), self.height())
    circleRadius = circleDiameter / 2
    x = int(centerX - circleRadius)
    y = int(centerY - circleRadius)
    width = int(circleDiameter)
    height = int(circleDiameter)
    startAngle = 0
    spanAngle = 180 * 16
    painter.drawArc(x, y, width, height, startAngle, spanAngle)

    # Draw main tickmarks
    tickmarks = list(range(self.__low__, self.__high__ + 1, self.__tickmarkStep__))
    for tickmark in tickmarks:
      self.__drawTick__(painter, centerX, centerY, circleRadius, tickmark, 10, True)

    # Draw minor tickmarks
    for i in range(len(tickmarks) - 1):
      start = tickmarks[i]
      end = tickmarks[i+1]
      step = (end - start) / 5
      for j in range(1, 5):
        self.__drawTick__(painter, centerX, centerY, circleRadius, start + j * step, 5)

    # Draw needle
    # normalize the value to the range [0, 180]
    angle = 180 - ((self.__currentValue__ - self.__low__) / 
                   (self.__high__ - self.__low__)) * 180
    angleRadian = math.radians(angle)
    needleLength = circleRadius
    # ABC right triangle (the right below is orthogonal)
    # AB is the opposite side of the angle
    # BC is the adjacent side of the angle
    # AC is the hypotenuse or the needleLength
    # sin(angle) = AB / AC
    # sine of an angle in a right triangle is the length of the opposite side of the hypotenuse
    # cos(angle) = BC / AC
    # cosine of an angle in a right triangle is the length of the adjacent side of the hypotenuse
    needleX = centerX + needleLength * math.cos(angleRadian)
    needleY = centerY - needleLength * math.sin(angleRadian)
    painter.setPen(QPen(Qt.GlobalColor.red, 2))
    painter.drawLine(QPointF(centerX, centerY), QPointF(needleX, needleY))
    
    painter.setBrush(Qt.GlobalColor.red)
    painter.drawEllipse(QPointF(centerX, centerY), 5, 5)

  def __drawTick__(self, painter: QPainter, centralX: int, centralY: int, 
                   circleRadius: int, value: int, tickLength: int, is_main=False):
    # normalize the value to the range [0, 180]
    angle = 180 - ((value - self.__low__) / 
                   (self.__high__ - self.__low__)) * 180
    angleRadian = math.radians(angle)
    
    # Draw tick line
    outerX = centralX + circleRadius * math.cos(angleRadian)
    outerY = centralY - circleRadius * math.sin(angleRadian)
    innerX = centralX + (circleRadius - tickLength) * math.cos(angleRadian)
    innerY = centralY - (circleRadius - tickLength) * math.sin(angleRadian)
    painter.drawLine(QPointF(outerX, outerY), QPointF(innerX, innerY))

    # Draw labels for main tickmarks
    if is_main:
      labelRadius = circleRadius - tickLength - 15
      labelX = centralX + labelRadius * math.cos(angleRadian)
      labelY = centralY - labelRadius * math.sin(angleRadian)
      painter.save()
      painter.translate(labelX, labelY)
      painter.drawText(QRectF(-20, -10, 40, 20), 
                       Qt.AlignmentFlag.AlignCenter, str(value))
      painter.restore()

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Gauge Widget")
    self.__setUpUI__()

  def __setUpUI__(self):
    low = 0
    high = 10000
    tickmarkStep = 1000

    gauge = Gauge(low, high, tickmarkStep)

    gaugeControlSlider = QSlider(Qt.Orientation.Horizontal)
    gaugeControlSlider.setRange(low, high)
    gaugeControlSlider.setTickInterval(tickmarkStep)
    gaugeControlSlider.valueChanged.connect(lambda: gauge.updateValue(gaugeControlSlider.value(), tickmarkStep))
    
    mainLayout = QVBoxLayout()
    mainLayout.addWidget(gauge)
    mainLayout.addWidget(gaugeControlSlider)

    centralWidget = QWidget()
    centralWidget.setLayout(mainLayout)
    self.setCentralWidget(centralWidget)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  mainWin = MainWindow()
  mainWin.show()
  sys.exit(app.exec_())