from pymongo import MongoClient

from commons.app_settings import get_settings


class MongoDbManager:
    client: MongoClient
    db = None

    def connect(self):
        self.client = MongoClient(
            get_settings().db_url,
            uuidRepresentation="standard"
        )
        self.db = self.client.get_database(get_settings().db_name)

    def close(self):
        if self.client:
            self.client.close()

db_manager = MongoDbManager()

def get_database():
    return db_manager.db