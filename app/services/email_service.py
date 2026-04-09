import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailDeliveryError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmailService:
    def send_email(self, to_email: str, subject: str, html_body: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.sendmail(
                    settings.SMTP_FROM_EMAIL,
                    to_email,
                    msg.as_string(),
                )
        except smtplib.SMTPAuthenticationError as exc:
            raise EmailDeliveryError(
                "SMTP authentication failed. Check your email credentials."
            ) from exc
        except smtplib.SMTPException as exc:
            raise EmailDeliveryError("Failed to send email.") from exc

    def send_email_verification(self, to_email: str, username: str, token: str) -> None:
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

        subject = "Verify your email"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:0;background-color:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f5;padding:40px 16px;">
            <tr>
              <td align="center">
                <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background-color:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e4e4e7;">

                  <tr>
                    <td style="background-color:#1a1a2e;padding:32px;text-align:center;">
                      <p style="color:#ffffff;font-size:18px;font-weight:500;margin:0;">Verify your email</p>
                    </td>
                  </tr>

                  <tr>
                    <td style="padding:32px 32px 24px;">
                      <p style="font-size:15px;color:#18181b;margin:0 0 8px;">Hello, <strong>{username}</strong>!</p>
                      <p style="font-size:14px;color:#71717a;margin:0 0 24px;line-height:1.6;">
                        Thanks for signing up. To activate your account, please confirm your email address by clicking the button below.
                      </p>

                      <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                          <td align="center" style="padding:8px 0 0;">
                            <a href="{verify_url}" style="display:inline-block;background-color:#1a1a2e;color:#ffffff;text-decoration:none;padding:12px 32px;border-radius:8px;font-size:14px;font-weight:500;">
                              Verify email
                            </a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>

                  <tr>
                    <td style="border-top:1px solid #e4e4e7;padding:16px 32px;">
                      <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                          <td style="font-size:12px;color:#a1a1aa;">This link expires in <strong>30 minutes</strong>.</td>
                          <td align="right" style="font-size:12px;color:#a1a1aa;">If you didn't sign up, you can safely ignore this email.</td>
                        </tr>
                      </table>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
        )

    def send_password_reset_email(
        self,
        to_email: str,
        username: str,
        token: str,
    ) -> None:
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        subject = "Reset your password"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin:0;padding:0;background-color:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f5;padding:40px 16px;">
            <tr>
              <td align="center">
                <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background-color:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e4e4e7;">

                  <tr>
                    <td style="background-color:#1a1a2e;padding:32px;text-align:center;">
                      <p style="color:#ffffff;font-size:18px;font-weight:500;margin:0;">Reset your password</p>
                    </td>
                  </tr>

                  <tr>
                    <td style="padding:32px 32px 24px;">
                      <p style="font-size:15px;color:#18181b;margin:0 0 8px;">Hello, <strong>{username}</strong>!</p>
                      <p style="font-size:14px;color:#71717a;margin:0 0 24px;line-height:1.6;">
                        We received a request to reset your password. Click the button below to create a new password.
                      </p>

                      <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                          <td align="center" style="padding:8px 0 0;">
                            <a href="{reset_link}" style="display:inline-block;background-color:#1a1a2e;color:#ffffff;text-decoration:none;padding:12px 32px;border-radius:8px;font-size:14px;font-weight:500;">
                              Reset password
                            </a>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>

                  <tr>
                    <td style="border-top:1px solid #e4e4e7;padding:16px 32px;">
                      <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                          <td style="font-size:12px;color:#a1a1aa;">This link expires in <strong>30 minutes</strong>.</td>
                          <td align="right" style="font-size:12px;color:#a1a1aa;">If you did not request this, you can safely ignore this email.</td>
                        </tr>
                      </table>
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>
        </body>
        </html>
        """

        self.send_email(
            to_email=to_email,
            subject=subject,
            html_body=html_body,
        )
