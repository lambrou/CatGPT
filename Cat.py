from PyQt5 import QtWidgets, QtGui, QtCore


class Cat(QtWidgets.QLabel):
    def __init__(self, window):
        super().__init__()

        # Load all the cat images
        self.states = {
            "angry": QtGui.QPixmap("assets/cat/angry.png"),
            "idle": [QtGui.QPixmap(f"assets/cat/idle{i}.png") for i in range(1, 5)],
            "sleeping": [
                QtGui.QPixmap(f"assets/cat/sleeping{i}.png") for i in range(1, 7)
            ],
            "walking_left": [
                QtGui.QPixmap(f"assets/cat/walkingleft{i}.png") for i in range(1, 5)
            ],
            "walking_right": [
                QtGui.QPixmap(f"assets/cat/walkingright{i}.png") for i in range(1, 5)
            ],
            "zzz": [QtGui.QPixmap(f"assets/cat/zzz{i}.png") for i in range(1, 5)],
            "thinking": [
                QtGui.QPixmap(f"assets/cat/think{i}.png") for i in range(1, 5)
            ]
        }

        self.w = window

        # Set initial state
        self.current_state = "idle"
        self.prev_state = "idle"
        self.current_frame = 0

        # Set the initial pixmap
        self.setPixmap(self.states["idle"][0])
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(self.pixmap().size())
        self.setAlignment(QtCore.Qt.AlignCenter)

        # Timer for animations
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(500)  # Adjust the interval for animation speed

    def animate(self):
        if self.current_state == "idle":
            if self.prev_state != "idle":
                self.prev_state = "idle"
            self.current_frame = (self.current_frame + 1) % len(self.states["idle"])
            self.setPixmap(self.states["idle"][self.current_frame])
        elif self.current_state == "sleeping":
            if self.prev_state != "sleeping":
                self.prev_state = "sleeping"
            self.current_frame = (self.current_frame + 1) % len(self.states["sleeping"])
            self.setPixmap(self.states["sleeping"][self.current_frame])
        elif self.current_state == "thinking":
            if self.prev_state != "thinking":
                self.prev_state = "thinking"
            self.current_frame = (self.current_frame + 1) % len(self.states["thinking"])
            self.setPixmap(self.states["thinking"][self.current_frame])

    def wakeUp(self):
        self.current_state = "idle"
        self.current_frame = 0

    def goToSleep(self):
        self.current_state = "sleeping"
        self.current_frame = 0

    def think(self):
        self.current_state = "thinking"
        self.current_frame = 0

    def stopThinking(self):
        self.current_state = "idle"
        self.current_frame = 0
