import json

from client.availability import Availability
from custom_types.custom_types import CampsiteEntry, NotificationGroup
from db.service.db_config import DBConfig

class CamperDB:
    def __init__(self, config_file: str = None):
        self.config: DBConfig = DBConfig() if config_file is None else DBConfig(config_file)
        self.campsite_entries: list[CampsiteEntry] = []
        self.notification_groups: dict = {}
        self.refresh_db()

    def __get_db_json(self):
        db_path = self.config.get_db_path()
        with open(db_path) as db_file:
            return json.load(db_file)

    def refresh_db(self):
        new_entries: list[CampsiteEntry] = []
        db_json = self.__get_db_json()

        # Parse notification groups
        if "notification_groups" in db_json:
            print("noti groups")
            try:
                for group_name, notification_group in db_json["notification_groups"].items():
                    print(group_name, notification_group)
                    self.notification_groups[group_name] = NotificationGroup.from_dict(notification_group)
            except KeyError:
                print(f"Error: DB does not follow proper schema for notification groups")
            except BaseException:
                print("Error: Unknown error parsing DB")

        # Parse campsite entries
        try:
            for campsite in db_json["campsites"]:
                if "notification_group" in campsite:
                    campsite["notification_group"] = self.notification_groups[campsite["notification_group"]]
                else:
                    campsite["notification_group"] = NotificationGroup([], [])

                new_entries.append(CampsiteEntry.from_dict(campsite))
        except KeyError as e:
            print(f"Error: DB does not follow proper schema for campsites")
        except BaseException:
            print("Error: Unknown error parsing DB")

        self.campsite_entries = new_entries

    def get_campsites(self):
        return self.campsite_entries
    
# No longer works
if __name__ == "__main__":
    db: CamperDB = CamperDB()

    for entry in db.campsite_entries:
        print("--------------------------------")
        print(entry)

        avail: Availability = Availability(entry.campsite_id, entry.start_date.month, entry.start_date.year)
        available_sites = avail.filter_sites_from_entry(entry)
        for site in available_sites:
            print("SITE IS AVAILABLE")
            print(site)
    