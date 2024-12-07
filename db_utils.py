import mysql.connector
from dotenv import load_dotenv
import logging
import os



class DB_Utils():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connect()
        

    def db_connect(self):

        load_dotenv()
        self.connection = mysql.connector.connect(
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
        )
        self.cursor = self.connection.cursor()


        self.logger.info("DB_Utils -> db_connect -> done")



    def db_close_connection(self):
        self.connection.close()
        self.cursor.close()

        self.logger.info("DB_Utils -> db_close_connection -> done")