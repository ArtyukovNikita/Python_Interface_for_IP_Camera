import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

class CameraApp(QWidget):
    def __init__(self, camera_url):
        super().__init__()
        self.camera_url = camera_url
        self.is_recording = False
        self.initUI()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.capture = cv2.VideoCapture(self.camera_url, cv2.CAP_FFMPEG)
        if not self.capture.isOpened():
            print("Не удалось подключиться к камере.")
            sys.exit()

        print("Подключение к камере успешно.")
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        self.out = None

    def initUI(self):
        self.setWindowTitle('IP Camera Stream')
        self.layout = QHBoxLayout()  # Основной горизонтальный layout

        # QLabel для отображения видео
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)

        # Создаем вертикальный layout для кнопки записи
        left_control_layout = QVBoxLayout()
        self.record_button = QPushButton('🔴')
        self.record_button.setFixedSize(60, 60)  # Устанавливаем фиксированный размер для кнопки записи (квадрат)
        self.record_button.clicked.connect(self.toggle_recording)
        left_control_layout.addWidget(self.record_button)

        # Создаем вертикальный layout для кнопок управления
        right_control_layout = QVBoxLayout()
        button_layout = QGridLayout()
        self.forward_button = QPushButton('↑')
        self.backward_button = QPushButton('↓')
        self.right_button = QPushButton('→')
        self.left_button = QPushButton('←')

        # Устанавливаем размеры кнопок
        for button in [self.forward_button, self.backward_button, self.right_button, self.left_button]:
            button.setFixedSize(40, 40)

        # Располагаем кнопки управления
        button_layout.addWidget(self.left_button, 0, 0)
        button_layout.addWidget(self.forward_button, 0, 1)
        button_layout.addWidget(self.right_button, 0, 2)
        button_layout.addWidget(self.backward_button, 1, 1)

        right_control_layout.addLayout(button_layout)

        # Добавляем элементы в основной layout
        self.layout.addLayout(left_control_layout)  # Сначала добавляем кнопку записи
        self.layout.addWidget(self.image_label)      # Затем добавляем изображение
        self.layout.addLayout(right_control_layout)  # Затем добавляем кнопки управления

        self.setLayout(self.layout)

        # Подключаем обработчики нажатий для кнопок
        self.left_button.clicked.connect(self.move_left)
        self.right_button.clicked.connect(self.move_right)
        self.forward_button.clicked.connect(self.move_forward)
        self.backward_button.clicked.connect(self.move_backward)

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            print("Ошибка захвата кадра.")
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Растягиваем изображение до размеров QLabel
        self.image_label.setPixmap(
            pixmap.scaled(self.image_label.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        if self.is_recording:
            if self.out is None:
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (w, h))
            self.out.write(frame)
        else:
            if self.out is not None:
                self.out.release()
                self.out = None

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        self.record_button.setText('🛑' if self.is_recording else '🔴')

    def move_left(self):
        print("Нажата кнопка влево")

    def move_right(self):
        print("Нажата кнопка вправо")

    def move_forward(self):
        print("Нажата кнопка вверх")

    def move_backward(self):
        print("Нажата кнопка вниз")

    def resizeEvent(self, event):
        if self.image_label.pixmap() is not None:
            self.image_label.setPixmap(self.image_label.pixmap().scaled(self.image_label.size(), Qt.IgnoreAspectRatio,
                                                                        Qt.SmoothTransformation))
        super().resizeEvent(event)

    def closeEvent(self, event):
        if self.out is not None:
            self.out.release()
        self.capture.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    camera_url = 'rtsp://admin:Admin123@192.168.1.100:554/Streaming/Channels/101'  # Обновите IP на актуальный
    ex = CameraApp(camera_url)
    ex.show()
    sys.exit(app.exec_())
