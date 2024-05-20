# Import packages
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
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

# Define the data types and filenames
data_info = {
    "pointofinterest": "ESP-1697915895-xs2u-pointofinterest.csv",
    "cellsite": "ESP-1697916284-6wv8-cellsite.csv",
    "transmissionnode": "ESP-1697916384-1icf-transmissionnode.csv"
}

# Create a dictionary to hold the data
data_dict = {}

# Loop through the data_info dictionary and read each CSV file
for data_type, filename in data_info.items():
    filepath = os.path.join(os.getcwd(), "data", "ESP", "processed", data_type, filename)
    data_dict[data_type] = pd.read_csv(filepath)

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

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Use pandas.to_sql for bulk insertion

    # POI data
try:
    data_dict["pointofinterest"].to_sql("point_of_interest", engine, index=False, if_exists='append')
    print("POI data added to the database.")
except Exception as e:
    print("Error:", e)

    # Cell site data
try:
    data_dict["cellsite"].to_sql("cell_site", engine, index=False, if_exists='append')
    print("Cell site data added to the database.")
except Exception as e:
    print("Error:", e)

    # Transmission node data
try:
    data_dict["transmissionnode"].to_sql("transmission_node", engine, index=False, if_exists='append')
    print("Transmission node data added to the database.")
except Exception as e:
    print("Error:", e)

# Commit the changes
session.commit()