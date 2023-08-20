import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QEvent, QCoreApplication
from PyQt5.QtGui import QIcon, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QMenu, QSystemTrayIcon, QAction

from Cat import Cat
from SpeechBubble import SpeechBubble
from UserInputWindow import UserInputWindow


class CatWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.drag_position = None
        self.controller = controller
        self.cat_widget = Cat(self)
        self.setCentralWidget(self.cat_widget)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool | Qt.FramelessWindowHint)
        self.dragging = False
        self.resize(self.cat_widget.width(), self.cat_widget.height())

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        close_action = context_menu.addAction("Close")
        close_action.triggered.connect(self.controller.closeAllWindows)
        context_menu.exec_(event.globalPos())

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.controller.user_input_window.isHidden():
                self.controller.user_input_window.showContent()
                self.controller.updateUserInputPosition()
            else:
                self.controller.user_input_window.hideContent()
        super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.controller.updateSpeechBubblePosition()
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)

    def moveEvent(self, event):
        # Update the speech bubble window's position when the cat window is moved
        if self.dragging:
            self.controller.updateSpeechBubblePosition()
            self.controller.updateUserInputPosition()
        super().moveEvent(event)


class SpeechBubbleWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.speech_bubble_widget = SpeechBubble(self)
        self.setCentralWidget(self.speech_bubble_widget)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)


class Controller:
    def __init__(self):
        self.cat_window = CatWindow(self)
        self.cat_window.show()
        self.speech_bubble_window = SpeechBubbleWindow(self)

        self.user_input_window = UserInputWindow(self)

        self.tray_icon = QSystemTrayIcon(QIcon("assets/cat/angry.png"), self.cat_window)
        tray_menu = QMenu()
        show_action = QAction("Show", self.cat_window)
        show_action.triggered.connect(self.showAllWindows)
        tray_menu.addAction(show_action)
        hide_action = QAction("Hide", self.cat_window)
        hide_action.triggered.connect(self.hideAllWindows)
        tray_menu.addAction(hide_action)
        close_action = QAction("Close", self.cat_window)
        close_action.triggered.connect(self.closeAllWindows)
        tray_menu.addAction(close_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.speech_bubble_window.speech_bubble_widget.setText("Meow!")

    def updateUserInputPosition(self):
        x = self.cat_window.x() + (self.cat_window.cat_widget.pixmap().width() - self.user_input_window.width()) // 2
        y = self.cat_window.y() + self.cat_window.height()
        self.user_input_window.move(x, y)

    def updateSpeechBubblePosition(self):
        x = self.cat_window.x() + (self.cat_window.cat_widget.pixmap().width() - self.speech_bubble_window.width()) // 2
        y = (
            self.cat_window.y()
            - self.speech_bubble_window.speech_bubble_widget.bubble_pixmap.height()
        )
        self.speech_bubble_window.move(x, y)

    def showAllWindows(self):
        self.cat_window.show()
        self.speech_bubble_window.show()

    def hideAllWindows(self):
        self.cat_window.hide()
        self.speech_bubble_window.hide()

    def closeAllWindows(self):
        self.cat_window.close()
        self.speech_bubble_window.close()
        QCoreApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window_ctrl = Controller()
    window_ctrl.updateSpeechBubblePosition()
    sys.exit(app.exec_())
