import sys

from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QTimeEdit, QHBoxLayout, QCheckBox, QLineEdit)

import Conf
import Reporter


class ReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        layout = QVBoxLayout()
        entry_layout = QVBoxLayout()
        exit_layout = QVBoxLayout()
        hours_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        self.widget.setLayout(layout)
        self.setWindowTitle('Hours Reporter')

        self.text = QLabel(parent=self, text='Do you want to report working hours now?\n')
        self.button_yes = QPushButton(parent=self, text="Yes")
        self.button_yes.clicked.connect(self.button_clicked_report)
        self.button_no = QPushButton(parent=self, text="No")
        self.button_no.clicked.connect(sys.exit)
        self.entry_time = QTimeEdit(self)
        self.exit_time = QTimeEdit(self)
        self.work_location = QCheckBox('WFH', self)
        self.set_def = QCheckBox('Set as default', self)
        self.use_cred = QCheckBox('Use saved credentials', self)
        self.use_cred.setChecked(True)

        default_entry, default_exit = Conf.get_def_hours()
        self.entry_time.setTime(QTime(*default_entry))
        self.exit_time.setTime(QTime(*default_exit))
        self.work_location_text = "נוכחות מהמשרד"

        entry_layout.addWidget(QLabel(parent=self, text='Entry:'))
        entry_layout.addWidget(self.entry_time)
        exit_layout.addWidget(QLabel(parent=self, text='Exit:'))
        exit_layout.addWidget(self.exit_time)
        hours_layout.addLayout(entry_layout)
        hours_layout.addLayout(exit_layout)
        buttons_layout.addWidget(self.button_yes)
        buttons_layout.addWidget(self.button_no)
        layout.addWidget(self.text)
        layout.addLayout(hours_layout)
        layout.addWidget(self.work_location)
        layout.addWidget(self.set_def)
        layout.addWidget(self.use_cred)
        layout.addLayout(buttons_layout)

    def button_clicked_report(self):
        if self.work_location.isChecked():
            self.work_location_text = "עבודה מהבית"
        if self.set_def.isChecked():
            Conf.save_def_hours(self.entry_time.text(), self.exit_time.text())
        try:
            cred = Conf.get_cred()
        except:
            cred = None
        if not cred or not self.use_cred.isChecked():
            cred_app = CredApp(self)
            cred_app.show()

        else:
            Reporter.report(cred[0], cred[1], self.entry_time.text(), self.exit_time.text(), self.work_location_text)
            sys.exit()


class CredApp(QMainWindow):
    def __init__(self, parent=None):
        self.prnt = parent
        super(CredApp, self).__init__(parent)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        self.widget.setLayout(layout)
        self.setWindowTitle('Credentials')

        self.text = QLabel(parent=self, text='Please enter your credentials for Hilan.net.\n'
                                             'If your password is saved by Chrom, only username is needed')
        self.button_yes = QPushButton(parent=self, text="Continue")
        self.button_yes.clicked.connect(self.button_clicked_report)
        self.button_no = QPushButton(parent=self, text="Cancel")
        self.button_no.clicked.connect(sys.exit)
        self.username = QLineEdit(self)
        self.username.returnPressed.connect(self.button_clicked_report)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.button_clicked_report)
        self.save = QCheckBox('Save data locally', self)

        layout.addWidget(self.text)
        layout.addWidget(QLabel(parent=self, text='Username:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel(parent=self, text='Password:'))
        layout.addWidget(self.password)
        buttons_layout.addWidget(self.button_yes)
        buttons_layout.addWidget(self.button_no)
        layout.addWidget(self.save)
        layout.addLayout(buttons_layout)

    def button_clicked_report(self):
        username = self.username.text()
        password = self.password.text()
        if self.save.isChecked():
            Conf.save_cred(username, password)

        Reporter.report(username, password, self.prnt.entry_time.text(), self.prnt.exit_time.text(), self.prnt.work_location_text)
        sys.exit()

    def closeEvent(self, event):
        event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ReportApp()
    gui.show()
    sys.exit(app.exec_())
