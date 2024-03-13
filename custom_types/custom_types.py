from dataclasses import dataclass
import datetime

@dataclass
class CampsiteDate:
    month: int
    day: int
    year: int

    def get_as_date(self):
        return datetime.date(self.year, self.month, self.day)

    @staticmethod
    def from_dict(obj: dict):
        return CampsiteDate(obj["month"], obj["day"], obj["year"])

@dataclass
class CampsiteEntry:
    campsite_id: str
    start_date: CampsiteDate
    end_date: CampsiteDate
    num_people: int

    @staticmethod
    def from_dict(obj: dict):
        return CampsiteEntry(
            obj["campsite_id"],
            CampsiteDate.from_dict(obj["start_date"]),
            CampsiteDate.from_dict(obj["end_date"]),
            obj["num_people"]
        )
    
    def __str__(self):
        return f"🏕️  Campsite {self.campsite_id} 🏕️\n\
    Start Date: {self.start_date.get_as_date()}\n\
    End Date:   {self.end_date.get_as_date()}\n\
    Number of Campers: {self.num_people}"
    