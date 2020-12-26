ver = "#version 1.3.13"
print(f"collector_api Version: {ver}")

from collections import OrderedDict
from sqlalchemy import Integer, Text
import os
from PyQt5.QtWidgets import *
from Stock_lib.kiwoom_api import *

class collector_api():
    def __init__(self):
        print('collector_api - __init__')

    def variable_setting(self):
        print('collector_api.variable_setting')