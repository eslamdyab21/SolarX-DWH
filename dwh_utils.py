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
        self.cursor = self.connection.cursor(buffered=True)


        self.logger.info("DWH_Utils -> dwh_connect -> done")



    def dwh_close_connection(self):
        self.logger.info("DWH_Utils -> dwh_close_connection -> start")

        self.connection.close()
        self.cursor.close()

        self.logger.info("DWH_Utils -> dwh_close_connection -> done")

    
    def select_query_fetchonce(self, query):
        self.logger.info("DWH_Utils -> select_query_fetchonce -> start")

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        self.logger.info("DWH_Utils -> select_query_fetchonce -> done")
        return result
    

    def select_query_fetchall(self, query):
        self.logger.info("DWH_Utils -> select_query_fetchall -> start")

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        self.logger.info("DWH_Utils -> select_query_fetchall -> done")
        return result


    def insert_query(self, query):
        self.logger.info("DWH_Utils -> insert_query -> start")

        self.cursor.execute(query)
        # self.connection.commit()

        self.logger.info("DWH_Utils -> insert_query -> done")




    def handle_solar_panel_scd2(self, source_id, source_capacity_kwh, source_name):
        self.logger.info("DWH_Utils -> handle_solar_panel_scd2 -> Start")
        query = (
        f"""
            SELECT  
                solar_panel_key,
                capacity_kwh
            FROM 
                dimSolarPanel
            WHERE 
                solar_panel_id = {source_id}
            ORDER BY solar_panel_key DESC LIMIT 1
        """
        )
        querey_result = self.select_query_fetchonce(query)


        if querey_result:
            solar_panel_key, destination_capacity_kwh = querey_result
            if source_capacity_kwh != destination_capacity_kwh:
                self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> Record is there, Updated from source, Insert new record")

                query = (
                f"""
                    INSERT INTO  
                        dimSolarPanel(solar_panel_id, name, capacity_kwh, capacity_start_date, capacity_end_date)
                    VALUES 
                        ({source_id}, {'"' + str(source_name) + '"'}, {source_capacity_kwh}, NOW(), NULL)
                """
                )
                self.insert_query(query)

                self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> Record is there, Updated from source, Update prev date")
                query = (
                f"""
                    UPDATE 
                        dimSolarPanel
                    SET
                        capacity_end_date = NOW()
                    WHERE
                        solar_panel_key = {solar_panel_key}
                """
                )
                self.insert_query(query)

            else:
                self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> Record is there, not updated")

        self.logger.info("DWH_Utils -> handle_solar_panel_scd2 -> End")



    def dwh_solar_panel_insert_new_records(self, source_records):
        self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> start")

        for record in source_records:
            source_id, source_name, source_capacity_kwh = record

            query = (
                f"""
                    SELECT  
                        1
                    FROM 
                        dimSolarPanel
                    WHERE 
                        solar_panel_id = {source_id}
                """
            )
            
            querey_result = self.select_query_fetchonce(query)

            # New record, insert it
            if not querey_result:
                self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> New record, insert it")
                query = (
                    f"""
                        INSERT INTO  
                            dimSolarPanel(solar_panel_id, name, capacity_kwh, capacity_start_date, capacity_end_date)
                        VALUES 
                            ({source_id}, {'"' + str(source_name) + '"'}, {source_capacity_kwh}, NOW(), NULL)
                    """
                )
                self.insert_query(query)

            # The record is there, check if it has been updated to insert a new record for it
            # and update the capacity_end_date for the previous record
            else:
                self.logger.info("DWH_Utils -> dwh_solar_panel_insert_new_records -> Record is there, check update")
                self.handle_solar_panel_scd2(source_id, source_capacity_kwh, source_name)
                

        self.connection.commit()