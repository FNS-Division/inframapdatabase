# Import packages
import os
import pandas as pd
from sqlalchemy import create_engine, inspect
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

# Database URL
db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create an engine to access the database
engine = create_engine(db_url, echo=False)

# Show the tables in the database
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:")
for table in tables:
    print(table)

# Write your SQL query
sql_query = "SELECT * FROM point_of_interest WHERE country_code = 'ESP'"

# Read the query results into a pandas DataFrame
query_output_df = pd.read_sql(sql_query, engine)

# Print the DataFrame
print(query_output_df.head)