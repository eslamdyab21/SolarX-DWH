import mysql.connector
from dotenv import load_dotenv
import logging
import os



class DB_Utils():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db_connect()
        

    def db_connect(self):
        self.logger.info("DB_Utils -> db_connect -> start")

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
        self.logger.info("DB_Utils -> db_close_connection -> start")

        self.connection.close()
        self.cursor.close()

        self.logger.info("DB_Utils -> db_close_connection -> done")


    def select_query(self, query):
        self.logger.info("DB_Utils -> select_query -> start")

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.logger.info("DB_Utils -> select_query -> done")
        return result
    

    def db_retrive_dim_solar_panels(self):
        self.logger.info("DB_Utils -> db_retrive_dim_solar_panels -> start")
        query = (
                """
                    SELECT  
                        id, 
                        name, 
                        capacity_kwh
                    FROM 
                        Solar_pannels;
                """
            )
        
        result = self.select_query(query)

        self.logger.info("DB_Utils -> db_retrive_dim_solar_panels -> done")
        return result