from fastapi import APIRouter, HTTPException, status

from registerSchema import (
    RegisterBasicRequest,
    RegisterCompleteRequest,
    RegisterEmailCheckRequest,
    RegisterPreferenceRequest,
    RegisterResponse,
    SendEmailAuthCodeRequest,
    VerifyEmailAuthCodeRequest,
)
from registerService import (
    checkEmailDuplicate,
    completeRegistration,
    registerBasic,
    savePreferences,
    sendEmailAuthCode,
    verifyEmailAuthCode,
)

router = APIRouter(prefix="/api/register", tags=["register"])


@router.post("/basic", response_model=RegisterResponse)
async def registerBasicEndpoint(payload: RegisterBasicRequest):
    # REG-01: 기본 정보 입력
    try:
        result = registerBasic(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/email/check", response_model=RegisterResponse)
async def emailCheckEndpoint(payload: RegisterEmailCheckRequest):
    # REG-02: 이메일 형식 및 중복 검증
    try:
        result = checkEmailDuplicate(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/email/sendCode", response_model=RegisterResponse)
async def sendEmailCodeEndpoint(payload: SendEmailAuthCodeRequest):
    # REG-03-01: 이메일 인증코드 발급 및 전송
    try:
        result = sendEmailAuthCode(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/email/verifyCode", response_model=RegisterResponse)
async def verifyEmailCodeEndpoint(payload: VerifyEmailAuthCodeRequest):
    # REG-03-02: 이메일 인증코드 검증
    try:
        result = verifyEmailAuthCode(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/preferences", response_model=RegisterResponse)
async def preferencesEndpoint(payload: RegisterPreferenceRequest):
    # REG-04: 선호 장르 / 보유 OTT 설정
    try:
        result = savePreferences(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/complete", response_model=RegisterResponse)
async def completeEndpoint(payload: RegisterCompleteRequest):
    # REG-05: 가입 완료 처리
    try:
        result = completeRegistration(payload)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
