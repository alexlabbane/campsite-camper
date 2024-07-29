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
class NotificationGroup:
    email: list[str]
    whatsapp: list[str]

    @staticmethod
    def from_dict(obj: dict):
        return NotificationGroup(
            obj["email"],
            obj["whatsapp"]    
        )

    def __str__(self):
        return f"Email: {','.join(self.email)}\n\
    WhatsApp: {','.join(self.whatsapp)}"

@dataclass
class CampsiteEntry:
    campsite_id: str
    start_date: CampsiteDate
    end_date: CampsiteDate
    num_people: int
    reserve_url: str
    notification_group: NotificationGroup

    @staticmethod
    def from_dict(obj: dict):
        campsite_id = obj["campsite_id"]
        return CampsiteEntry(
            campsite_id,
            CampsiteDate.from_dict(obj["start_date"]),
            CampsiteDate.from_dict(obj["end_date"]),
            obj["num_people"],
            f"https://www.recreation.gov/camping/campgrounds/{campsite_id}",
            obj["notification_group"]
        )
    
    def __str__(self):
        return f"🏕️  Campsite {self.campsite_id} 🏕️\n\
    Start Date: {self.start_date.get_as_date()}\n\
    End Date:   {self.end_date.get_as_date()}\n\
    Number of Campers: {self.num_people}\n\
    {self.notification_group.__str__()}"