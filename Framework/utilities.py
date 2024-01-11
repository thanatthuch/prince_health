"""Utilities for mysql
Method:
    - Truncate table
    - Insert into
"""


import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
TB_NAME = os.getenv("TB_NAME")
SRC_PATH= os.getenv("SRC_PATH")

def TableTruncate(tbl_name: str, stage: str = "raw") -> None:
    """test"""
    if stage == "persist":
        DATABASE = os.getenv("DB_PST")
    else:
        DATABASE = os.getenv("DB_RAW")


    connection = mysql.connector.connect(
    host= DB_HOST,
    user= DB_USER,
    password= DB_PASS,
    database= DATABASE
    )

    cursor = connection.cursor()

    Command = f"TRUNCATE TABLE {tbl_name}"
    try:
        cursor.execute(Command)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied error: Check your credentials.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database `{DATABASE}` does not exist.")
        elif err.errno == errorcode.ER_DBACCESS_DENIED_ERROR:
            print("Access denied for database.")
        elif err.errno == errorcode.ER_NO_SUCH_TABLE:
            print(f"Table `{DATABASE}`.`{tbl_name}` does not exist.")
        else:
            print(f"Error: {err}")
    else:
        connection.close()
        print(f"Truncate `{DATABASE}`.`{tbl_name}` Done.")



def TableLoadfile(tbl_name: str, File_name: str) -> None:
    """
    - This function will be load CSV file into table.
    """
    DATABASE = os.getenv("DB_RAW")
    Full_path = SRC_PATH + "/" + File_name

    connection = mysql.connector.connect(
    host= DB_HOST,
    user= DB_USER,
    password= DB_PASS,
    database= DATABASE
    )

    cursor = connection.cursor()


    Command = f"""
        LOAD DATA INFILE '{Full_path}'
        INTO TABLE {tbl_name}
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS;
    """
    try:
        cursor.execute(Command)
    except mysql.connector.Error as err:
        raise(err)
    else:
        cursor.close()
        connection.commit()
        connection.close()
        print(f"LoadData `[{File_name}]` into `{DATABASE}`.`{tbl_name} Succeeded.`")



