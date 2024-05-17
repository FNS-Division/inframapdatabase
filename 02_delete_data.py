# Import packages
import os
import pandas as pd
from mysql import connector

# Load database credentials
# If you wish to you use your local database, run the following line instead:
    # from credentials.local_db_credentials import db_name, db_user, db_password, db_host, db_port

from credentials.aws_db_credentials import db_name, db_user, db_password, db_host, db_port

# Create a connection to the database
try: 
    # Connect to existing database
    with connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
    ) as existing_database:
        # Write the SQL query to delete a record
        # In this example, we are deleting all records from the point_of_interest table where the country_code is 'ESP'
        drop_record = "DELETE FROM point_of_interest WHERE country_code = 'ESP'"
        with existing_database.cursor() as cursor:
            cursor.execute(drop_record)
            existing_database.commit()
except connector.Error as e: 
    print(e)