from db_utils import DB_Utils 
from dwh_utils import DWH_Utils 
from logging_config import setup_logging
import logging



def main():
    # connect 
    db = DB_Utils()
    dwh = DWH_Utils()
    
    querey_res = db.db_retrive_dim_solar_panels()
    dwh.dwh_solar_panel_insert_new_records(querey_res)
    


    
    # close connection
    db.db_close_connection()
    dwh.dwh_close_connection()



if __name__ == "__main__":
    setup_logging()
    logging.getLogger(__name__).info("ETL Started")
    main()