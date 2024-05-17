# Import packages
import pandas as pd
from sqlalchemy import create_engine, inspect

# Load database credentials
# If you wish to you use your local database, run the following line instead:
    # from credentials.local_db_credentials import db_name, db_user, db_password, db_host, db_port

from credentials.aws_db_credentials import db_name, db_user, db_password, db_host, db_port

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