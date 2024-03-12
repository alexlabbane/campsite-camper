# Answer availability queries about the campsite
import datetime
from time import sleep
from client import get_availability, RESPONSE_DATE_FORMAT

# Check if specific site is available between start_date, end_date
# return true if it is
def filter_site(campsite, start_date, end_date):
    available = False

    for date_str, availability in campsite["availabilities"].items():
        parsed_date = datetime.datetime.strptime(date_str, RESPONSE_DATE_FORMAT).date()
        if parsed_date >= start_date and parsed_date <= end_date:
            available = True
            if availability != "Available":
                return False

    return available

class Availability:
    DEFAULT_TTL_SEC = 60 * 5
    DEFAULT_HTTP_RETRIES = 3
    DEFAULT_RETRY_COOLDOWN_SEC = 3

    def __init__(self, campground_id, month=datetime.date.today().month, year=datetime.date.today().year):
        self.campground_id = campground_id
        self.month = month
        self.year = year
        self.last_update = None
        self.refresh_data()

    # Re-fetch fresh data
    # TODO: Handle data that spans multiple months (smush multiple request together?)
    # TTL is in seconds
    def refresh_data(self, ttl=DEFAULT_TTL_SEC, retry=DEFAULT_HTTP_RETRIES):
        cur_time = datetime.datetime.now()
        if self.last_update is not None and (cur_time - datetime.timedelta(seconds=ttl)) < self.last_update:
            return

        try:
            self.data = get_availability(self.campground_id, self.month, self.year)
            self.last_update = datetime.datetime.now()
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
    def filter_sites_by_capacity(self, num_people=1, campsites=None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if v["min_num_people"] <= num_people and v["max_num_people"] >= num_people}

    def filter_sites_by_date(self, start_date, end_date, campsites=None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if filter_site(v, start_date, end_date)}

    def filter_sites(self, start_date, end_date, num_people=1, campsites=None):
        self.refresh_data()
        if campsites is None:
            campsites = self.data["campsites"]
        campsites = self.filter_sites_by_capacity(num_people, campsites)
        campsites = self.filter_sites_by_date(start_date, end_date, campsites)

        return campsites

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
