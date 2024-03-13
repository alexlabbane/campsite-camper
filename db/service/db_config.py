import json

class DBConfig:
    DB_CONFIG_INDENT_LEVEL=4
    KEY_DB_PATH = "db_path"

    def __init__(self, config_file = "./db/service/default_config.json"):
        self.config_file = config_file
        self.refresh_config()

    def __get_config(self):
        with open(self.config_file) as config_file:
            return json.load(config_file)

    def __set_config(self, new_config):
        with open(self.config_file, 'w') as config_file:
            json.dump(new_config, config_file, indent=DBConfig.DB_CONFIG_INDENT_LEVEL)

    def refresh_config(self):
        config_json = self.__get_config()

        self.db_path = config_json[DBConfig.KEY_DB_PATH]

    def rewrite_config(self):
        new_config = self.__get_config()

        # Update the old_config data members
        new_config[DBConfig.KEY_DB_PATH] = self.db_path

        self.__set_config(new_config)

    # Get DB Config data members
    def get_db_path(self):
        return self.db_path

    def update_db_path(self, new_path):
        self.db_path = new_path
        self.rewrite_config()

if __name__ == "__main__":
    config = DBConfig()
    original_path = config.get_db_path()
    print(original_path)
    config.update_db_path("test_db_path")

    config_instance_2 = DBConfig()
    print(config_instance_2.get_db_path())
    config_instance_2.update_db_path(original_path)
    print(config_instance_2.get_db_path())
