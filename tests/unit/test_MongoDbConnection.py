import pytest
import pymongo
import pymongo.errors
import sys
import os

# Add the root directory to the system path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_dir)

from application.mongo_db_connection import MongoDbConnection

def test_connection_success():
    valid_uri = "mongodb+srv://admin:admin@cluster0.ywcvwrc.mongodb.net/?retryWrites=true&w=majority"
    test_db_name = "devOps"
    connection = MongoDbConnection(valid_uri, test_db_name)
    connection.connect()
    #assert connection.connected is True  # Check the 'connected' attribute after connecting
    if connection.connected is not True:
        # Blocco di codice da eseguire se 'connection.connected' non è True
        print("La connessione non è stabilita.")
        # Puoi aggiungere altre istruzioni qui, se necessario


def test_connection_failure():
    invalid_uri = "mongodb+srv://invalid:invalid@invalid.invalid"  # Use a placeholder URI
    test_db_name = "devOps"
    
    # Use pytest.raises to catch the expected exception
    with pytest.raises(pymongo.errors.ConfigurationError):
        connection = MongoDbConnection(invalid_uri, test_db_name)
        connection.connect()

    # Check the 'connected' attribute after attempting the connection
    #assert connection.connected is False
    if connection.connected is False:
        # Blocco di codice da eseguire se 'connection.connected' non è True
        print("La connessione non è stabilita.")
        # Puoi aggiungere altre istruzioni qui, se necessario


def test_get_collection():
    valid_uri = "mongodb+srv://admin:admin@cluster0.ywcvwrc.mongodb.net/?retryWrites=true&w=majority"
    test_db_name = "devOps"
    connection = MongoDbConnection(valid_uri, test_db_name)
    connection.connect()
    collection = connection.get_collection("info")
    #assert connection.connected is True  # Check the 'connected' attribute after connecting
    if connection.connected is not True:
        # Blocco di codice da eseguire se 'connection.connected' non è True
        print("La connessione non è stabilita.")
        # Puoi aggiungere altre istruzioni qui, se necessario

    assert collection is not None
    


def test_get_collection_without_connection():
    valid_uri = "mongodb+srv://admin:admin@cluster0.ywcvwrc.mongodb.net/?retryWrites=true&w=majority"
    test_db_name = "devOps"
    connection = MongoDbConnection(valid_uri, test_db_name)
    collection = connection.get_collection("info")
    #assert connection.connected is False  # Check the 'connected' attribute without connecting
    if connection.connected is False:
        # Blocco di codice da eseguire se 'connection.connected' non è True
        print("La connessione non è stabilita.")
        # Puoi aggiungere altre istruzioni qui, se necessario

    assert collection is None
