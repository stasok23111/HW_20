import pytest
from unittest.mock import MagicMock
from service.director import DirectorService
from dao.director import DirectorDAO
from dao.model.director import Director
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    dir_1 = Director(id=1, name='Kate')
    dir_2 = Director(id=2, name='Aragorn')
    dir_3 = Director(id=3, name='Frodo')

    director_dao.get_one = MagicMock(return_value=dir_1)
    director_dao.get_all = MagicMock(return_value=[dir_1, dir_2, dir_3])
    director_dao.create = MagicMock(return_value=Director(id=4))
    director_dao.update = MagicMock()
    director_dao.delete = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_director_service(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        director_d = {
            'id': 1,
            'name': 'Ruk'
        }
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_delete(self):
        director =  self.director_service.delete(1)
        assert director is None

    def test_update(self):
        director_d = {
            'id': 3,
            'name': 'Kira'
        }

        self.director_service.update(director_d)

