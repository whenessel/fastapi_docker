import base64
import os

from requests import request

from app.config import get_settings

settings = get_settings()


class EmailNotification:
    def __init__(self, app_key, secret_key):
        self.app_key = app_key
        self.secret_key = secret_key
        self.auth_header = self.generate_basic_auth(self.app_key, self.secret_key)

        self.sender = settings.email_sender

    def generate_basic_auth(self, username: str, password: str):
        return base64.b64encode(f"{username}:{password}".encode())

    def send(self, receiver: str, subject: str, template: str, vars: dict):
        if (os.getenv("TESTING") is not None) and (os.getenv("TESTING") == "1"):
            return "TEST_EMAIL_NOTIFICATION"

        if settings.ENVIRONMENT != "PRD":
            receiver = settings.email_dev

        # response = self.by_email_labs(receiver, subject, template, vars)
        response = self.send_by_mailjet(receiver, subject, template, vars)

        return response

    def send_by_email_labs(self, receiver: str, subject: str, template: str, vars: dict):
        url = "https://api.emaillabs.net.pl/api/sendmail_templates"
        smtp = settings.email_smtp

        receiver_data = {f"to[{receiver}]": ""}

        for key, value in vars.items():
            receiver_data[f"to[{receiver}][vars][{key}]"] = value

        headers = {"Authorization": f"Basic {self.auth_header.decode()}"}
        template_data = {"from": self.sender, "smtp_account": smtp, "subject": subject, "template_id": template}

        payload = receiver_data | template_data
        files = {}

        response = request("POST", url, headers=headers, data=payload, files=files)
        return response.text

    def send_by_mailjet(self, receiver: str, subject: str, template: str, vars: dict):
        url = "https://api.mailjet.com/v3.1/send"

        to_field = {"Email": f"{receiver}", "Name": "user"}
        from_field = settings.email_mailjet_sender

        payload = {
            "Messages": [
                {
                    "From": {"Email": f"{from_field}", "Name": "rm.pl"},
                    "To": [to_field],
                    "TemplateID": 4534065,
                    "TemplateLanguage": True,
                    "Subject": "Nowa awaria",
                    "Variables": {
                        "issue_name": "Awaria",
                        "issue_url": "www.onet.pl",
                        "sender_name": "Michał",
                        "product_name": "Intio",
                    },
                    "TemplateErrorReporting": {"Email": settings.email_dev, "Name": "Mailjet Template Errors"},
                }
            ]
        }

        headers = {"Content-Type": "application/json", "Authorization": f"Basic {self.auth_header.decode()}"}

        # response = request("POST", url, headers=headers, json=payload)

        # return response.text

        return "OK"

    def _add_template_debugging(message_data: dict) -> None:
        message_data["TemplateErrorReporting"] = {
            "Email": settings.DEV_EMAIL_ADDRESS,
            "Name": "Mailjet Template Errors",
        }

        # https://github.com/pass-culture/pass-culture-api/blob/b24db94a2fb2dd6473705c3bde97c9e28fac3390/api/src/pcapi/utils/mailing.py#L195
