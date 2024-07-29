# Answer availability queries about the campsite
import datetime
import json

from custom_types.custom_types import CampsiteDate, CampsiteEntry
from time import sleep
from client.client import get_availability, RESPONSE_DATE_FORMAT

# Check if specific site is available between start_date, end_date
# return true if it is
def filter_site(campsite: dict, start_date: datetime.date, end_date: datetime.date):
    available = False

    for date_str, availability in campsite["availabilities"].items():
        parsed_date = datetime.datetime.strptime(date_str, RESPONSE_DATE_FORMAT).date()
        if parsed_date >= start_date and parsed_date <= end_date:
            available = True
            if availability != "Available":
                return False

    return available

class Availability:
    DEFAULT_TTL_SEC: int = 60 * 3
    DEFAULT_HTTP_RETRIES: int = 3
    DEFAULT_RETRY_COOLDOWN_SEC: int = 3

    def __init__(self, campground_id, month=datetime.date.today().month, year=datetime.date.today().year):
        self.campground_id = campground_id
        self.month = month
        self.year = year
        self.last_update = None
        self.refresh_data()

    # Re-fetch fresh data
    # TODO: Handle data that spans multiple months (smush multiple request together?)
    # TTL is in seconds
    def refresh_data(self, ttl: int = DEFAULT_TTL_SEC, retry: int = DEFAULT_HTTP_RETRIES):
        cur_time = datetime.datetime.now()
        if self.last_update is not None and (cur_time - datetime.timedelta(seconds=ttl)) < self.last_update:
            return

        print("Refreshing data")
        try:
            self.data = get_availability(self.campground_id, self.month, self.year)
            self.last_update = datetime.datetime.now()

            # Dump the latest data
            with open('latest_request.json', 'w') as dump_file:
                json.dump(self.data, dump_file)
        except:
            print(f"{datetime.datetime.now()}: HTTP Request to recreation.gov failed. Retries left: {retry}")
            if retry > 0:
                print(f"Retrying in {Availability.DEFAULT_RETRY_COOLDOWN_SEC} seconds")
                sleep(Availability.DEFAULT_RETRY_COOLDOWN_SEC)
                self.refresh_data(ttl, retry - 1)
            else:
                # TODO: Notify that we had an error accessing recreation.gov API
                pass

    # Query functions
    def get_num_campsites(self):
        self.refresh_data()
        return self.data["count"]

    # Return the filtered sites
    def filter_sites_by_capacity(self, num_people: int = 1, campsites: dict = None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if v["min_num_people"] <= num_people and v["max_num_people"] >= num_people}

    def filter_sites_by_date(self, 
            start_date: datetime.date, 
            end_date: datetime.date, 
            campsites: dict = None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if filter_site(v, start_date, end_date)}

    def filter_sites(self, 
            start_date: datetime.date, 
            end_date: datetime.date, 
            num_people: int = 1, 
            campsites: dict = None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]
        campsites = self.filter_sites_by_capacity(num_people, campsites)
        campsites = self.filter_sites_by_date(start_date, end_date, campsites)

        return campsites
    
    def filter_sites_from_entry(self, campsite_entry: CampsiteEntry) -> list[CampsiteEntry]:
        if campsite_entry.campsite_id != self.campground_id:
            raise Exception(
                f"CampsiteEntry and Availability objects are for different \
campground IDs {campsite_entry.campsite_id} and {self.campground_id}") 

        campsite_start_date: datetime.date = campsite_entry.start_date.get_as_date()
        campsite_end_date: datetime.date = campsite_entry.end_date.get_as_date()

        return self.filter_sites(
            campsite_start_date,
            campsite_end_date,
            campsite_entry.num_people
        )

# No longer works
if __name__=="__main__":
    # 232447 is for Upper Pines Yosemite, month/year defaults to current
    availability = Availability(232447, 4, 2024)
    print(availability.get_num_campsites())

    start = datetime.date(2024, 4, 8)
    end = datetime.date(2024, 4, 8)
    print(availability.filter_sites(start, end, 4).keys())

    print(availability.get_num_campsites())
    sleep(1)
    print(availability.get_num_campsites())
    sleep(2)
    print(availability.get_num_campsites())
    sleep(2)
    print(availability.get_num_campsites())
    sleep(4)
    print(availability.get_num_campsites())
    sleep(1)
    print(availability.get_num_campsites())
    sleep(5)
    print(availability.get_num_campsites())
    sleep(5)
    print(availability.get_num_campsites())
