import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QApplication, QPushButton


class PainterCanvas(QWidget):
    painter_pixmap_width = 1000
    painter_pixmap_height = 800
    def __init__(self):
        super().__init__()
        self.setMouseTracking(False)
        self.painter = QPainter()

        self.pen = QPen(Qt.black, 7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.grid = QGridLayout()
        self.lb = QLabel()
        self.grid.addWidget(self.lb)
        self.pixmap = QPixmap(self.painter_pixmap_width, self.painter_pixmap_height)
        self.pixmap.fill(Qt.white)
        self.lb.setPixmap(self.pixmap)
        self.old_x = 0
        self.old_y = 0
        self.setLayout(self.grid)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear)
        self.grid.addWidget(self.clear_btn)
        self.setWindowTitle("签名测试")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.resize(self.painter_pixmap_width, self.painter_pixmap_height)

    def mouseMoveEvent(self, event):
        self.painter.begin(self.pixmap)  #
        self.painter.setPen(self.pen)
        if self.check():
            self.painter.drawLine(event.pos().x() - 10, event.pos().y() - 10, event.pos().x() - 10,
                                  event.pos().y() - 10)
        else:
            self.painter.drawLine(self.old_x, self.old_y, event.pos().x() - 10, event.pos().y() - 10)
        self.painter.end()
        self.lb.setPixmap(self.pixmap)
        self.old_x = event.pos().x() - 10
        self.old_y = event.pos().y() - 10

    def mousePressEvent(self, event):
        self.painter.begin(self.pixmap)
        self.painter.setPen(self.pen)
        self.painter.drawPoint(event.pos().x() - 10, event.pos().y() - 10)
        self.painter.end()
        self.lb.setPixmap(self.pixmap)
        self.old_x = event.pos().x() - 10
        self.old_y = event.pos().y() - 10

    def check(self):
        return self.old_x == 0 and self.old_y == 0

    def mouseReleaseEvent(self, event):
        self.old_x = 0
        self.old_y = 0

    # 重置签名
    def clear(self):
        self.pixmap = QPixmap(self.painter_pixmap_width, self.painter_pixmap_height)
        self.pixmap.fill(Qt.white)
        self.lb.setPixmap(self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = PainterCanvas()
    a.show()

    sys.exit(app.exec_())
