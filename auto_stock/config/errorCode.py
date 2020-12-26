def errors(errCode):
	errDict = {
		0 : ('OP_ERR_NONE', '정상처리'),
		-10 : ('OP_ERR_FAIL', '실패'),
		-100 : ('OP_ERR_LOGIN', '사용자정보교환실패'),
		-101 : ('OP_ERR_CONNECT', '서버접속실패'),
		
		- 310 : ('OP_ERR_MIS_500CNT_EXC', '주문수량500계약초과'),
		- 340 : ('OP_ERRP_ORD_WRONG_ACCTINFO', '계좌정보없음'),
		- 500 : ('OP_ERR_ORD_SYMCODE_EMPTY', '종목코드없음'),
		
	}

	result = errDict[errCode]

	return result

####################################################
# 로그인 관련 이벤트
# OnEventConnect()
#  -0 로그인 성공
# -100 사용자 정보교환 실패
# -101 서버접속 실패
# -102 버전처리 실패
####################################################