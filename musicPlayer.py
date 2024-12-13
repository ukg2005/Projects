import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QInputDialog)
from PyQt5.Qt import Qt
import pygame

# if you are trying to run the program bring the playlist into the same directory
# otherwise doesn't work as intended

class music_Player(QWidget):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.playlist = ["playlist/song1.mp3", "playlist/song2.mp3", "playlist/song3.mp3"]
        self.current_index = 0
        self.music_label = QLabel("Song", self)
        self.prev_button = QPushButton("prev", self)
        self.pause_button = QPushButton("pause", self)
        self.next_button = QPushButton("next", self)
        self.music_paused= False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Music Player")
        self.setGeometry(300, 300, 500, 300)

        vbox = QVBoxLayout()
        vbox.addWidget(self.music_label)
        self.setLayout(vbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.prev_button)
        hbox.addWidget(self.pause_button)
        hbox.addWidget(self.next_button)
        vbox.addLayout(hbox)

        self.music_label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibre;
            }
            QLabel {
                font-size: 40px;
                font-style: italic;
                font-weight: bold;
            }
            QPushButton{
                font-size: 40px;
                border: 1px solid black;
            }
            QPushButton:hover{
                background-color: hsl(83, 1%, 58%);
            }
        """)

        self.prev_button.clicked.connect(self.play_prev)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.next_button.clicked.connect(self.play_next)

        self.update_button_state()

    def load_song(self):
        if self.playlist:
            song = self.playlist[self.current_index]
            pygame.mixer.music.load(song)
            self.music_label.setText(song.split("/")[-1])
            self.play_song()
        else:
            self.music_label.setText("Playlist is Empty")

    def play_song(self):
        pygame.mixer.music.play()
        self.music_label.setText(f"Playing: {self.playlist[self.current_index].split('/')[-1]}")

    def play_prev(self):
        if self.current_index != 0:
            self.current_index -= 1
            self.load_song()
            self.play_song()
        self.update_button_state()

    def toggle_pause(self):
        if not pygame.mixer.music.get_busy() and not self.music_paused:
            return
        if not self.music_paused:
            pygame.mixer.music.pause()
            self.pause_button.setText("play")
            self.music_label.setText("Paused")
            self.music_paused = True
        else:
            pygame.mixer.music.unpause()
            self.pause_button.setText("pause")
            self.music_label.setText(f"Playing: {self.playlist[self.current_index].split('/')[-1]}")
            self.music_paused = False

    def play_next(self):
        if self.current_index != len(self.playlist) - 1:
            self.current_index += 1
            self.load_song()
            self.play_song()
        self.update_button_state()

    def update_button_state(self):
        self.prev_button.setDisabled(self.current_index == 0)
        self.next_button.setDisabled(self.current_index == len(self.playlist) - 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = music_Player()
    player.load_song()
    player.show()
    sys.exit(app.exec_())