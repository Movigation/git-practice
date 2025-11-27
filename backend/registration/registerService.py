import random
import re
import string
from datetime import datetime

from emailSender import sendAuthCodeEmail

# DB 담당에게 넘기는 함수(더미)


def saveUserToDatabase(userData):
    # 실제 DB 저장은 DB 담당 영역.
    # 지금은 더미 구현.
    print("DB Save Request:", userData)
    return True


def isEmailDuplicate(email):
    # 이메일 중복 여부 조회 (더미).
    # 실제 구현은 DB 담당자가 작성.
    return False


def isUserIdDuplicate(userId):
    # 아이디 중복 여부 조회 (더미).
    # 실제 구현은 DB 담당자가 작성.
    return False


# 공용 검증 로직 (validator 통합)


def validateUserId(userId: str) -> None:
    if len(userId) < 4:
        raise ValueError("아이디는 최소 4자리여야 합니다.")
    if not re.match(r"^[a-zA-Z0-9_]+$", userId):
        raise ValueError("아이디는 영문, 숫자, 밑줄만 사용할 수 있습니다.")


def validatePassword(password: str) -> None:
    if len(password) < 6:
        raise ValueError("비밀번호는 최소 6자리여야 합니다.")
    if not re.search(r"[0-9]", password):
        raise ValueError("비밀번호에 숫자가 포함되어야 합니다.")
    if not re.search(r"[A-Za-z]", password):
        raise ValueError("비밀번호에 영문이 포함되어야 합니다.")


def validateEmail(email: str) -> None:
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValueError("이메일 형식이 올바르지 않습니다.")


# 이메일 인증코드 저장소(메모리)
# 실제로는 Redis 같은 캐시 사용

emailAuthMemory: dict[str, str] = {}


# REG-01: 기본 정보 입력


def registerBasic(payload):
    userId = payload.userId
    userPassword = payload.userPassword
    userPasswordCheck = payload.userPasswordCheck
    userName = payload.userName
    userEmail = payload.userEmail

    # 기본 검증
    validateUserId(userId)
    validatePassword(userPassword)
    validateEmail(userEmail)

    # 비밀번호 확인
    if userPassword != userPasswordCheck:
        raise ValueError("비밀번호가 일치하지 않습니다.")

    # 중복 체크
    if isUserIdDuplicate(userId):
        raise ValueError("이미 존재하는 아이디입니다.")
    if isEmailDuplicate(userEmail):
        raise ValueError("이미 존재하는 이메일입니다.")

    return {
        "success": True,
        "message": "기본 정보 검증 완료",
        "data": {
            "userId": userId,
            "userName": userName,
            "userEmail": userEmail,
        },
    }


# REG-02: 이메일 중복 및 형식 검증


def checkEmailDuplicate(payload):
    email = payload.userEmail

    validateEmail(email)

    if isEmailDuplicate(email):
        raise ValueError("이미 사용 중인 이메일입니다.")

    return {
        "success": True,
        "message": "사용 가능한 이메일입니다.",
    }


# REG-03-01: 인증코드 발급 + 발송


def sendEmailAuthCode(payload):
    email = payload.userEmail

    validateEmail(email)

    # 6자리 숫자 인증코드 생성
    authCode = "".join(random.choices(string.digits, k=6))

    # 메모리에 저장
    emailAuthMemory[email] = authCode

    # ✅ 발송 로직은 emailSender로 위임
    sendAuthCodeEmail(email, authCode)

    return {
        "success": True,
        "message": "인증코드가 이메일로 발송되었습니다.",
    }


# REG-03-02: 인증코드 검증


def verifyEmailAuthCode(payload):
    email = payload.userEmail
    inputCode = payload.inputEmailAuthCode

    if email not in emailAuthMemory:
        raise ValueError("인증코드가 발급되지 않았습니다.")

    if emailAuthMemory[email] != inputCode:
        raise ValueError("인증코드가 일치하지 않습니다.")

    return {
        "success": True,
        "message": "이메일 인증이 완료되었습니다.",
    }


# REG-04: 선호 장르 / OTT 설정


def savePreferences(payload):
    return {
        "success": True,
        "message": "선호 장르 및 OTT 정보가 저장되었습니다.",
        "data": {
            "preferredGenre": payload.userPreferredGenre,
            "ownedOtt": payload.userOwnedOtt,
        },
    }


# REG-05: 가입 완료


def completeRegistration(payload):
    userData = {
        "userId": payload.userId,
        # TODO: 비밀번호 해싱 적용 필요 (예: bcrypt)
        "userPassword": payload.userPassword,
        "userName": payload.userName,
        "userEmail": payload.userEmail,
        "preferredGenre": payload.userPreferredGenre,
        "ownedOtt": payload.userOwnedOtt,
        "createdAt": datetime.now().isoformat(),
    }

    # DB 저장 요청
    saveUserToDatabase(userData)

    return {
        "success": True,
        "message": "회원가입이 완료되었습니다.",
        "data": userData,
    }
