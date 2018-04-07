from sqlalchemy import MetaData, Table, create_engine, Column, Integer, String
import unittest

username = "dev"
password = "dev"
host = "0.0.0.0"
port = "3306"
database = "sentiment"

info = "mysql://{}:{}@{}:{}/{}".format(username, password, host, port, database)

engine = create_engine(info)

class TestDBUtil(unittest.TestCase):
    
    def test_get_recent_reddit(self):
        self.assertEqual(5, len(database.get_recent_reddit("all").head()))
        self.assertEqual(5, len(database.get_recent_reddit("").head()))


if __name__ == "__main__":
    from DBUtil import database
    unittest.main()

