import pytest
import dotenv
import os
from users.app import create_app
# from users.db import db


# dotenv.load_dotenv()
# db_params = {
#     'host': os.environ['POSTGRES_HOST_TEST'],
#     'database': os.environ['POSTGRES_DB_TEST'],
#     'user': os.environ['POSTGRES_USER_TEST'],
#     'pwd': os.environ['POSTGRES_PASSWORD_TEST'],
#     'port': os.environ['POSTGRES_PORT_TEST'],
# }

# DB_URI = 'postgresql://{user}@{host}:{port}/{database}'


@pytest.fixture
def app():

    application = create_app()
    application.app_context().push()
    application.db.create_all()

    return application
