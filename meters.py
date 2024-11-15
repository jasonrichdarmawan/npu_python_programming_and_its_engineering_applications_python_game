import sys
import math
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt, QTimer


# 通用仪表基类
class InstrumentBase(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 150)
        self.setStyleSheet("""
            InstrumentBase {
                background-color: #222;
                border-radius: 10px;
                border: 2px solid #444;
            }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_background(painter)
        self.draw_indicator(painter)


# 仪表盘类
class Gauge(InstrumentBase):
    def __init__(self, value=0, min_value=0, max_value=100, label='Value'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.label = label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)

    def update_value(self):
        self.value = (self.value + 1) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        center = self.rect().center()
        radius = min(self.width(), self.height()) / 2 * 0.8
        painter.drawEllipse(center, radius, radius)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 10):
            angle = self.value_to_angle(i)
            x = center.x() + radius * 0.8 * math.sin(angle)
            y = center.y() - radius * 0.8 * math.cos(angle)
            painter.drawText(x - 10, y + 5, str(i))

    def value_to_angle(self, value):
        return (value - self.min_value) / (self.max_value - self.min_value) * 2 * math.pi - math.pi / 2

    def draw_indicator(self, painter):
        center = self.rect().center()
        radius = min(self.width(), self.height()) / 2 * 0.6
        angle = self.value_to_angle(self.value)
        needle_length = radius * 0.6
        x_end = center.x() + needle_length * math.sin(angle)
        y_end = center.y() - needle_length * math.cos(angle)
        painter.setPen(QPen(Qt.red, 3))
        painter.drawLine(center.x(), center.y(), x_end, y_end)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(center.x() - 20, center.y() + radius * 0.3, self.label + ':'+ str(self.value))


# 温度计类
class Thermometer(InstrumentBase):
    def __init__(self, value=20, min_value=0, max_value=100, unit='°C'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(2000)

    def update_value(self):
        self.value = (self.value + 5) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        painter.drawRect(30, 50, 20, 200)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 10):
            y = 250 - (i - self.min_value) * (200 / (self.max_value - self.min_value))
            painter.drawText(10, y, str(i) + self.unit)

    def draw_indicator(self, painter):
        y = 250 - (self.value - self.min_value) * (200 / (self.max_value - self.min_value))
        painter.setBrush(QColor('red'))
        painter.drawRect(35, y, 10, 250 - y)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(20, y - 10, str(self.value) + self.unit)


# 压力计类
class Manometer(InstrumentBase):
    def __init__(self, value=1.0, min_value=0, max_value=2.0, unit='MPa'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1500)

    def update_value(self):
        self.value = round(self.value + 0.1, 1) % (self.max_value + 0.1)
        self.update()

    def draw_background(self, painter):
        center = self.rect().center()
        painter.drawArc(center.x() - 70, center.y() - 70, 140, 140, 45 * 16, 270 * 16)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(int(self.min_value * 10), int(self.max_value * 10) + 1, 1):
            angle = self.value_to_angle(i / 10)
            x = center.x() + 70 * math.sin(angle)
            y = center.y() - 70 * math.cos(angle)
            painter.drawText(x - 10, y + 5, str(i / 10) + self.unit)

    def value_to_angle(self, value):
        return (value - self.min_value) / (self.max_value - self.min_value) * 2.5 * math.pi - math.pi / 4

    def draw_indicator(self, painter):
        center = self.rect().center()
        angle = self.value_to_angle(self.value)
        x_end = center.x() + 60 * math.sin(angle)
        y_end = center.y() - 60 * math.cos(angle)
        painter.setPen(QPen(Qt.blue, 3))
        painter.drawLine(center.x(), center.y(), x_end, y_end)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(center.x() - 30, center.y() + 80, '压力:'+ str(self.value) + self.unit)


# 电压表类
class Voltmeter(InstrumentBase):
    def __init__(self, value=220, min_value=0, max_value=380, unit='V'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(3000)

    def update_value(self):
        self.value = (self.value + 10) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        painter.drawRect(30, 30, 100, 200)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 20):
            y = 230 - (i - self.min_value) * (200 / (self.max_value - self.min_value))
            painter.drawText(20, y, str(i) + self.unit)

    def draw_indicator(self, painter):
        y = 230 - (self.value - self.min_value) * (200 / (self.max_value - self.min_value))
        painter.setBrush(QColor('green'))
        painter.drawRect(35, y, 90, 230 - y)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(15, y - 10, str(self.value) + self.unit)


# 电流表类
class Ammeter(InstrumentBase):
    def __init__(self, value=5, min_value=0, max_value=10, unit='A'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(2500)

    def update_value(self):
        self.value = (self.value + 1) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        painter.drawRect(30, 30, 100, 200)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 1):
            y = 230 - (i - self.min_value) * (200 / (self.max_value - self.min_value))
            painter.drawText(20, y, str(i) + self.unit)

    def draw_indicator(self, painter):
        y = 230 - (self.value - self.min_value) * (200 / (self.max_value - self.min_value))
        painter.setBrush(QColor('yellow'))
        painter.drawRect(35, y, 90, 230 - y)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(15, y - 10, str(self.value) + self.unit)


# 液位计类
class LevelMeter(InstrumentBase):
    def __init__(self, value=50, min_value=0, max_value=100, unit='%'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(2000)

    def update_value(self):
        self.value = (self.value + 5) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        painter.drawRect(30, 30, 100, 200)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 10):
            y = 230 - (i - self.min_value) * (200 / (self.max_value - self.min_value))
            painter.drawText(20, y, str(i) + self.unit)

    def draw_indicator(self, painter):
        y = 230 - (self.value - self.min_value) * (200 / (self.max_value - self.min_value))
        painter.setBrush(QColor('orange'))
        painter.drawRect(35, y, 90, 230 - y)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(15, y - 10, str(self.value) + self.unit)


# 流量计类
class FlowMeter(InstrumentBase):
    def __init__(self, value=100, min_value=0, max_value=200, unit='L/min'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)

    def update_value(self):
        self.value = (self.value + 10) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        center = self.rect().center()
        painter.drawEllipse(center, 60, 60)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 20):
            angle = self.value_to_angle(i)
            x = center.x() + 50 * math.sin(angle)
            y = center.y() - 50 * math.cos(angle)
            painter.drawText(x - 10, y + 5, str(i) + self.unit)

    def value_to_angle(self, value):
        return (value - self.min_value) / (self.max_value - self.min_value) * 2 * math.pi - math.pi / 2

    def draw_indicator(self, painter):
        center = self.rect().center()
        radius = 50
        angle = self.value_to_angle(self.value)
        x_end = center.x() + radius * math.sin(angle)
        y_end = center.y() - radius * math.cos(angle)
        painter.setPen(QPen(Qt.magenta, 3))
        painter.drawLine(center.x(), center.y(), x_end, y_end)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(center.x() - 30, center.y() + 70, '流量:'+ str(self.value) + self.unit)


# 转速表类
class Tachometer(InstrumentBase):
    def __init__(self, value=1000, min_value=0, max_value=2000, unit='RPM'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1500)

    def update_value(self):
        self.value = (self.value + 100) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        center = self.rect().center()
        painter.drawEllipse(center, 70, 70)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 200):
            angle = self.value_to_angle(i)
            x = center.x() + 60 * math.sin(angle)
            y = center.y() - 60 * math.cos(angle)
            painter.drawText(x - 20, y + 5, str(i) + self.unit)

    def value_to_angle(self, value):
        return (value - self.min_value) / (self.max_value - self.min_value) * 2 * math.pi - math.pi / 2

    def draw_indicator(self, painter):
        center = self.rect().center()
        radius = 60
        angle = self.value_to_angle(self.value)
        x_end = center.x() + radius * math.sin(angle)
        y_end = center.y() - radius * math.cos(angle)
        painter.setPen(QPen(Qt.cyan, 3))
        painter.drawLine(center.x(), center.y(), x_end, y_end)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(center.x() - 30, center.y() + 80, '转速:'+ str(self.value) + self.unit)


# 湿度计类
class Hygrometer(InstrumentBase):
    def __init__(self, value=50, min_value=0, max_value=100, unit='%RH'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(2500)

    def update_value(self):
        self.value = (self.value + 5) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        painter.drawRect(30, 30, 100, 200)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 10):
            y = 230 - (i - self.min_value) * (200 / (self.max_value - self.min_value))
            painter.drawText(20, y, str(i) + self.unit)

    def draw_indicator(self, painter):
        y = 230 - (self.value - self.min_value) * (200 / (self.max_value - self.min_value))
        painter.setBrush(QColor('purple'))
        painter.drawRect(35, y, 90, 230 - y)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(15, y - 10, str(self.value) + self.unit)


# 功率计类
class PowerMeter(InstrumentBase):
    def __init__(self, value=1000, min_value=0, max_value=2000, unit='W'):
        super().__init__()
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_value)
        self.timer.start(2000)

    def update_value(self):
        self.value = (self.value + 100) % (self.max_value + 1)
        self.update()

    def draw_background(self, painter):
        center = self.rect().center()
        painter.drawEllipse(center, 70, 70)
        painter.setFont(QFont('Arial', 10, QFont.Bold))
        painter.setPen(QColor('lightgray'))
        for i in range(self.min_value, self.max_value + 1, 200):
            angle = self.value_to_angle(i)
            x = center.x() + 60 * math.sin(angle)
            y = center.y() - 60 * math.cos(angle)
            painter.drawText(x - 20, y + 5, str(i) + self.unit)

    def value_to_angle(self, value):
        return (value - self.min_value) / (self.max_value - self.min_value) * 2 * math.pi - math.pi / 2

    def draw_indicator(self, painter):
        center = self.rect().center()
        radius = 60
        angle = self.value_to_angle(self.value)
        x_end = center.x() + radius * math.sin(angle)
        y_end = center.y() - radius * math.cos(angle)
        painter.setPen(QPen(Qt.darkYellow, 3))
        painter.drawLine(center.x(), center.y(), x_end, y_end)
        painter.setFont(QFont('Arial', 12, QFont.Bold))
        painter.setPen(QColor('white'))
        painter.drawText(center.x() - 30, center.y() + 80, '功率:'+ str(self.value) + self.unit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    layout = QGridLayout()
    widgets = [
        Gauge(value=60),
        Thermometer(value=30),
        Manometer(value=1.5),
        Voltmeter(value=250),
        Ammeter(value=7),
        LevelMeter(value=70),
        FlowMeter(value=150),
        Tachometer(value=1500),
        Hygrometer(value=60),
        PowerMeter(value=1500)
    ]
    row, col = 0, 0
    for widget in widgets:
        layout.addWidget(widget, row, col)
        col += 1
        if col == 5:
            col = 0
            row += 1
    main_widget = QWidget()
    main_widget.setLayout(layout)
    main_widget.show()
    sys.exit(app.exec_())