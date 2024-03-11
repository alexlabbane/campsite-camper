# Answer availability queries about the campsite
import datetime
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
    def __init__(self, campground_id, month=datetime.date.today().month, year=datetime.date.today().year):
        self.campground_id = campground_id
        self.month = month
        self.year = year
        self.refresh_data()

    # Re-fetch fresh data
    # TODO: Handle data that spans multiple months (smush multiple request together?)
    def refresh_data(self):
        try:
            self.data = get_availability(self.campground_id, self.month, self.year)
            self.last_update = datetime.datetime.now()
        except:
            print(f"{datetime.datetime.now()}: HTTP Request to recreation.gov failed")
            pass

    # Query functions
    def get_num_campsites(self):
        return self.data["count"]

    # Return the filtered sites
    def filter_sites_by_capacity(self, num_people=1, campsites=None):
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if v["min_num_people"] <= num_people and v["max_num_people"] >= num_people}



    def filter_sites_by_date(self, start_date, end_date, campsites=None):
        if campsites is None:
            campsites = self.data["campsites"]

        return {k:v for k,v in campsites.items() if filter_site(v, start_date, end_date)}

    def filter_sites(self, start_date, end_date, num_people=1, campsites=None):
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