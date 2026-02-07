import json
import os

import dotenv
import pytest
from pymongo import MongoClient
from starlette.testclient import TestClient
from testcontainers.mongodb import MongoDbContainer

from commons.utils.database import db_manager, get_database
from main import app


def pytest_sessionstart(session):
    """
    Session level hook for loading the environment variables.
    :param session:
    :return:
    """
    dotenv_path = os.path.join(os.path.dirname(__file__),'..','.env')
    dotenv.load_dotenv(dotenv_path)

    test_env_path = os.path.join(os.path.dirname(__file__),'..','.test.env')
    if os.path.exists(test_env_path):
        dotenv.load_dotenv(test_env_path,override=True)


@pytest.fixture(scope="session", autouse=True)
def mongo_container():
    with MongoDbContainer("mongo:latest") as mongo_client:
        yield mongo_client


@pytest.fixture(scope="session")
def db_client(mongo_container, request):
    test_mongo_uri = mongo_container.get_connection_url()
    client = MongoClient(test_mongo_uri, uuidRepresentation="standard")
    yield client


@pytest.fixture(scope="session")
def clean_database(db_client):
    db_name = "test_db"
    db_client.drop_database(db_name)
    yield db_client

    db_client.close()
    db_manager.close()

@pytest.fixture(scope="session")
def client(db_client):
    """
    Configures a test database for the application and provides a test client wrapped
    in a context manager for testing purposes. Overrides the default database dependency
    of the application to use a test database.

    :param db_client: The database client used to create and fetch the test database.
    :type db_client: Any
    :return: A testing client configured to use the test database.
    :rtype: Generator[TestClient, None, None]
    """
    test_db_name = "test_db"

    def get_test_database():
        return db_client.get_database(test_db_name)

    app.dependency_overrides[get_database] = get_test_database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def read_data_from_file():
    with open('tests/test_data.json', 'r') as file:
        test_data = json.load(file)
    yield test_data

@pytest.fixture(scope="session")
def get_test_email_data(read_data_from_file):
    return read_data_from_file['test_emails'][0]