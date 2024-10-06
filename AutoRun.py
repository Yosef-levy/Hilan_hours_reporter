"""
Report working hours to Hilanet

Requirements:
Selenium
pyqt5
"""

import sys
import Conf

if Conf.is_today_reported():
    print("Today reported")
    sys.exit()

#
# import urllib.request
# try:
#     urllib.request.urlopen('http://google.com')
# except:
#     print("Connection issue")
#     sys.exit()


import sys
from PyQt5.QtWidgets import (QApplication)

import App


app = QApplication(sys.argv)
gui = App.ReportApp()
gui.show()
sys.exit(app.exec_())

