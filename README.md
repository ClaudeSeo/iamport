# iamport
아임포트 (http://www.iamport.kr/) REST API 연동 모듈 

- 이용중 발생한 문제에 대하여 책임을 지지 않습니다


[![Build Status](https://travis-ci.org/ClaudeSeo/iamport.svg?branch=master)](https://travis-ci.org/ClaudeSeo/iamport)


# 기능
1. 결제 스케줄 예약
2. 결제 스케줄 취소
3. 재결제
4. 비 인증 결제
5. 결제 취소
6. 부분 결제 취소
7. 결제 정보 확인

# 설치
```
$ git clone https://github.com/SeoDongMyeong/iamport.git
$ cd iamport
$ python setup.py install
```

# 사용 방법
```
iamport = Iamport(imp_key, imp_secret)

# 비 인증 결제
try :
	iamport.onetime(merchant_uid, '0000-0000-0000-0000','2022-01', '970101', '00', 1004)
except iamport.IamportError as e:
    print e.message

# 결제정보 가져오기
try:
	iamport.find(merchant_uid)
except iamport.IamportError as e:
    print e.message
```

# TODO
1. vbanks API 추가
2. 구매자 빌키 관리 API 추가
3. 파이썬3 테스트
