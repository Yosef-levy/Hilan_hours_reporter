import ctypes
import os
import time
from pathlib import Path

import Encryption

home_directory = os.path.expanduser('~')
hidden_directory = os.path.join(home_directory, 'Documents', 'hours_reporter')
if not os.path.isdir(hidden_directory):
    os.mkdir(hidden_directory)
    ctypes.windll.kernel32.SetFileAttributesW(hidden_directory, 0x02)
certificate_file = os.path.join(hidden_directory, 'daily_report')
default_hours_file = os.path.join(hidden_directory, 'default_hours')
credentials_file = os.path.join(hidden_directory, 'tmp')


def update_today_reported():
    Path(certificate_file).touch()


def is_today_reported():
    if os.path.isfile(certificate_file):
        if time.localtime(os.path.getmtime(certificate_file)).tm_yday == time.localtime(time.time()).tm_yday:
            return True


def get_cred():
    if not os.path.isfile(credentials_file):
        return None
    with open(credentials_file, 'r') as fl:
        return Encryption.decrypt(fl.read())


def save_cred(username, password):
    with open(credentials_file, 'w+') as fl:
        fl.write(Encryption.encrypt(username, password))


def get_def_hours():
    if not os.path.isfile(default_hours_file):
        return (9, 0), (18, 0)
    with open(default_hours_file, 'r') as fl:
        return (int(fl.readline()), int(fl.readline())), (int(fl.readline()), int(fl.readline()))


def save_def_hours(start, end):
    en = start.split(':')
    ex = end.split(':')
    with open(default_hours_file, 'w+') as fl:
        fl.write(en[0] + '\n')
        fl.write(en[1] + '\n')
        fl.write(ex[0] + '\n')
        fl.write(ex[1] + '\n')


