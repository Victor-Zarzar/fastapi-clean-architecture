import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailDeliveryError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EmailService:
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

                  <!-- Header -->
                  <tr>
                    <td style="background-color:#1a1a2e;padding:32px;text-align:center;">
                      <div style="display:inline-block;background:rgba(255,255,255,0.08);border-radius:12px;padding:14px;margin-bottom:16px;">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M20 4H4C2.9 4 2 4.9 2 6V18C2 19.1 2.9 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4Z" stroke="#a1a1aa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M22 6L12 13L2 6" stroke="#a1a1aa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </div>
                      <p style="color:#ffffff;font-size:18px;font-weight:500;margin:0;">Verify your email</p>
                    </td>
                  </tr>

                  <!-- Body -->
                  <tr>
                    <td style="padding:32px 32px 24px;">
                      <p style="font-size:15px;color:#18181b;margin:0 0 8px;">Hello, <strong style="font-weight:500;">{username}</strong>!</p>
                      <p style="font-size:14px;color:#71717a;margin:0 0 24px;line-height:1.6;">Thanks for signing up. To activate your account, please confirm your email address by clicking the button below.</p>

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

                  <!-- Footer -->
                  <tr>
                    <td style="border-top:1px solid #e4e4e7;padding:16px 32px;">
                      <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                          <td style="font-size:12px;color:#a1a1aa;">This link expires in <strong style="font-weight:500;">30 minutes</strong>.</td>
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
            raise EmailDeliveryError("Failed to send verification email.") from exc
