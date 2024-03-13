from typing import Union

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hellow": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# https://www.recreation.gov/api/camps/availability/campground/232447/month?start_date=2024-04-11T00%3A00%3A00.000Z
# Types of availability: "Reserved" "Closed" "Available" <-- we want available
# max_num_people >= 4