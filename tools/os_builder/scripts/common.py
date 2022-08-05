import colorama
from colorama import Fore, Back, Style

import pip


def print_info(text):
    print(Fore.BLUE, "\bInfo:", text, Style.RESET_ALL)


def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        print("Trying to install " + package + " ...")
        pip.main(['install', package])

