def sendAuthCodeEmail(email: str, authCode: str) -> None:
    """
    이메일 인증코드 발송 유틸
    - 지금은 print로 대체
    - 나중에 실제 이메일 / 카카오 알림톡 연동 시 이 함수 내부만 수정하면 됨.
    """
    # TODO: 실제 이메일 또는 알림톡 발송 코드로 교체
    print(f"[SEND AUTH EMAIL] to={email}, authCode={authCode}")
