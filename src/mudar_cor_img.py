import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageFilterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor de Imagens - PyQt5")
        self.image = None  # imagem original
        self.filtered_image = None  # imagem processada

        # Centralizar na tela
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(
            (screen.width() - 720) // 2,
            (screen.height() - 600) // 2,
            720,
            600
        )

        # Widgets principais (20% maior e padding 10% extra)
        self.image_label = QLabel("Nenhuma imagem carregada")
        self.image_label.setFixedSize(660, 456)
        self.image_label.setStyleSheet("""
            border: 2px solid #26A69A;
            border-radius: 12px;
            background-color: #1E1E1E;
            padding: 22px;
            color: #AAAAAA;
        """)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.btn_load = QPushButton("Carregar Imagem")
        self.btn_load.clicked.connect(self.load_image)
        self.btn_load.setFixedHeight(44)
        self.btn_load.setStyleSheet("""
            QPushButton {
                background-color: #26A69A;
                color: #FFFFFF;
                font-weight: bold;
                border-radius: 20px;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2BBBAD;
            }
        """)

        self.combo_filters = QComboBox()
        self.combo_filters.addItems([
            "Original", "Escala de Cinza", "Inversão de Cores",
            "Filtro de Borrado", "Detecção de Bordas"
        ])
        self.combo_filters.currentIndexChanged.connect(self.apply_filter)
        self.combo_filters.setStyleSheet("""
            QComboBox {
                background-color: #2C2C2C;
                color: #EAEAEA;
                border: 1px solid #26A69A;
                border-radius: 10px;
                padding: 8px;
                font-size: 13px;
            }
            QComboBox QAbstractItemView {
                background-color: #1E1E1E;
                selection-background-color: #26A69A;
                color: #EAEAEA;
            }
        """)

        # Layout (dark mode)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        layout.addSpacing(18)
        layout.addWidget(self.btn_load)
        layout.addSpacing(12)
        layout.addWidget(self.combo_filters)
        self.setLayout(layout)

        # Fundo da janela no modo escuro
        self.setStyleSheet("background-color: #121212;")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Abrir Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.image = cv2.imread(file_name)
            self.filtered_image = self.image.copy()
            self.show_image(self.image)

    def show_image(self, img):
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Ajustar mantendo proporção
        pixmap = pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)

    def apply_filter(self):
        if self.image is None:
            return

        choice = self.combo_filters.currentText()

        if choice == "Original":
            self.filtered_image = self.image.copy()
        elif choice == "Escala de Cinza":
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.filtered_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        elif choice == "Inversão de Cores":
            self.filtered_image = cv2.bitwise_not(self.image)
        elif choice == "Filtro de Borrado":
            self.filtered_image = cv2.GaussianBlur(self.image, (15, 15), 0)
        elif choice == "Detecção de Bordas":
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.filtered_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        self.show_image(self.filtered_image)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec_())
