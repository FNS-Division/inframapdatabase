# Import packages
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

# Load database credentials
# If you wish to you use your local database, run the following line instead:
    # from credentials.local_db_credentials import db_name, db_user, db_password, db_host, db_port

from credentials.aws_db_credentials import db_name, db_user, db_password, db_host, db_port

# Read in POI data from data folder
poi_data_filepath = os.path.join(os.getcwd(), "data", "ESP", "processed", "pointofinterest", "ESP-1697915895-xs2u-pointofinterest.csv")
poi_data = pd.read_csv(poi_data_filepath)

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
try:
    poi_data.to_sql("point_of_interest", engine, index=False, if_exists='append')
    print("Data added to the database.")
except Exception as e:
    print("Error:", e)

# Commit the changes
session.commit()