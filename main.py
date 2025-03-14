from PyQt5 import QtWidgets, QtMultimedia, QtMultimediaWidgets, QtCore, QtGui
import subprocess as sp
from win32gui import FindWindow,FindWindowEx,EnumWindows,ShowWindow,SendMessage,SetParent
import sys

# process = None
# path = ""

class ConfigurationPanel(QtWidgets.QWidget):
    def __init__(self, path="", process=None):
        super().__init__()
        self.process = process
        self.path = path
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("芙芙的小蛋糕")
        self.setWindowIcon(QtGui.QIcon("./icon.png"))
        self.setGeometry(0, 0, 400, 300)
        self.center()
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        
        self.file_path_edit = QtWidgets.QLineEdit(self)
        self.choose_file_btn = QtWidgets.QPushButton("选择文件",self)
        self.choose_file_btn.clicked.connect(self.choose_file)
        self.file_path_area = QtWidgets.QHBoxLayout()
        self.file_path_area.addWidget(self.file_path_edit)
        self.file_path_area.addWidget(self.choose_file_btn)
        self._layout.addLayout(self.file_path_area)
        self.choose_file_btn.show()
        
        self.preview_video = QtMultimediaWidgets.QVideoWidget()
        self._layout.addWidget(self.preview_video)
        self.preview_video.show()
        self.media_player = QtMultimedia.QMediaPlayer()
        self.media_player.setVideoOutput(self.preview_video)

        self.stop_btn = QtWidgets.QPushButton("停止", self)
        self.apply_btn = QtWidgets.QPushButton("应用", self)
        self.stop_btn.clicked.connect(self.stop)
        self.apply_btn.clicked.connect(self.apply)
        self.action_area = QtWidgets.QHBoxLayout()
        self.action_area.addWidget(self.stop_btn)
        self.action_area.addWidget(self.apply_btn)
        self._layout.addLayout(self.action_area)
        self.apply_btn.show()
    
    def center(self):
        scr = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((scr.width() - self.width()) // 2, (scr.height() - self.height()) // 3)

    def apply(self):
        if self.process is not None:
            self.process.kill()
        self.process = sp.Popen(f"pythonw wallpaper.py {self.path}")

    def stop(self):
        if self.process is not None:
            self.process.kill()
            self.process = None

    def choose_file(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "")[0]
        if self.path != "":
            self.file_path_edit.setText(self.path)
            self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path)))
            self.media_player.play()
    
    def set_path(self, path):
        self.path = path
        self.file_path_edit.setText(self.path)
        self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path)))
        self.media_player.play()

    def closeEvent(self, a0):
        self.hide()
        # a0.ignore()
        # return super().closeEvent(a0)
    # def showEvent(self, a0):
    #     self.media_player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path)))
    #     self.media_player.play()
    #     return super().showEvent(a0)

    def quit(self):
        if self.process is not None:
            self.process.kill()

class Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None, app=None, window=None):
        super(Tray, self).__init__(parent)
        self.window = window
        self.app = app
        self.init_ui()
    def init_ui(self):
        self.setIcon(QtGui.QIcon("./icon.png"))
        self.setToolTip("Free Wallpaper")

        show = QtWidgets.QAction("打开主窗口", self, triggered=self.window.show)
        quit = QtWidgets.QAction("退出", self, triggered=self.quit)

        menu = QtWidgets.QMenu()
        menu.addAction(show)
        menu.addAction(quit)
        self.setContextMenu(menu)
        # self.show()
        
    def quit(self):
        self.window.quit()
        self.app.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    window = ConfigurationPanel()
    window.show()
    tray = Tray(app=app, window=window)
    tray.show()
    if len(sys.argv) > 1:
        window.set_path(sys.argv[1])
        window.apply()
        window.hide()
    sys.exit(app.exec_())