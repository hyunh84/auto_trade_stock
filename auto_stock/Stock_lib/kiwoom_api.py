import sys
import datetime
import warnings
#PyQt5 - 파이썬 라이브러리
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
# pandas - 데이터 분석
from pandas import DataFrame
import pandas as pd
# re - 파이선 정규표현식
import re
from Stock_lib.logging_pack import *
# 키움 Open Api가 32비트 환경지원
is_64bits = sys.maxsize > 2**32
if is_64bits:
    print('64bit 환경입니다.')
else:
    print('32bit 환경입니다.')

# 데이터 요청시 더 이상 읽어올 데이터가 없을때 다음 실행영역으로 이동시킴
class RateLimitExceeded(BaseException):
    pass

warnings.simplefilter(action='ignore', category=UserWarning)

class Kiwoom_api(QtWidgets):
    def __init__(self):
        super().__init__()
        print('open_api - __init__')

        # Kiwoom_api 호출 횟수를 저장하는 변수
        self.rq_count = 0
        self.date_setting()
        self.tr_loop_count = 0
        self.call_time = datetime.datetime.now()

        # Kiwoom_api 연동
        self._create_open_api_instance()
        self._set_signal_slots()
        self.comm_connect()

        # 계좌 정보 가져오는 함수
        self.account_info()
        self.variable_setting()

    def date_setting(self):
        print('open_api.date_setting')