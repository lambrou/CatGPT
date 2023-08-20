from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QTextOption, QFontMetrics
from PyQt5.QtWidgets import (
    QGraphicsOpacityEffect,
    QWidget,
    QTextEdit,
    QFrame,
    QVBoxLayout, QPushButton, QScrollArea,
)


class SpeechBubble(QWidget):
    def __init__(self, window):
        super().__init__()

        self.scroll_area = None
        self.text = "Meow!"
        self.w = window

        self.font = None
        self.fill = None
        self.bottom_right = None
        self.bottom_center = None
        self.bottom_left = None
        self.right_edge = None
        self.left_edge = None
        self.top_right = None
        self.top_center = None
        self.top_left = None
        self.font = QtGui.QFont("Arial", 12)  # Example font

        self.bubble_scale_factor = 2
        self.fixed_width = 280
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        # Create the fade-in and fade-out animations
        self.fade_in_animation = QtCore.QPropertyAnimation(
            self.opacity_effect, b"opacity"
        )
        self.fade_in_animation.setDuration(5000)  # 1 second
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)

        self.fade_out_animation = QtCore.QPropertyAnimation(
            self.opacity_effect, b"opacity"
        )
        self.fade_out_animation.setDuration(1000)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        # Load the nine-slice images
        self.loadNineSlice()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.text_edit.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.text_edit.setWordWrapMode(QTextOption.WordWrap)
        self.text_edit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.text_edit.setStyleSheet(
            "background: transparent; border: none; font-size: 12px; color: black;"
        )

        self.hide_button = QPushButton("👁")  # Using a UTF-8 close symbol
        self.hide_button.clicked.connect(self.fadeOut)  # Connect the button's clicked signal to the hide method
        self.hide_button.setFixedSize(15, 15)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.hide_button)
        self.setLayout(layout)

        self.bubble_pixmap = None
        self.setAutoFillBackground(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.show()
        self.w.move(self.w.controller.cat_window.x(), self.w.controller.cat_window.y())

    def setText(self, text):
        if self.isVisible():
            self.fadeOut()
        else:
            self.w.show()
        self.text = text
        self.text_edit.setText(self.text)
        self.updateLayout()
        self.bubble_pixmap = self.createSpeechBubble()

        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(self.bubble_pixmap))
        self.setPalette(palette)
        self.setFixedSize(self.bubble_pixmap.size())
        self.w.controller.updateSpeechBubblePosition()
        self.fadeIn()
        self.show()

    def fadeIn(self):
        self.w.show()
        self.fade_out_animation.stop()
        self.fade_in_animation.start()

    def fadeOut(self):
        self.fade_in_animation.stop()
        self.fade_out_animation.start()
        self.fade_out_animation.finished.connect(self.w.hide)

    def loadNineSlice(self):
        self.top_left = QPixmap("assets/speechbubble/nine_slice/top_left.png")
        self.top_left = self.top_left.scaled(
            self.top_left.width() // self.bubble_scale_factor,
            self.top_left.height() // self.bubble_scale_factor,
        )
        self.top_center = QPixmap("assets/speechbubble/nine_slice/top_center.png")
        self.top_center = self.top_center.scaled(
            self.top_center.width() // self.bubble_scale_factor,
            self.top_center.height() // self.bubble_scale_factor,
        )
        self.top_right = QPixmap("assets/speechbubble/nine_slice/top_right.png")
        self.top_right = self.top_right.scaled(
            self.top_right.width() // self.bubble_scale_factor,
            self.top_right.height() // self.bubble_scale_factor,
        )
        self.left_edge = QPixmap("assets/speechbubble/nine_slice/left_edge.png")
        self.left_edge = self.left_edge.scaled(
            self.left_edge.width() // self.bubble_scale_factor,
            self.left_edge.height() // self.bubble_scale_factor,
        )
        self.right_edge = QPixmap("assets/speechbubble/nine_slice/right_edge.png")
        self.right_edge = self.right_edge.scaled(
            self.right_edge.width() // self.bubble_scale_factor,
            self.right_edge.height() // self.bubble_scale_factor,
        )
        self.bottom_left = QPixmap("assets/speechbubble/nine_slice/bottom_left.png")
        self.bottom_left = self.bottom_left.scaled(
            self.bottom_left.width() // self.bubble_scale_factor,
            self.bottom_left.height() // self.bubble_scale_factor,
        )
        self.bottom_center = QPixmap("assets/speechbubble/nine_slice/bottom_center.png")
        self.bottom_center = self.bottom_center.scaled(
            self.bottom_center.width() // self.bubble_scale_factor,
            self.bottom_center.height() // self.bubble_scale_factor,
        )
        self.bottom_right = QPixmap("assets/speechbubble/nine_slice/bottom_right.png")
        self.bottom_right = self.bottom_right.scaled(
            self.bottom_right.width() // self.bubble_scale_factor,
            self.bottom_right.height() // self.bubble_scale_factor,
        )
        self.fill = QPixmap("assets/speechbubble/nine_slice/fill.png")
        self.fill = self.fill.scaled(
            self.fill.width() // self.bubble_scale_factor,
            self.fill.height() // self.bubble_scale_factor,
        )

    def createSpeechBubble(self):
        self.font = QtGui.QFont("Arial", 12)  # Example font
        font_metrics = QtGui.QFontMetrics(self.font)
        max_text_height = 300 - self.top_left.height() - self.bottom_left.height()
        text_rect = font_metrics.boundingRect(
            0, 0, self.fixed_width, max_text_height, Qt.TextWordWrap, self.text
        )
        height = min(text_rect.height(), max_text_height) + self.top_left.height() + self.bottom_left.height()
        pixmap = QtGui.QPixmap(self.fixed_width, height)
        pixmap.fill(Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setFont(self.font)
        painter.drawPixmap(0, 0, self.top_left)
        painter.drawPixmap(
            self.top_left.width(),
            0,
            self.fixed_width - self.top_left.width() - self.top_right.width(),
            self.top_center.height(),
            self.top_center,
        )
        painter.drawPixmap(self.fixed_width - self.top_right.width(), 0, self.top_right)
        painter.drawPixmap(
            0,
            self.top_left.height(),
            self.left_edge.width(),
            height - self.top_left.height() - self.bottom_left.height(),
            self.left_edge,
        )
        painter.drawPixmap(
            self.left_edge.width(),
            self.top_left.height(),
            self.fixed_width - self.left_edge.width() - self.right_edge.width(),
            height - self.top_left.height() - self.bottom_left.height(),
            self.fill,
        )
        painter.drawPixmap(
            self.fixed_width - self.right_edge.width(),
            self.top_left.height(),
            self.right_edge.width(),
            height - self.top_left.height() - self.bottom_left.height(),
            self.right_edge,
        )
        painter.drawPixmap(0, height - self.bottom_left.height(), self.bottom_left)
        painter.drawPixmap(
            self.bottom_left.width(),
            height - self.bottom_left.height(),
            self.fixed_width - self.bottom_left.width() - self.bottom_right.width(),
            self.bottom_center.height(),
            self.bottom_center,
        )
        painter.drawPixmap(
            self.fixed_width - self.bottom_right.width(),
            height - self.bottom_right.height(),
            self.bottom_right,
        )
        painter.end()
        return pixmap

    def updateLayout(self):
        # Check if the content height exceeds the maximum height
        font_metrics = QtGui.QFontMetrics(self.font)
        max_text_height = 600 - self.top_left.height() - self.bottom_left.height()
        text_rect = font_metrics.boundingRect(
            0, 0, self.fixed_width, max_text_height, Qt.TextWordWrap, self.text
        )

        if text_rect.height() > max_text_height:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        else:
            self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)