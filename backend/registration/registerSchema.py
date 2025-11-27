from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr


class RegisterBasicRequest(BaseModel):
    """
    REG-01 (회원가입 기본 정보)
    - userId, userPassword, userPasswordCheck, userName, userEmail
    """

    userId: str
    userPassword: str
    userPasswordCheck: str
    userName: str
    userEmail: EmailStr


class RegisterEmailCheckRequest(BaseModel):
    """
    REG-02-01 이메일 형식 및 중복 검증 요청
    """

    userEmail: EmailStr


class SendEmailAuthCodeRequest(BaseModel):
    """
    REG-03-01 인증코드 발송 요청
    """

    userEmail: EmailStr


class VerifyEmailAuthCodeRequest(BaseModel):
    """
    REG-03-02 인증코드 검증 요청
    """

    userEmail: EmailStr
    inputEmailAuthCode: str


class RegisterPreferenceRequest(BaseModel):
    """
    REG-04 선호 장르 / 보유 OTT 설정
    리스트가 아니라 단일 값이면 List[str] 대신 str로 바꿔도 됨.
    """

    userPreferredGenre: List[str]
    userOwnedOtt: List[str]


class RegisterCompleteRequest(BaseModel):
    """
    REG-05 가입 완료 요청
    - 최종 회원 생성에 필요한 모든 정보
    - 지금 구조에서는 프론트가 한 번에 다시 보내는 방식
    """

    userId: str
    userPassword: str
    userName: str
    userEmail: EmailStr
    userPreferredGenre: List[str]
    userOwnedOtt: List[str]


class RegisterResponse(BaseModel):
    """
    공통 응답 스키마
    """

    success: bool
    message: str
    data: Optional[Any] = None
