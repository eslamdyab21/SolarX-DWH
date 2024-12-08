import mysql.connector
from dotenv import load_dotenv
import logging
import os



class DWH_Utils():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.dwh_connect()
        

    def dwh_connect(self):
        self.logger.info("DWH_Utils -> dwh_connect -> start")

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
        self.logger.info("DWH_Utils -> dwh_close_connection -> start")

        self.connection.close()
        self.cursor.close()

        self.logger.info("DWH_Utils -> dwh_close_connection -> done")

    
    def select_query(self, query):
        self.logger.info("DWH_Utils -> select_query -> start")

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        self.logger.info("DWH_Utils -> select_query -> done")
        return result
    


    def insert_query(self, query):
        self.logger.info("DWH_Utils -> insert_query -> start")

        self.cursor.execute(query)
        # self.connection.commit()

        self.logger.info("DWH_Utils -> insert_query -> done")



    def dwh_solar_panel_insert_new_records(self, source_records):
        for record in source_records:
            id, name, capacity_kwh = record

            query = (
                f"""
                    SELECT  
                        1
                    FROM 
                        dimSolarPanel
                    WHERE 
                        solar_panel_id = {id}
                """
            )
            
            querey_result = self.select_query(query)
            if not querey_result:
                query = (
                    f"""
                        INSERT INTO  
                            dimSolarPanel(solar_panel_id, name, capacity_kwh, capacity_start_date, capacity_end_date)
                        VALUES 
                            ({id}, {'"' + str(name) + '"'}, {capacity_kwh}, NOW(), NULL)
                    """
                )
                self.insert_query(query)

        self.connection.commit()