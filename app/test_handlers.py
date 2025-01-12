import pytest
from app import app


@pytest.fixture()
def app_creation():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app_creation

    # clean up / reset resources here


@pytest.fixture()
def client(app_creation):
    return app.test_client()


@pytest.fixture()
def runner(app_creation):
    return app.test_cli_runner()


def test_registration(client):
    response = client.post("/user_registration", data={
        "login": "Flask",
        "password": "dark",
        "address": "required",
        "phone": "required"})
    assert response.get_json()["login"] == "Flask"


def test_conclude(client):
    client.post("/user_registration", data={
        "login": "Flask",
        "password": "dark",
        "address": "required",
        "phone": "required"})

    client.post("/", data={
        "size_5": "25",
        "quantity_5": 1
    })

    client.post("/", data={
        "size_7": "25",
        "quantity_7": 1
    })

    response = client.get("/conclude")

    assert response.get_json() == 618
