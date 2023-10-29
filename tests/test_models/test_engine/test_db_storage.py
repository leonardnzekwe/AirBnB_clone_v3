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
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/db_storage.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            [
                "tests/test_models/test_engine/\
test_db_storage.py"
            ]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(
            db_storage.__doc__, None, "db_storage.py needs a docstring"
        )
        self.assertTrue(
            len(db_storage.__doc__) >= 1, "db_storage.py needs a docstring"
        )

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(
            DBStorage.__doc__, None, "DBStorage class needs a docstring"
        )
        self.assertTrue(
            len(DBStorage.__doc__) >= 1, "DBStorage class needs a docstring"
        )

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(
                func[1].__doc__, None, "{:s} method needs a docstring".format(
                    func[0]
                    )
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """set up class"""
        # Create objects of different classes and add them to the database
        cls.storage = models.storage
        cls.amenity = Amenity(name="Food")
        cls.storage.new(cls.amenity)
        cls.state = State(name="Lagos")
        cls.storage.new(cls.state)
        cls.storage.save()
        cls.city = City(name="Arizona", state_id=cls.state.id)
        cls.storage.new(cls.city)
        cls.user = User(
            first_name="Leonard",
            last_name="nzekwe",
            email="leo@nze.com",
            password="ifniofn43ifn",
        )
        cls.storage.new(cls.user)
        cls.storage.save()
        cls.place = Place(
            name="Lagos", city_id=cls.city.id, user_id=cls.user.id
        )
        cls.storage.new(cls.place)
        cls.storage.save()
        cls.review = Review(
            place_id=cls.place.id, user_id=cls.user.id, text="Awesome"
        )
        cls.storage.new(cls.review)
        cls.storage.save()

    @classmethod
    def tearDownClass(cls):
        """set up class"""
        cls.storage.close()

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        all_objects = self.storage.all()
        self.assertIs(type(all_objects), dict)

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        # Get all objects without specifying a class
        all_objects = self.storage.all()
        # Check that all objects are present in the result
        self.assertIn(self.state, all_objects.values())
        self.assertIn(self.city, all_objects.values())
        self.assertIn(self.amenity, all_objects.values())
        self.assertIn(self.user, all_objects.values())

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        # Retrieve the object from the database
        retrieved_obj = self.storage.get(State, self.state.id)
        # Check that the retrieved object is the same as the original
        self.assertEqual(retrieved_obj, self.state)

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        # Retrieve the object from the database
        retrieved_obj = self.storage.get(Review, self.review.id)
        # Check that the retrieved object is the same as the original
        self.assertEqual(retrieved_obj, self.review)

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_get(self):
        """Test that get retrieves an object from the database"""
        # Retrieve the object from the database using get
        retrieved_obj = self.storage.get(Place, self.place.id)
        # Check that the retrieved object is the same as the original
        self.assertEqual(retrieved_obj, self.place)

    @unittest.skipIf(models.storage_t != "db", "not testing database storage")
    def test_count(self):
        """Test that count properly counts objects in the database"""
        # Count the number of User objects in the database
        count = self.storage.count(User)
        # Check that the count is 1 since we added one User object
        self.assertGreater(count, 0)
