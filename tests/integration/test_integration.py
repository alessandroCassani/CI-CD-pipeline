import pytest
import sys
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_dir)

from application.mongo_db_connection import MongoDbConnection

URI= "mongodb+srv://admin:admin@cluster0.ywcvwrc.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "devOps"
COLLECTION_NAME = "info"

connection = MongoDbConnection(URI,DB_NAME)
connection.connect()
collection = connection.get_collection(COLLECTION_NAME)

@pytest.fixture
def db_collection():
    data = {
        "user": "federico",
        "psw": "rossi",
        "dipartimento": "matematica"
    }
    collection.insert_one(data)
    
    yield collection
    connection.disconnect()

def test_connect_and_query_mongodb_found():
    output = collection.find_one({'user': "federico", 'psw': "rossi", 'dipartimento': "matematica"})
    assert output is not None

def test_connect_and_query_mongodb_not_found():
    output = collection.find_one({'user': "prova", 'psw': "prova", 'dipartimento': "prova"})
    assert output is None

if __name__ == "__main":
    pytest.main()
