#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """
    This class interacts with the MySQL database.

    Attributes:
        __engine: The database engine.
        __session: The database session.
    """

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query the current database session.

        Args:
            cls (optional): The class name to filter the query.
                If not provided, returns all objects.

        Returns:
            dict: A dictionary with format {<class_name>.<id>: <object>}.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session.

        Args:
            obj: The object to add.
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session.

        Args:
            obj (optional): The object to delete.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()

    def count(self, cls=None) -> int:
        """
        Returns the number of objects in the storage.

        Args:
            cls (optional): The class name of the objects to count.
                If not provided, counts all objects.

        Returns:
            int: The number of objects in the storage.
        """
        return len(self.all(cls))

    def get(self, cls=None, cls_id=None) -> object:
        """
        Returns the instance object that has the specified class name and id.

        Args:
            cls (optional): The class name of the object to retrieve.
            cls_id(optional): The ID of the object.

        Returns:
            object: The instance object that matches class name and id.
        """
        if cls and cls_id:
            return self.__session.query(cls).filter(cls.id == cls_id).first()
        return None

    def drop_all_tables(self):
        """Drop all tables, useful when testing."""
        self.__engine.execute('SET FOREIGN_KEY_CHECKS = 0')
        self.__session.rollback()
        Base.metadata.drop_all(self.__engine)
        self.__engine.execute('SET FOREIGN_KEY_CHECKS = 1')
        self.reload()
