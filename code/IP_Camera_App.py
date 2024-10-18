import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class IP_Camera_App(QMainWindow):
    def __init__(self, ip_address):
        super().__init__()
        self.setWindowTitle("IP Camera Viewer")

        self.video_source = ip_address
        self.vid = cv2.VideoCapture(self.video_source)

        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)

        self.btn1 = QPushButton("Кнопка 1", self)
        self.btn1.clicked.connect(self.button1_action)

        self.btn2 = QPushButton("Кнопка 2", self)
        self.btn2.clicked.connect(self.button2_action)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout
        self.timer.timeout.connect(self.update)
        self.timer.start(30)  # Обновление каждые 30 мс

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

    def button1_action(self):
        print("Кнопка 1 нажата")

    def button2_action(self):
        print("Кнопка 2 нажата")

    def closeEvent(self, event):
        self.vid.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ip_address = "http://<ваш_ip_адрес_камеры>/video"  # Замените на адрес вашей IP-камеры
    window = IP_Camera_App(ip_address)
    window.show()
    sys.exit(app.exec_())
