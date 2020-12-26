print('collector 프로그램 시작!!!!!!!')

from Stock_lib.collector_api import *

class Auto_stock:

    def __init__(self):
        self.collector_api = collector_api()

    def auto_stock(self):
        self.collector_api.variable_setting()
        # self.collector_api.code_update_check()

if __name__=="__main__":
    print('collector __main__ 진입')
    app = QApplication(sys.argv)
    c = Auto_stock()
    c.auto_stock()