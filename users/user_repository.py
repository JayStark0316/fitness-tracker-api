from pymongo.synchronous.database import Database

from users.db_user_model import UserDbModel

COLLECTION_NAME = "users"

def get_user_by_id(id: str, db: Database):
    pass

def get_user_by_hashed_email(email: str, db: Database):
    pass

def create_user(user_db: UserDbModel):
    pass