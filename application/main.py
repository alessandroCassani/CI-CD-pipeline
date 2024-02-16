"""
This script interacts with a MongoDB database to perform user queries.
"""

import atexit
import sys
import pymongo.errors
from mongo_db_connection import MongoDbConnection

URI = "mongodb+srv://admin:admin@cluster0.ywcvwrc.mongodb.net/?retryWrites=true&w=majority"
COLLECTION_NAME = "info"
DB_NAME = 'devOps'

def silent_exit():
    """
    Suppress standard error messages related to the pymongo library.
    """
    sys.stderr.write = lambda x: None


atexit.register(silent_exit)

if __name__ == "__main__":
    # Create a MongoDB connection
    connection = MongoDbConnection(URI, DB_NAME)
    connection.connect()
    # Get the collection
    collection = connection.get_collection(COLLECTION_NAME)
    try:
        user = input('inserire username: ')
        psw = input('inserire password: ')
        dipartimento = input('inserire dipartimento: ')
        # Query the collection to find the matching document
        document = collection.find_one({'user': user, 'psw': psw, 'dipartimento': dipartimento})
        if document:
            print('trovato')
        else:
            print('non trovato')
    except pymongo.errors.PyMongoError as e:
        print(f"MongoDB Error: {e}")
    finally:
        connection.disconnect()
