import pytest
from app import create_app
from app import db


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

from app.models.planet import Planet


@pytest.fixture
def two_planets(app):
    # Arrange
    planet_mars = Planet(title="Mars",
                      description="Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, being larger than only Mercury.")
    planet_saturn = Planet(title="Saturn",
                         description="Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter.")

    db.session.add_all([planet_saturn, planet_mars])
    # Alternatively, we could do
    # db.session.add(planet_mars)
    # db.session.add(planet_saturn)
    db.session.commit()