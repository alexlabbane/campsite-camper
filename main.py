from db.service.camper_db import CamperDB
from client.availability import Availability
from custom_types.custom_types import CampsiteEntry
from notification.camper_notification_providers import CamperWhatsappProvider, CamperGmailProvider
from daemon.daemon import CampsiteCamperDaemon

# Test
if __name__ == "__main__":
    daemon: CampsiteCamperDaemon = CampsiteCamperDaemon()
    daemon.start()