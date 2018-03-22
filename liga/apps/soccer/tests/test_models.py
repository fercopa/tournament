import pytest
from mixer.backend.django import mixer
from .. import models
pytestmark = pytest.mark.django_db


class TestNews:
    def test_new_news(self):
        news = mixer.blend(models.News)
        assert news.pk == 1, 'Should save an instance'


class TestCategory:
    def test_new_category(self):
        category = mixer.blend(models.Category)
        assert category.pk == 1, 'Should save an instance'

    def test_get_teams(self):
        category = mixer.blend(models.Category)
        mixer.blend(models.Team, category=category)
        mixer.blend(models.Team, category=category)
        assert len(category.get_teams()) == 2, 'There must be 2 teams'


class TestTournament:
    def test_new_tournament(self):
        tournament = mixer.blend(models.Tournament)
        assert tournament.pk == 1, 'Should save an instance'


class TestZone:
    def test_new_zone(self):
        zone = mixer.blend(models.Zone)
        assert zone.pk == 1, 'Should save an instance'


class TestTeam:
    def test_new_team(self):
        team = mixer.blend(models.Team)
        assert team.pk == 1, 'Should save an instance'


class TestPlayer:
    def test_new_player(self):
        player = mixer.blend(models.Player)
        assert player.pk == 1, 'Should save an instance'


class TestSoccerField:
    def test_new_soccer_field(self):
        soccer_field = mixer.blend(models.SoccerField)
        assert soccer_field.pk == 1, 'Should save an instance'


class TestMatch:
    def test_new_match(self):
        match = mixer.blend(models.Match)
        assert match.pk == 1, 'Should save an instance'


class TestGoal:
    def test_new_goal(self):
        goal = mixer.blend(models.Goal)
        assert goal.pk == 1, 'Should save an instance'


class TestPoint:
    def test_new_point(self):
        point = mixer.blend(models.Point)
        assert point.pk == 1, 'Should save an instance'
