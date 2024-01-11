import os
import pandas as pd
from utilities import TableTruncate, TableLoadfile
from dotenv import load_dotenv

load_dotenv()


File_name  :str = None
Data_path  :str = os.getenv("DATA_PATH")
Table_name :str = os.getenv("TB_NAME")




File_name = "1996Aug.csv"


# TableTruncate(Table_name)
# TableLoadfile(Table_name, File_name)




