import mysql.connector
from dotenv import load_dotenv
import logging
import os



class DWH_Utils():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dwh_connect()
        

    def dwh_connect(self):

        load_dotenv()
        self.connection = mysql.connector.connect(
            host=os.getenv('DWH_HOST'),
            port=os.getenv('DWH_PORT'),
            user=os.getenv('DWH_USER'),
            password=os.getenv('DWH_PASSWORD'),
            database=os.getenv('DWH_NAME'),
        )
        self.cursor = self.connection.cursor()


        self.logger.info("DWH_Utils -> dwh_connect -> done")



    def dwh_close_connection(self):
        self.connection.close()
        self.cursor.close()

        self.logger.info("DWH_Utils -> dwh_close_connection -> done")