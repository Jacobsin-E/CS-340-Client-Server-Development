"""
CRUD_Python_Module.py

A reusable Python module that provides Create, Read, Update, and Delete (CRUD)
operations for the Austin Animal Center (AAC) outcomes data stored in MongoDB.
Built for Grazioso Salvare by Global Rain.

Author: Jacobsin Enriquez
Course: CS 340 Client/Server Development
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password, host='localhost', port=27017,
                 db_name='aac', collection_name='animals'):
        """
        Opens an authenticated connection to the MongoDB database.
        :param username: MongoDB user name (e.g. 'aacuser').
        :param password: Password for the MongoDB user.
        :param host: Database host name (defaults to 'localhost').
        :param port: Database port number (defaults to 27017).
        :param db_name: Name of the database (defaults to 'aac').
        :param collection_name: Name of the collection (defaults to 'animals').
        """
        # URL encode the credentials to handle special characters safely
        encoded_user = urllib.parse.quote_plus(username)
        encoded_password = urllib.parse.quote_plus(password)

        # Connect to the database using the provided credentials.
        # aacuser was created in the admin database, so authSource=admin.
        self.client = MongoClient(
            f'mongodb://{encoded_user}:{encoded_password}@{host}:{port}/{db_name}?authSource=admin'
        )
        self.database = self.client[db_name]
        self.collection = self.database[collection_name]

    def create(self, data):
        """
        Inserts a document into the specified MongoDB database and collection.
        :param data: Dictionary containing key/value pairs to insert.
        :return: True if successful, False otherwise.
        """
        if data is not None:
            try:
                insert_result = self.collection.insert_one(data)
                return True if insert_result.acknowledged else False
            except Exception as e:
                print(f"An error occurred during creation: {e}")
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, query):
        """
        Queries for documents from the specified MongoDB database and collection.
        :param query: Dictionary containing key/value lookup pairs.
        :return: List of matching documents, or an empty list if none found.
        """
        if query is not None:
            try:
                # find() returns a cursor; cast to a list to satisfy the rubric
                cursor = self.collection.find(query)
                return list(cursor)
            except Exception as e:
                print(f"An error occurred during read: {e}")
                return []
        else:
            raise Exception("Nothing to read, because query parameter is empty")

    def update(self, query, new_values):
        """
        Queries for and changes document(s) in the specified MongoDB database
        and collection.
        :param query: Dictionary containing key/value lookup pairs that select
                      the document(s) to change.
        :param new_values: Dictionary of changes in the format accepted by
                           update_many(), e.g. {"$set": {"name": "Max"}}.
                           A plain dictionary such as {"name": "Max"} is
                           wrapped in "$set" automatically.
        :return: The number of documents modified (0 if none or on error).
        """
        if query is not None and new_values:
            try:
                # Wrap plain key/value pairs in $set so callers can pass either
                # an update operator document or a simple dictionary of fields
                if not any(key.startswith('$') for key in new_values):
                    new_values = {"$set": new_values}

                # update_many() changes every document that matches the query
                update_result = self.collection.update_many(query, new_values)
                return update_result.modified_count
            except Exception as e:
                print(f"An error occurred during update: {e}")
                return 0
        else:
            raise Exception("Nothing to update, because query or new_values parameter is empty")

    def delete(self, query):
        """
        Queries for and removes document(s) from the specified MongoDB database
        and collection.
        :param query: Dictionary containing key/value lookup pairs that select
                      the document(s) to remove.
        :return: The number of documents removed (0 if none or on error).
        """
        if query is not None:
            try:
                # Guard against an empty query, which would delete every document
                if len(query) == 0:
                    raise ValueError("An empty query would delete the entire collection")

                # delete_many() removes every document that matches the query
                delete_result = self.collection.delete_many(query)
                return delete_result.deleted_count
            except Exception as e:
                print(f"An error occurred during delete: {e}")
                return 0
        else:
            raise Exception("Nothing to delete, because query parameter is empty")
