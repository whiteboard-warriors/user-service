import pytest
import dotenv
import os
from users.app import create_app

@pytest.fixture
def app():

    application = create_app()
    application.app_context().push()
    application.db.create_all()

    return application
