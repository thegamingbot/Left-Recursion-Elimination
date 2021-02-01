r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""
from GUIWindow import GUIWindow
from MainWindow import MainWindow


class Controller:
    def __init__(self):
        self.login = GUIWindow()

    def show_login(self):
        self.login.switch_window.connect(self.show_main)
        self.login.show()

    def show_main(self, grammar):
        self.window = MainWindow(grammar)
        self.login.close()
        self.window.show()
