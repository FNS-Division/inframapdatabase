# Import packages
import os
import pandas as pd
from mysql import connector
from dotenv import load_dotenv

# Set the .env file path based on the environment
server = "aws" # aws or local
if server == "aws":
  env_file_path = "credentials/.env.aws"
else:
  env_file_path = "credentials/.env.local"

# Load the environment variables from the path
load_dotenv(env_file_path)

# Get environment variables
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

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