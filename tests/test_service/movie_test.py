from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db

@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    movie_1 = Movie(id=1,
                    title='misfits',
                    description='description Coup',
                    trailer='trailer',
                    year=2003,
                    rating=10,
                    genre_id=1,
                    director_id=2,)
    movie_2 = Movie(id=2,
                    title='Run *****, Run',
                    description='description RUUUUUUUNNNNNN',
                    trailer='trailer Fake',
                    year=2003,
                    rating=2,
                    director_id=1,
                    )

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_2, movie_2])
    movie_dao.create = MagicMock(return_value=Movie(id=3, title="Kill Bill"))
    movie_dao.update = MagicMock()
    movie_dao.delete = MagicMock()
    return movie_dao




class TestMovieService:

    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_movie_service(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movie = self.movie_service.get_all()

        assert len(movie) > 0

    def test_create(self):
        movie_d = {
            "id": 1,
            "title": "Kill Bill",
            "description": "Killing Butterflies",
            "trailer": "No",
            "year": 2020,
            "rating": 10,
            "genre_id": 1,
            "director_id": 1,
        }
        movie = self.movie_service.create(movie_d)
        assert movie.title == movie_d['title']

    def test_delete(self):
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_d = {
            "id": 3,
            "title": "Kill Bill",
            "description": "Killing Butterflies",
            "trailer": "No",
            "year": 2020,
            "rating": 10,
            "genre_id": 2,
            "director_id": 1,
        }
        self.movie_service.update(movie_d)
