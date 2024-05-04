from logging import Logger
from sqlite3 import connect


class SqliteDriver:
    def __init__(self, file: str, logger: Logger):
        """
        Initialise a SqliteDriver instance
        """
        self.db_file = file
        self.logger = logger
        self.conn = None

    def connect(self):
        """
        Connect to the sqlite database
        """
        self.conn = self.__connect_to_sqlite()

    def close(self):
        """
        Close the connection to the sqlite database
        """
        self.conn.close()

    def __connect_to_sqlite(self):
        """
        Connect to the SQLite database

        :returns: A database connection instance
        :rtype: Connection (part of Sqlite3)
        """
        conn = None
        try:
            conn = connect(self.db_file)
            self.logger.debug(f"Successfully connected to {self.db_file}")
        except Exception as e:
            self.logger.error(f"Error connecting to {self.db_file}: {e}")

        return conn
