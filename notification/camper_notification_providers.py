from dataclasses import dataclass
import json
import smtplib
from email.message import EmailMessage
import requests
from custom_types.custom_types import CampsiteDate, CampsiteEntry

class CamperGmailProvider:
    def __init__(self, config_file = "./notification/gmail_config.json"):
        with open(config_file) as f:
            config = json.load(f)
            self.username = config["USERNAME"]
            self.password = config["APP_PASSWORD"]

    
    def send_notification(self, campsite_entry: CampsiteEntry, retry: int = 3) -> bool:
        if retry == 0:
            return False

        recipients = campsite_entry.notification_group.email
        msg = EmailMessage()
        msg_body = str(campsite_entry) + "\nReserve now at %s" % (campsite_entry.reserve_url)
        msg.set_content(msg_body)

        msg['Subject'] = f"🏕️  Campsite {campsite_entry.campsite_id} is Available!"
        msg['From'] = self.username
        msg['To'] = ", ".join(recipients)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self.username, self.password)
            server.sendmail(self.username, recipients, msg.as_string())
            server.close()
        except BaseException:
            return self.send_notification(campsite_entry, retry - 1)
        
        return True

class CamperWhatsappProvider:
    def __init__(self, config_file = "./notification/whatsapp_config.json"):
        with open(config_file) as f:
            config = json.load(f)
            self.access_token = config["ACCESS_TOKEN"]
            self.version = config["VERSION"]
            self.phone_number_id = config["PHONE_NUMBER_ID"]

    def send_notification(self, campsite_entry: CampsiteEntry) -> bool:
        return_code = True
        for recipient in campsite_entry.notification_group.whatsapp:
            try:
                message_sent = self._send_message(recipient, campsite_entry)
                if message_sent is False:
                    raise Exception()
            except BaseException:
                return_code = False
                print("Failed to send Whatsapp notification to %s" % (recipient))
        
        return return_code

    def _send_message(self, recipient: str, campsite_entry: CampsiteEntry, retry: int = 3):
        if retry == 0:
            return

        msg_data: dict = self._get_text_message_input(recipient, campsite_entry)
        headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {self.access_token}",
        }
        url = 'https://graph.facebook.com' + f"/{self.version}/{self.phone_number_id}/messages"

        res = requests.post(url, headers=headers, data=msg_data)
        if res.status_code != 200:
            print("Error sending whatsapp message to %s. %d retries left" % (res.text, retry))
            self._send_message(recipient, campsite_entry, retry - 1)


    def _get_text_message_input(self, recipient: str, campsite_entry: CampsiteEntry):
        campsite_id = campsite_entry.campsite_id
        start_date = campsite_entry.start_date.get_as_date()
        end_date = campsite_entry.end_date.get_as_date()
        reserve_url = campsite_entry.reserve_url

        return json.dumps({
            "messaging_product": "whatsapp",
            "preview_url": False,
            "recipient_type": "individual",
            "to": recipient,
            "type": "template",
            "template": { 
                "name": "campsite_available", 
                "language": { "code": "en"},
                "components": [
                    {
                        "type": "HEADER",
                        "parameters": [{
                            "type": "text",
                            "text": campsite_id
                        }]
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {
                                "type": "text",
                                "text": campsite_id
                            },
                            {
                                "type": "text",
                                "text": str(start_date)
                            },
                            {
                                "type": "text",
                                "text":str(end_date)
                            },
                            {
                                "type": "text",
                                "text": reserve_url
                            }
                        ]
                    }
                ],
            }
        })

if __name__ == "__main__":
    entry = CampsiteEntry.from_dict(
        {
            "campsite_id": "232447",
            "start_date": {
                "month": 4,
                "day": 11,
                "year": 2024
            },
            "end_date": {
                "month": 4,
                "day": 13,
                "year": 2024
            },
            "num_people": 4,
            "notification_group": {
                "email": ['alex.labbane@gmail.com'],
                "whatsapp": ['19182895986']
            }
        }
    )
    gmail_provider = CamperGmailProvider()
    if gmail_provider.send_notification(entry):
        print("Success!")
    else:
        print("Failed")

    whatsapp_provider = CamperWhatsappProvider()
    if whatsapp_provider.send_notification(entry):
        print("Success!")
    else:
        print("Failed")