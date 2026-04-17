from pydantic import BaseModel


class Enable2FAResponse(BaseModel):
    secret_key: str
    otpauth_uri: str


class Verify2FARequest(BaseModel):
    totp_code: str


class TwoFALoginRequest(BaseModel):
    email: str
    password: str
    totp_code: str | None = None
