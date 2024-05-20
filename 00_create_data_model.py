# Import the module containing functions for creating the database schema
import os
from dotenv import load_dotenv
import datamodel

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

# Create the data model for the database.
# WARNING: This step will delete all the tables and data previously contained in the database

datamodel.create_data_model(db_name, db_user, db_password, db_host, db_port)
