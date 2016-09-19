import tempfile
import unittest
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.session import Session
import cssefserver

class CreateDatabaseConnectionTest(unittest.TestCase):
    """Tests cssefserver.utils.create_database_connection
    """
    def test_blank(self):
        db_conn = cssefserver.databaseutils.create_database_connection()
        self.assertTrue(isinstance(db_conn, Session))

    def test_file_path(self):
        settings_file = tempfile.NamedTemporaryFile()
        db_conn = cssefserver.databaseutils.create_database_connection(settings_file.name)
        self.assertTrue(isinstance(db_conn, Session))

    def test_bad_path(self):
        database_file_path = '/no/such/path'
        with self.assertRaises(Exception) as context:
            cssefserver.databaseutils.create_database_connection(database_file_path)
        self.assertTrue('unable to open database file' in str(context.exception))