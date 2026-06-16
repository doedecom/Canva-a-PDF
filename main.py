import re
import sys
import os

import qdarkstyle
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QFileDialog, QVBoxLayout,
    QHBoxLayout, QMessageBox, QSpinBox,
    QProgressBar
)

from PyQt5.QtCore import QThread, pyqtSignal

from playwright.sync_api import sync_playwright
from pypdf import PdfWriter

"""
La tarde se apago sin dejar calor,
y en el silencio quedo mi dolor.
Busque tu recuerdo con temor,
perdido entre sombras, lejos de Ecuador.

... .. ..
"""

class Worker(QThread):
    progreso = pyqtSignal(int)
    terminado = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
            self,
            url,
            carpeta,
            nombre_pdf,
            slide_inicio,
            slide_fin,
            espera_ms
    ):
        super().__init__()

        self.url = url
        self.carpeta = carpeta
        self.nombre_pdf = nombre_pdf
        self.slide_inicio = slide_inicio
        self.slide_fin = slide_fin
        self.espera_ms = espera_ms

    def run(self):
        try:
            pdfs = []

            with sync_playwright() as p:

                browser = p.chromium.launch(
                    executable_path=resource_path(
                        "chrome-win/chrome.exe"
                    ),
                    headless=True
                )
                page = browser.new_page()

                total = self.slide_fin - self.slide_inicio + 1

                for indice, slide in enumerate(
                        range(self.slide_inicio, self.slide_fin + 1),
                        start=1
                ):

                    page.goto(
                        f"{self.url}#{slide}",
                        wait_until="domcontentloaded"
                    )

                    page.wait_for_load_state("networkidle")

                    page.wait_for_function(
                        "() => Array.from(document.images).every(img => img.complete)"
                    )

                    page.wait_for_timeout(self.espera_ms)

                    pdf_path = os.path.join(
                        self.carpeta,
                        f"slide_{slide}.pdf"
                    )

                    page.pdf(
                        path=pdf_path,
                        format="A4",
                        landscape=True,
                        print_background=True
                    )

                    pdfs.append(pdf_path)

                    porcentaje = int(
                        (indice / total) * 100
                    )

                    self.progreso.emit(porcentaje)

                page.close()
                browser.close()

            writer = PdfWriter()

            for pdf in pdfs:
                writer.append(pdf)

            pdf_final = os.path.join(
                self.carpeta,
                f"{self.nombre_pdf}.pdf"
            )

            with open(pdf_final, "wb") as salida:
                writer.write(salida)

            writer.close()

            self.terminado.emit(pdf_final)

        except Exception as e:
            self.error.emit(str(e))


class Ventana(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Canva a PDF")
        self.setFixedSize(600, 400)


        layout = QVBoxLayout()

        # URL
        layout.addWidget(QLabel("Enlace Canva:"))

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(
            "https://www.canva.com/design/.../view"
        )
        layout.addWidget(self.txt_url)

        # Carpeta
        layout.addWidget(QLabel("Carpeta destino:"))

        h_carpeta = QHBoxLayout()

        self.txt_carpeta = QLineEdit()

        btn_carpeta = QPushButton("Examinar")
        btn_carpeta.clicked.connect(
            self.seleccionar_carpeta
        )

        h_carpeta.addWidget(self.txt_carpeta)
        h_carpeta.addWidget(btn_carpeta)

        layout.addLayout(h_carpeta)

        # Nombre PDF
        layout.addWidget(QLabel("Nombre PDF final:"))

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setText("presentacion_completa")

        layout.addWidget(self.txt_nombre)

        # Rango de diapositivas
        layout.addWidget(QLabel("Rango de diapositivas:"))

        h_rango = QHBoxLayout()

        self.spin_inicio = QSpinBox()
        self.spin_inicio.setRange(1, 10000)
        self.spin_inicio.setValue(1)

        self.spin_fin = QSpinBox()
        self.spin_fin.setRange(1, 10000)
        self.spin_fin.setValue(60)

        h_rango.addWidget(QLabel("Desde"))
        h_rango.addWidget(self.spin_inicio)

        h_rango.addWidget(QLabel("Hasta"))
        h_rango.addWidget(self.spin_fin)

        layout.addLayout(h_rango)

        # Tiempo espera
        layout.addWidget(
            QLabel("Tiempo espera Canva (ms):")
        )

        self.spin_espera = QSpinBox()
        self.spin_espera.setRange(0, 60000)
        self.spin_espera.setValue(3000)

        layout.addWidget(self.spin_espera)

        # Barra progreso
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Botón iniciar
        self.btn_generar = QPushButton(
            "Generar PDF"
        )

        self.btn_generar.clicked.connect(
            self.generar_pdf
        )

        layout.addWidget(self.btn_generar)

        self.setLayout(layout)

    def seleccionar_carpeta(self):

        carpeta = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta"
        )

        if carpeta:
            self.txt_carpeta.setText(carpeta)

    def generar_pdf(self):

        inicio = self.spin_inicio.value()
        fin = self.spin_fin.value()

        if inicio > fin:
            QMessageBox.warning(
                self,
                "Error",
                "La diapositiva inicial no puede ser mayor que la final."
            )
            return

        url = self.txt_url.text().strip()
        carpeta = self.txt_carpeta.text().strip()
        nombre = self.txt_nombre.text().strip()

        if not url:
            QMessageBox.warning(
                self,
                "Error",
                "Ingrese una URL."
            )
            return

        url = re.sub(r"#\d+$", "", url)

        if not carpeta:
            QMessageBox.warning(
                self,
                "Error",
                "Seleccione una carpeta."
            )
            return

        if not nombre:
            QMessageBox.warning(
                self,
                "Error",
                "No se a declaro un nombre al PDF final."
            )
            return

        self.btn_generar.setEnabled(False)

        self.worker = Worker(
            url=url,
            carpeta=carpeta,
            nombre_pdf=nombre,
            slide_inicio=inicio,
            slide_fin=fin,
            espera_ms=self.spin_espera.value()
        )

        self.worker.progreso.connect(
            self.progress.setValue
        )

        self.worker.terminado.connect(
            self.proceso_terminado
        )

        self.worker.error.connect(
            self.proceso_error
        )

        self.worker.start()

    def proceso_terminado(self, pdf):

        self.btn_generar.setEnabled(True)

        respuesta = QMessageBox.information(
            self,
            "Completado",
            f"PDF generado:\n\n{pdf}",
            QMessageBox.Ok
        )

        if respuesta == QMessageBox.Ok:
            os.startfile(pdf)

    def proceso_error(self, mensaje):

        self.btn_generar.setEnabled(True)

        QMessageBox.critical(
            self,
            "Error",
            mensaje
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyleSheet(
        qdarkstyle.load_stylesheet(qt_api='pyqt5')
    )


    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    app.setWindowIcon(
        QIcon(resource_path("icon.ico"))
    )

    app.setFont(QFont("Bahnschrift", 11))

    ventana = Ventana()
    ventana.show()

    sys.exit(app.exec_())