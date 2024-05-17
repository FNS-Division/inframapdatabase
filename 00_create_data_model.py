# Import the module containing functions for creating the database schema

import datamodel

# Load database credentials
# If you wish to you use your local database, run the following line instead:
    # from credentials.local_db_credentials import db_name, db_user, db_password, db_host, db_port

from credentials.aws_db_credentials import db_name, db_user, db_password, db_host, db_port

# Create the data model for the database.

datamodel.create_data_model(db_name, db_user, db_password, db_host, db_port)