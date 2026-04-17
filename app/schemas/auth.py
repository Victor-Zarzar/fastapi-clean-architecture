from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    mfa_pending_token: str | None = None


class TokenData(BaseModel):
    sub: str | None = None
    role: str | None = None


class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class MFAVerifyRequest(BaseModel):
    mfa_pending_token: str
    totp_code: str


class MFAPendingResponse(BaseModel):
    mfa_pending_token: str
    token_type: str = "mfa_pending"
