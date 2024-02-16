"""
mongo_db_connection.py

A module for managing connections to a MongoDB database using pymongo.
"""

import pymongo

class MongoDbConnection:
    """
    A class for managing connections to a MongoDB database using pymongo.

    Attributes:
        connection_uri (str): The connection URI for the MongoDB database.
        database_name (str): The name of the MongoDB database.
        client (pymongo.MongoClient): The MongoDB client object.
        collection (pymongo.collection.Collection): The currently selected collection.
        db (pymongo.database.Database): The MongoDB database object.
        connected (bool): Indicates whether the connection to MongoDB is established.

    Methods:
        connect(): Establishes a connection to the MongoDB database.
        disconnect(): Closes the connection to the MongoDB database.
        get_collection(collection_name): Returns a MongoDB collection by name.
    """
    def __init__(self, connection_uri, database_name):
        """
        Initializes a new MongoDbConnection instance.

        Args:
            connection_uri (str): The connection URI for the MongoDB database.
            database_name (str): The name of the MongoDB database.
        """
        self.connection_uri = connection_uri
        self.database_name = database_name
        self.client = None
        self.collection = None
        self.database = None
        self.connected = False

    def connect(self):
        """
        Establishes a connection to the MongoDB database.
        """
        try:
            self.client = pymongo.MongoClient(
                self.connection_uri,
                ssl=True,
                tlsAllowInvalidCertificates=True,
            )
            self.database = self.client[self.database_name]
            self.connected = True
            print("Connected to MongoDB Atlas")
        except pymongo.errors.ConnectionFailure as e:
            self.connected = False
            print(f"Error during connection: {e}")

    def disconnect(self):
        """
        Closes the connection to the MongoDB database.
        """
        if self.client:
            self.client.close()
            self.connected = False
            print("Disconnected from MongoDB Atlas")

    def get_collection(self, collection_name):
        """
        Returns a MongoDB collection by name.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            pymongo.collection.Collection: The requested MongoDB collection or None.
        """
        if self.database is not None:
            return self.database[collection_name]
        self.connected = False
        return None
