from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import requests
import os
import ctypes
from io import BytesIO
from PIL import Image

app = QApplication([])
win = QWidget()

win.setWindowTitle("ТЦК")
win.resize(600, 500)

text_1 = QLabel("Вам є 18 років?")
yes_button = QPushButton("Так")
no_button = QPushButton("Ні")

main_line = QVBoxLayout()
main_line.addWidget(text_1, alignment=Qt.AlignmentFlag.AlignCenter)
main_line.addWidget(yes_button, alignment=Qt.AlignmentFlag.AlignCenter)
main_line.addWidget(no_button, alignment=Qt.AlignmentFlag.AlignCenter)

def download_image():
    url = "https://varta1.com.ua/uploads/media/images/image/8e/1b/8e1bbcb1d0354801a2e9ec7b16633f47lvkwnjzy4nzrhwa_image.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image_path = os.path.join(os.path.expanduser("~"), "downloaded_wallpaper.jpg")
        image.save(image_path)
        return image_path
    return None

def set_wallpaper(image_path):
    if os.name == 'nt':  # Windows
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    elif os.uname().sysname == 'Darwin':  # macOS
        script = f'''
            /usr/bin/osascript<<END
            tell application "Finder"
            set desktop picture to POSIX file "{image_path}"
            end tell
            END
        '''
        os.system(script)
    elif os.uname().sysname == 'Linux':  # Linux (Gnome)
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")

def replace_no_button():
    main_line.removeWidget(no_button)
    new_yes_button = QPushButton("Так")
    main_line.addWidget(new_yes_button, alignment=Qt.AlignmentFlag.AlignCenter)
    new_yes_button.clicked.connect(lambda: set_wallpaper(download_image()))

no_button.clicked.connect(replace_no_button)
yes_button.clicked.connect(lambda: set_wallpaper(download_image()))

win.setLayout(main_line)
win.show()
app.exec()