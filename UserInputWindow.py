from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import (
    QMainWindow,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTextEdit,
)

from CatGPTAgent import CatGPTAgent, CatResponseThread


class UserInputWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.response_thread = None
        self.controller = controller

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setFixedSize(300, 300)
        self.text_input = QTextEdit(self)
        self.text_input.setFixedHeight(200)
        self.text_input.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.onSubmit)
        self.resizing = False

        layout = QVBoxLayout()
        layout.addWidget(self.text_input)
        layout.addWidget(self.submit_button)
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        hide_button = QPushButton("👁")
        hide_button.setFixedSize(30, 30)
        hide_button.clicked.connect(
            self.hideContent
        )
        layout.addWidget(hide_button)
        self.cat_gpt = CatGPTAgent()

    def hideContent(self):
        self.hide()

    def showContent(self):
        self.show()

    def onSubmit(self):
        text = self.text_input.toPlainText()
        self.controller.cat_window.cat_widget.think()
        self.response_thread = CatResponseThread(self.cat_gpt, text)
        self.response_thread.finished.connect(self.cleanupThread)  # Connect the finished signal
        self.response_thread.response_signal.connect(self.handleCatResponse)
        self.response_thread.start()

    def handleCatResponse(self, cat_response):
        self.controller.speech_bubble_window.speech_bubble_widget.setText(cat_response)
        self.controller.cat_window.cat_widget.stopThinking()
        self.controller.updateSpeechBubblePosition()

    def cleanupThread(self):
        self.response_thread.quit()
        self.response_thread.wait()
        self.response_thread.deleteLater()
        self.response_thread = None

class ResizeWidget(QWidget):
    def mousePressEvent(self, event):
        self.parent().resizing = True
        self.parent().oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.parent().resizing:
            delta = QPoint(event.globalPos() - self.parent().oldPos)
            self.parent().resize(self.parent().width() + delta.x(), self.parent().height() + delta.y())
            self.parent().oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.parent().resizing = False