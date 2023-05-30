import pytest
from src.flask_application.app import create_app

@pytest.fixture()
def app():  # sourcery skip: inline-immediately-yielded-variable
    app = create_app('testing')
    # other setup can go here
    yield app
    # clean up / reset resources here

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client
        