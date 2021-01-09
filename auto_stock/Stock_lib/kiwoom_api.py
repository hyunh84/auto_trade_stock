from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom_api(QAxWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom_api init start')

        ######  event loop를 실행하기 위한 변수 모음 ######
        self.login_event_loop = QEventLoop() # 로그인 요청용 이벤트 루프 PyQt5.QtCore에서 제공
        self.OnReceiveTrData_event_loop = QEventLoop() # OnReceiveTrData요청시 이벤트 루프

        ###### 계좌정보 변수 설정 ######
        self.account_no = None # 계좌번호
        self.sever_gubun = None # 실서버/모의투자서버 구문
        self.account_pw = None # 계좌 패스워드
        self.deposit = 0 # 예수금
        self.use_money = 0 # 실제 투자에 사용할 금액
        self.use_money_percent = 0.5 # 예수금에서 실제 사용할 비율
        self.output_deposit = 0 # 출력가능 금액
        self.total_buy_money = 0 # 총매입금액
        self.total_profit_loss_money = 0 # 총평가손익금액
        self.total_profit_loss_rate = 0.0  # 총수익률(%)
        self.account_evaluation_info = {} #계좌평가잔고 정보 객체

        ###### 요청스크린 번호 ######
        self.screen_my_info = '2000'

        ###### 초기셋팅 함수 바로 실행 ######
        self.get_ocx_instance() # OCX 방식을 파이썬에 사용할 수 있게 변환해 주는 변수
        self.event_slots() # 키움과 연결하기 위한 시그널 / 슬롯 모음
        self.signal_login_commConnect()  # 로그인 요청 함수 포함
        self.get_account_info() # 계좌정보
        self.get_deposit_detail_info() # 예수금상세현황 정보 요청
        self.get_account_blanace_detail() # 계좌평가잔고내역 요청

    #################### END :__init__ #########################

    def get_ocx_instance(self):
        # 레지스트리에 저장된 API 모듈 불러오기
        # 키움 API를 설치하면 레지스트리에 KHOPENAPI.KHOpenAPICtrl.1로 API모듈이 등록된다
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def signal_login_commConnect(self):
        # 로그인 요청 시그널
        # dynamicCall - PyQt5에서 제공하는 함수로 서버에 데이터를 송수신 할때 사용
        self.dynamicCall('CommConnect()')
        # 로그인 이벤트 루프 실행
        self.login_event_loop.exec_()

    ###### 슬롯 설정 함수 ######
    def event_slots(self):
        self.OnEventConnect.connect(self.login_slots) # 로그인 관련 이벤트
        self.OnReceiveTrData.connect(self.TR_data_slot) # 트랜젝션 요청관련 이벤트

    def login_slots(self, err_code):
        print(f'login_slots err_code = {errors(err_code)}')
        #로그인이 완료되면 이벤트 루프를 종료한다.
        self.login_event_loop.exit()

    def TR_data_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        print(f'TR_data_slot start')
        ########################################################################################################
        # BSTR sScrNo, // 화면번호
        # BSTR sRQName, // 사용자 구분명
        # BSTR sTrCode, // TR이름
        # BSTR sRecordName, // 레코드 이름
        # BSTR sPrevNext, // 연속조회 유무를 판단하는 값 0: 연속(추가조회) 데이터 없음, 2: 연속(추가조회) 데이터 있음
        ########################################################################################################
        if sRQName == '예수금상세현황요청':
            ###### 싱글데이터 ######
            deposit = int(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '예수금'))
            output_deposit = int(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '출금가능금액'))
            use_money = int(float(deposit) * self.use_money_percent) / 4
            self.deposit = deposit
            self.use_money = use_money
            self.output_deposit = output_deposit
            self.stop_screen_cancel(self.screen_my_info)
            self.OnReceiveTrData_event_loop.exit()

            print(f'예수금 {deposit}')
            print(f'실제 투자에 사용할 금액 {use_money}')
            print(f'출금가능금액 {output_deposit}')
        elif sRQName == '계좌평가잔고내역요청':
            print(f'계좌평가잔고내역요청')
            ###### 싱글데이터 ######
            total_buy_money = int(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '총매입금액'))
            total_profit_loss_money = int(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '총평가손익금액'))
            total_profit_loss_rate = float(self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, 0, '총수익률(%)'))
            self.total_buy_money = total_buy_money
            self.total_profit_loss_money = total_profit_loss_money
            self.total_profit_loss_rate = total_profit_loss_rate
            self.stop_screen_cancel(self.screen_my_info)

            print(f'총매입금액 {total_buy_money}')
            print(f'총평가손익금액 {total_profit_loss_money}')
            print(f'총수익률 {total_profit_loss_rate}')

            ###### 멀티데이터 ######
            multiData = self.dynamicCall('GetRepeatCnt(QString, QString)', sTrCode, sRQName)
            if multiData > 0:
                print(f'멀티데이터 계좌평가잔고내역 데이터 = {multiData}')
                for i in range(multiData):
                    stock_no = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '종목번호')
                    stock_no = stock_no.strip()[1:]
                    print(f'stock_no.strip()[1:] = {stock_no.strip()[1:]}')
                    stock_nm = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '종목명')
                    stock_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '보유수량')
                    stock_buy_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '매입가')
                    stock_rate_return = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '수익률(%)')
                    stock_current_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '현재가')
                    stock_purchase_total_price = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '매입금액')
                    stock_possible_sell_quantity = self.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRQName, i, '매매가능수량')
                    if not stock_no in self.account_evaluation_info:
                        print(f' not stock_no in self.account_evaluation_info = {not stock_no in self.account_evaluation_info}')
                        self.account_evaluation_info[stock_no] = {}

                    self.account_evaluation_info[stock_no].update({'종목명' : stock_nm.strip()})
                    self.account_evaluation_info[stock_no].update({'보유수량' : int(stock_quantity.strip())})
                    self.account_evaluation_info[stock_no].update({'매입가' : int(stock_buy_price.strip())})
                    self.account_evaluation_info[stock_no].update({'수익률(%)' : float(stock_rate_return.strip())})
                    self.account_evaluation_info[stock_no].update({'현재가' : int(stock_current_price.strip())})
                    self.account_evaluation_info[stock_no].update({'매입금액' : int(stock_purchase_total_price.strip())})
                    self.account_evaluation_info[stock_no].update({'매매가능수량' : int(stock_possible_sell_quantity.strip())})

                    print(f'종목번호 {stock_no}')
                    print(f'종목명 {stock_nm}')
                    print(f'보유수량 {stock_quantity}')
                    print(f'매입가 {stock_buy_price}')
                    print(f'수익률(%) {stock_rate_return}')
                    print(f'현재가 {stock_current_price}')
                    print(f'매입금액 {stock_purchase_total_price}')
                    print(f'매매가능수량 {stock_possible_sell_quantity}')
            else:
                print('멀티데이터 계좌평가잔고내역 데이터 없음')

            if sPrevNext == '2':
                self.get_account_blanace_detail(sPrevNext='2')
            else:
                self.OnReceiveTrData_event_loop.exit()

    def stop_screen_cancel(self, sScrNo=None):
        print(f'stop_screen_cancel (sScrNo : {sScrNo})')
        self.dynamicCall('DisconnectRealData(QString)', sScrNo)

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

        print(f'계좌번호 : {account_no}')
        print(f'접속서버 구분 (1 : 모의투자, 나머지 : 실서버) {sever_gubun}')
        print(f'계좌 비밀번호 {account_pw}')

        self.account_no = account_no
        self.sever_gubun = sever_gubun
        self.account_pw = account_pw

    def get_deposit_detail_info(self, sPrevNext = 0):
        # 예수금상세현황 정보
        self.dynamicCall('SetInputValue(QString, QString)', "계좌번호", self.account_no)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호", self.account_pw)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호입력매체구분", '00')
        self.dynamicCall('SetInputValue(QString, QString)', "조회구분", '1')
        self.dynamicCall('CommRqData(QString, QString, int, QString)', '예수금상세현황요청', 'opw00001', sPrevNext, self.screen_my_info)
        # self.OnReceiveTrData_event_loop = QEventLoop()
        self.OnReceiveTrData_event_loop.exec_()

    def get_account_blanace_detail(self, sPrevNext = 0):
        #계좌평가잔고요청 정보
        self.dynamicCall('SetInputValue(QString, QString)', "계좌번호", self.account_no)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호", self.account_pw)
        self.dynamicCall('SetInputValue(QString, QString)', "비밀번호입력매체구분", '00')
        self.dynamicCall('SetInputValue(QString, QString)', "조회구분", '1')
        self.dynamicCall('CommRqData(QString, QString, int, QString)', '계좌평가잔고내역요청', 'opw00018', sPrevNext, self.screen_my_info)
        # self.OnReceiveTrData_event_loop = QEventLoop()
        self.OnReceiveTrData_event_loop.exec_()












        
