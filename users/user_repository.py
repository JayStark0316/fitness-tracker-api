from pymongo.synchronous.database import Database
from users.db_user_model import UserDbModel
from uuid import uuid4

COLLECTION_NAME = "users"

def get_user_by_id(user_id: str, db: Database) -> UserDbModel | None:
    _document = db.get_collection(COLLECTION_NAME).find_one({"_id": user_id})
    return UserDbModel(**_document) if _document else None


def get_user_by_hashed_email(email: str, db: Database):
    _document = db.get_collection(COLLECTION_NAME).find_one({"hashed_email": email})
    return UserDbModel(**_document) if _document else None


def create_user(user_db: UserDbModel, db: Database):
    model_db = user_db.model_dump(by_alias=True)
    generated_id = uuid4()
    model_db['_id'] = generated_id
    inserted_id = db.get_collection(COLLECTION_NAME).insert_one(model_db).inserted_id
    return inserted_id