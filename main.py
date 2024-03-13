from typing import Union

from fastapi import FastAPI

import uvicorn

from db.service.camper_db import CamperDB
from client.availability import Availability
from custom_types.custom_types import CampsiteEntry

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hellow": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Test
if __name__ == "__main__":
    db: CamperDB = CamperDB()

    for entry in db.campsite_entries:
        print("--------------------------------")
        print(entry)

        avail: Availability = Availability(
            entry.campsite_id, 
            entry.start_date.month, 
            entry.start_date.year)
        
        available_sites = avail.filter_sites_from_entry(entry)
        for site in available_sites:
            print(f"SITE {site} IS AVAILABLE")

    uvicorn.run(app, host="0.0.0.0", port=8000)

# https://www.recreation.gov/api/camps/availability/campground/232447/month?start_date=2024-04-01T00%3A00%3A00.000Z
# Types of availability: "Reserved" "Closed" "Available" <-- we want available
# max_num_people >= 4