import requests
import datetime

# HTTP Status Codes
HTTP_STATUS_OK = 200

# Defaults
USER_AGENT = "Mozilla/5.0"

# Date Formatting
REQUEST_DATE_FORMAT = "%Y-%m-%dT00:00:00.000Z"
RESPONSE_DATE_FORMAT = "%Y-%m-%dT00:00:00Z"

# URLs
BASE_URL = "https://www.recreation.gov/api"
CAMPGROUND_AVAILABILITY = BASE_URL + "/camps/availability/campground/{CAMPGROUND_ID}/month"

def get_availability(campground_id, month=datetime.date.today().month, year=datetime.date.today().year):
    date = datetime.date(year, month, 1)
    params = {
        "start_date": datetime.date.strftime(date, REQUEST_DATE_FORMAT) 
    }
    headers = {
        "User-Agent": USER_AGENT
    }

    request_url = CAMPGROUND_AVAILABILITY.format(CAMPGROUND_ID=campground_id)
    
    print(request_url)
    res = requests.get(request_url, params=params, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Error code {res.status_code} received for API request {request_url}")
    return res.json()

if __name__=="__main__":
    # 232447 is for Upper Pines Yosemite, month/year defaults to current
    get_availability(232447)

# https://www.recreation.gov/api/camps/availability/campground/232447/month?start_date=2024-04-01T00%3A00%3A00.000Z
