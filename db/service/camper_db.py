from db_config import DBConfig

class CamperDB:
    def __init__(self, config_file=None):
        self.config = DBConfig() if config_file is None else DBConfig(config_file)

if __name__ == "__main__":
    db = CamperDB()
    print(db.config.get_db_path())