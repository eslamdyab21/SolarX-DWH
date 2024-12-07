from db_utils import DB_Utils 
from logging_config import setup_logging
import logging



def main():
    db = DB_Utils()
    connection = db.connection 
    cursor = db.cursor
    

    db.db_close_connection()


if __name__ == "__main__":
    setup_logging()
    logging.getLogger(__name__).info("ETL Started")
    main()