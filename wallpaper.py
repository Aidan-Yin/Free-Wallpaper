from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets
from constant import title
import sys
from win32gui import FindWindow,FindWindowEx,EnumWindows,ShowWindow,SendMessage,SetParent

class Wallpaper(QtMultimediaWidgets.QVideoWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint)
        self.setGeometry(QtWidgets.QApplication.desktop().geometry())
        self.setWindowTitle(title)

class Player:
    def __init__(self):
        self.player = Wallpaper()
        self.media_player = QtMultimedia.QMediaPlayer()
        self.media_player.setVideoOutput(self.player)
    
    def play(self, paths):
        medialist = [QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)) for path in paths]
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.playlist.addMedia(medialist)
        self.media_player.setPlaylist(self.playlist)
        # self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.media_player.play()

def hideWorkerW2(hwnd, _):
    if FindWindowEx(hwnd, None, "SHELLDLL_DefView", None) != 0:
        WorkerW2 = FindWindowEx(None, hwnd, "WorkerW", None)
        ShowWindow(WorkerW2, 0) # hide it
    return True
def setAsWallpaper(hwnd):
    progman = FindWindow("Progman", "Program Manager")
    SendMessage(progman, 0x005C, 0, 0)
    SendMessage(progman, 0x052C, 0, 0)
    EnumWindows(hideWorkerW2, None)
    SetParent(hwnd, progman)

app = QtWidgets.QApplication([])
mp = Player()
mp.player.show()
hwnd = int(mp.player.winId())
mp.play(sys.argv[1:])
setAsWallpaper(hwnd)
sys.exit(app.exec_())