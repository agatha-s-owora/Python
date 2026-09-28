from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from datetime import *
from gui import *
from pygame import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        mixer.init()    # Here to be accessible in entire class

        # Configuring the main timer
        self.main_timer = QTimer()
        self.alarm_time = "00:00:00"
        self.main_timer.timeout.connect(self.update_main_date_time)
        self.main_timer.start(1000)  # start timer and update every second
        self.update_main_date_time()

        # Configuring the alarm clock
        self.button_alarm_set.clicked.connect(lambda: self.update_alarm("set"))
        self.button_alarm_clear.clicked.connect(lambda: self.update_alarm("clear"))

        # Configuring the stopwatch timer
        self.stopwatch_time = QTime(0,0,0,0)
        self.stopwatch_timer = QTimer()
        self.stopwatch_timer.timeout.connect(self.update_stopwatch_display)
        self.button_stop_start.clicked.connect(lambda: self.update_stopwatch("start"))
        self.button_stop_stop.clicked.connect(lambda: self.update_stopwatch("stop"))
        self.button_stop_reset.clicked.connect(lambda: self.update_stopwatch("reset"))

        # Configuring the countdown timer
        self.countdown_remaining_seconds = 0
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown_display)
        self.button_countdown_start.clicked.connect(lambda: self.update_countdown("start"))
        self.button_countdown_stop.clicked.connect(lambda: self.update_countdown("stop"))
        self.button_countdown_reset.clicked.connect(lambda: self.update_countdown("reset"))

    def update_main_date_time(self):
        current_date = datetime.now()
        current_day = current_date.strftime("%A, %d %B, %Y")
        self.label_date.setText(str(current_day))
        current_time = current_date.strftime("%I:%M:%S %p")
        self.label_time.setText(current_time)

        # Check if it is time for alarm
        if self.alarm_time == str(current_time):
            self.label_alarm.setText("WAKE UP!!!")
            mixer.music.load("alarm.mp3")
            mixer.music.play()

    def update_alarm(self, state):
        if state == "set":
            self.alarm_time = str(self.timeedit_alarm.time().toPyTime().strftime("%I:%M:%S %p"))
            self.label_alarm.setText(f"Alarm set for: {self.alarm_time}")
        elif state == "clear":
            if mixer.music.get_busy():
                mixer.music.stop()
            self.timeedit_alarm.setTime(QTime(0, 0))
            self.label_alarm.setText("No Alarm Set!!")

    def update_stopwatch(self, action):
        if action == "start":
            self.stopwatch_timer.start(10)
        elif action == "stop":
            self.stopwatch_timer.stop()
        elif action == "reset":
            self.stopwatch_timer.stop()
            self.stopwatch_time = QTime(0,0,0,0)
            self.label_stopwatch.setText("00:00:00:00")

    def update_stopwatch_display(self):
        self.stopwatch_time = self.stopwatch_time.addMSecs(10)
        hours = self.stopwatch_time.hour()
        minutes = self.stopwatch_time.minute()
        seconds = self.stopwatch_time.second()
        milliseconds = self.stopwatch_time.msec() // 10
        self.label_stopwatch.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:02d}")

    def update_countdown(self, action):
        if action == "start":
            hours = self.spinbox_hrs.value() * 3600
            minutes = self.spinbox_mins.value() * 60
            seconds = self.spinbox_secs.value()
            self.countdown_remaining_seconds = hours + minutes + seconds
            self.countdown_timer.start(1000)
        elif action == "stop":
            self.countdown_timer.stop()
        elif action == "reset":
            self.countdown_timer.stop()
            self.countdown_remaining_seconds = 0
            self.spinbox_hrs.setValue(0)
            self.spinbox_mins.setValue(0)
            self.spinbox_secs.setValue(0)
            self.label_countdown.setText("00:00:00")

    def update_countdown_display(self):
        if self.countdown_remaining_seconds > 0:
            hours = self.countdown_remaining_seconds // 3600
            minutes = (self.countdown_remaining_seconds % 3600) // 60
            seconds = self.countdown_remaining_seconds % 60
            self.label_countdown.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.countdown_remaining_seconds -= 1
        else:
            self.countdown_timer.stop()
            self.label_countdown.setText("00:00:00")