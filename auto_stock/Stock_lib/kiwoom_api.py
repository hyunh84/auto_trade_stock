from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom_api(QAxWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom_api init start')

        ######  event loop를 실행하기 위한 변수 모음 ######
        self.login_event_loop = QEventLoop() # 로그인 요청용 이벤트 루프 PyQt5.QtCore에서 제공

        ###### 계좌정보 변수 설정 ######
        self.account_no = None # 계좌번호
        self.sever_gubun = None # 실서버/모의투자서버 구문
        self.account_pw = None # 계좌 패스워드
        self.deposit = 0 # 예수금
        self.use_money = 0 # 실제 투자에 사용할 금액
        self.use_money_percent = 0.5 # 예수금에서 실제 사용할 비율
        self.output_deposit = 0 # 출력가능 금액

        ###### 요청스크린 번호 ######
        self.screen_my_info = '2000'

        ###### 초기셋팅 함수 바로 실행 ######
        self.get_ocx_instance() # OCX 방식을 파이썬에 사용할 수 있게 변환해 주는 변수
        self.event_slots() # 키움과 연결하기 위한 시그널 / 슬롯 모음
        self.signal_login_commConnect() # 로그인 요청 함수 포함
        self.get_account_info() # 계좌정보
        self.get_deposit_detail_info() # 예수금상세현황 정보 요청

    #################### END :__init__ #########################

    def get_ocx_instance(self):
        # 레지스트리에 저장된 API 모듈 불러오기
        # 키움 API를 설치하면 레지스트리에 KHOPENAPI.KHOpenAPICtrl.1로 API모듈이 등록된다
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')
    
    def event_slots(self):
        # 로그인 관련 이벤트
        self.OnEventConnect.connect(self.login_slots)

    def signal_login_commConnect(self):
        # 로그인 요청 시그널
        # dynamicCall - PyQt5에서 제공하는 함수로 서버에 데이터를 송수신 할때 사용
        self.dynamicCall('CommConnect()')
        # 로그인 이벤트 루프 실행
        self.login_event_loop.exec_()

    def login_slots(self, err_code):
        print(f'login_slots err_code = ${errors(err_code)}')
        #로그인이 완료되면 이벤트 루프를 종료한다.
        self.login_event_loop.exit()

    def get_account_info(self):
        ########################################################################################################
        # 계좌정보 요청반환
        # "ACCOUNT_CNT" : 보유계좌 수를 반환합니다.
        # "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
        # "USER_ID" : 사용자 ID를 반환합니다.
        # "USER_NAME" : 사용자 이름을 반환합니다.
        # "KEY_BSECGB" : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
        # "FIREW_SECGB" : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
        # "GetServerGubun" : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실서버)
        ########################################################################################################
        account_no = self.dynamicCall('GetLoginInfo(QString)', 'ACCNO').split(';')[0]
        sever_gubun = self.dynamicCall('GetLoginInfo(QString)', 'GetServerGubun')

        if sever_gubun == '1':
            account_pw = 's8484'
        else:
            account_pw = '0000'

        print(f'계좌번호 : ${account_no.split(";")}')
        print(f'sever_gubun ${sever_gubun}')
        print(f'account_pw ${account_pw}')

        self.account_no = account_no
        self.sever_gubun = sever_gubun
        self.account_pw = account_pw

    def get_deposit_detail_info(self, sPrevNext = 0):
        # 예수금상세현황 정보
        self.dynamicCall('SetInputValue(QString, QString)', "계좌번호", self.account_no)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호", self.account_pw)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호입력매체구분", '00')
        self.dynamicCall('SetInputValue(QString, QString)', "조회구분", '1')
        self.dynamicCall('CommRqData(QString, Qstring, int, QString)', '예수금상세현황요청', 'opw00001', sPrevNext, self.screen_my_info)
        












        
