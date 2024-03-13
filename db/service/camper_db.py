import json

from custom_types.custom_types import CampsiteEntry
from db.service.db_config import DBConfig

class CamperDB:
    def __init__(self, config_file: str = None):
        self.config: DBConfig = DBConfig() if config_file is None else DBConfig(config_file)
        self.campsite_entries: list[CampsiteEntry] = []
        self.refresh_db()

    def __get_db_json(self):
        db_path = self.config.get_db_path()
        with open(db_path) as db_file:
            return json.load(db_file)

    def refresh_db(self):
        new_entries: list[CampsiteEntry] = []
        db_json = self.__get_db_json()

        try:
            for campsite in db_json["campsites"]:
                new_entries.append(CampsiteEntry.from_dict(campsite))
        except KeyError:
            print(f"Error: DB does not follow proper schema")
        except BaseException:
            print("Error: Unknown error parsing DB")

        self.campsite_entries = new_entries

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
    