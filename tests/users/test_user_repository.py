import uuid

from commons.utils import app_utils
from commons.utils.app_settings import get_settings
from users.db_user_model import UserDbModel
from users.user_repository import create_user, get_user_by_id, get_user_by_hashed_email


def test_create_user(db_client, test_user_data):
    # Given
    test_db = db_client.get_database(get_settings().db_name)
    actual_user_data = UserDbModel(**test_user_data)

    # When
    user_id = create_user(actual_user_data, test_db)
    created_user = get_user_by_id(user_id, test_db)

    assert created_user.email == actual_user_data.email
    assert created_user.display_name == actual_user_data.display_name
    assert created_user.role == actual_user_data.role
    assert created_user.hashed_email == actual_user_data.hashed_email
    assert created_user.password == actual_user_data.password


def test_get_user_by_hashed_email(db_client, test_user_data):
    # Given
    test_db = db_client.get_database(get_settings().db_name)
    actual_user_data = UserDbModel(**test_user_data)
    create_user(actual_user_data, test_db)

    saved_user = get_user_by_hashed_email(actual_user_data.hashed_email, test_db)

    assert saved_user.email == actual_user_data.email
    assert saved_user.display_name == actual_user_data.display_name
    assert saved_user.role == actual_user_data.role
    assert saved_user.hashed_email == actual_user_data.hashed_email
    assert saved_user.password == actual_user_data.password


def test_get_user_by_hashed_email_no_user_exists(db_client, test_user_data):
    # Given
    test_db = db_client.get_database(get_settings().db_name)

    actual_email = "sample_email@example.com"
    hashed_email = app_utils.hash_email(actual_email)

    saved_user = get_user_by_hashed_email(hashed_email, test_db)

    assert saved_user is None


def test_get_user_by_id_negative(db_client):
    # Given
    generated_id = uuid.uuid4()
    test_db = db_client.get_database(get_settings().db_name)

    saved_user = get_user_by_id(generated_id, test_db)

    assert saved_user is None


