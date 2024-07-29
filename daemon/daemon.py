import time
from db.service.camper_db import CamperDB
from client.availability import Availability
from custom_types.custom_types import CampsiteEntry, CampsiteDate
from notification.camper_notification_providers import CamperWhatsappProvider, CamperGmailProvider

DEFAULT_INTERVAL_MIN = 3

class CampsiteCamperDaemon:
    def __init__(self, interval_min: int = DEFAULT_INTERVAL_MIN):
        self.db: CamperDB = CamperDB()
        self.interval_min = interval_min
        self.daemon_running = False

        self.gmail_notification_provider = CamperGmailProvider()
        self.whatsapp_notification_provider = CamperWhatsappProvider()

    def start(self):
        self.daemon_running = True

        counter = 0
        while self.daemon_running:
            for entry in self.db.campsite_entries:
                available: Availability = Availability(
                    entry.campsite_id,
                    entry.start_date.month,
                    entry.start_date.year
                )
                available_sites: list[CampsiteEntry] =  available.filter_sites_from_entry(entry)
                if len(available_sites.keys()) > 0:
                    gmail_recipients = self.db.get_email_notification_recipients()
                    whatsapp_recipients = self.db.get_whatsapp_notification_recipients()

                    print("--------------------------------")
                    print(entry)

                    if self.gmail_notification_provider.send_notification(gmail_recipients, entry):
                        print("Successfully sent Gmail notification")
                    else:
                        print("Failed to send Gmail notification")
                    if self.whatsapp_notification_provider.send_notification(whatsapp_recipients, entry):
                        print("Successfully sent Whatsapp notification")
                    else:
                        print("Failed to send Whatsapp notification")
                else:
                    print(f"Campsite {entry.campsite_id} is not available")
            
            # Send a test ping every 6 hours
            if counter % 72 == 0:
                gmail_recipients = self.db.get_email_notification_recipients()
                whatsapp_recipients = self.db.get_whatsapp_notification_recipients()
                test_entry = CampsiteEntry(
                    "NOTIFICATION_TEST",
                    CampsiteDate(12, 31, 1970),
                    CampsiteDate(12, 31, 1970),
                    0,
                    "https://recreation.gov")
                if self.gmail_notification_provider.send_notification(['alex.labbane@gmail.com'], test_entry):
                    pass
                else:
                    print("Failed to send Gmail TEST notification")
                if self.whatsapp_notification_provider.send_notification(['19182895986'], test_entry):
                    pass
                else:
                    print("Failed to send Whatsapp TEST notification")

            print("################################")
            
            counter += 1
            time.sleep(60 * self.interval_min)


