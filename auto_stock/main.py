import sys
from PyQt5.QtWidgets import *
from Stock_lib.kiwoom_api import *

# 키움 Open Api가 32비트 환경지원
is_64bits = sys.maxsize > 2**32
if is_64bits:
    print('64bit 환경입니다.')
else:
    print('32bit 환경입니다.')

class Main():
	def __init__(self):
		print('main init start')

		self.app = QApplication(sys.argv)
		self.kiwoom = Kiwoom_api()
		# 이벤트 루프 실행 - self.app.exec_()
		self.app.exec_()


if __name__ == '__main__':
		Main()
