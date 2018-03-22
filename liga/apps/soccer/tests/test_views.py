import pytest
from django.test import RequestFactory
from .. import views
pytestmark = pytest.mark.django_db


class TestHome:
    def test_anonymous(self):
        """Everyone is welcome to visit the site."""
        req = RequestFactory().get('/')
        resp = views.HomeView.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'


class TestNextMatch:
    def test_anonymous(self):
        """Everyone will be able to see the next match page."""
        req = RequestFactory().get('/')
        resp = views.NextMatch.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'


class TestXCategory:
    def test_anonymous(self):
        """Everyone will be able to see the 'X' category page."""
        req = RequestFactory().get('/')
        resp = views.XCategory.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'


class TestFirstDivisionTeam:
    def test_anonymous(self):
        """Everyone will be able to see the first division team page."""
        req = RequestFactory().get('/')
        resp = views.FirstDivisionTeam.as_view()(req)
        assert resp.status_code == 200, 'Should be callable by anyone'
