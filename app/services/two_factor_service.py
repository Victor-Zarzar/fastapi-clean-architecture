import base64
import io
import secrets

import qrcode
from pyotp import TOTP

from app.models.user import User
from app.repository.user import UserRepository


class TwoFactorService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @staticmethod
    def generate_secret() -> str:
        return base64.b32encode(secrets.token_bytes(20)).decode()

    def enable_2fa(self, user: User) -> dict:
        secret = self.generate_secret()
        self.user_repository.set_totp_secret(user, secret)
        totp = TOTP(secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name="MyApp")
        return {"secret_key": secret, "otpauth_uri": uri}

    def get_qr_code_bytes(self, user: User) -> bytes:
        if not user.totp_secret:
            raise ValueError("2FA not enabled for this user.")
        totp = TOTP(user.totp_secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name="MyApp")
        img = qrcode.make(uri)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf.getvalue()

    def verify_code(self, user: User, totp_code: str) -> bool:
        if not user.totp_secret or not user.totp_enabled:
            return False
        return TOTP(user.totp_secret).verify(totp_code)

    def disable_2fa(self, user: User) -> None:
        self.user_repository.disable_totp(user)
