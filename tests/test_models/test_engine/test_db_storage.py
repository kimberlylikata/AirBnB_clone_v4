#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
from os import getenv
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


@unittest.skipUnless(getenv('HBNB_TYPE_STORAGE') == "db", "testing DBStorage")
class TestDBStorage(unittest.TestCase):
    """Tests the DBStorage."""

    def setUp(self) -> None:
        """Set up method that runs before each test case."""
        models.storage.drop_all_tables()

    def test_count_when_empty(self):
        """Test that the `count` method returns zero when nothing exists."""
        self.assertTrue(models.storage.count() == 0)

    def test_count_all_objects(self):
        """Test that the `count` method returns the right number of objects."""
        for i in range(1, 11):
            state = State(name=f"State_{i}")
            state.save()
            City(name=f"City_{i}", state_id=state.id).save()

        self.assertEqual(models.storage.count(), 20)

    def test_count_with_model_name(self):
        """Test that the `count` method returns the right number of objects for
        a particular class."""
        State(name="Arizona").save()
        State(name="California").save()

        self.assertEqual(models.storage.count(State), 2)

    def test_get_with_non_existent(self):
        """Test that the `get` method returns None for non-existent objects."""
        self.assertIsNone(models.storage.get(User, 'abcd-1234-test-5678'))

    def test_get_with_class_only(self):
        """Test that the `get` method operates correctly when only the class
        argument is passed."""
        self.assertIsNone(models.storage.get(User))

    def test_get_with_valid_class(self):
        """Test that the `get` method returns the right object."""
        state = State(name="Greater Accra")
        state.save()

        # test for state instance
        self.assertEqual(models.storage.get(
            State, state.id), state)

        city = City(name="Tema", state_id=state.id)
        city.save()
        self.assertEqual(models.storage.get(
            City, city.id), city)
