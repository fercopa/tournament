from django.conf.urls import url
from . import views


urlpatterns = [
    # Test
    url(r'^prueba/', views.prueba),
    # News
    url(r'^noticia/lista/$',
        views.NewsList.as_view(), name='news-list'),
    url(r'^noticia/nueva/$', views.CreateNews.as_view(),
        name='news-create'),
    url(r'^noticia-(?P<pk>\d+)/detalle/$', views.NewsDetail.as_view(),
        name='news-detail'),
    url(r'^noticia-(?P<pk>\d+)/actualizar/$',
        views.NewsUpdate.as_view(), name='news-update'),
    url(r'^noticia-(?P<pk>\d+)/eliminar/$',
        views.NewsDelete.as_view(), name='news-delete'),

    # Category
    url(r'^categoria/lista/$', views.CategoryList.as_view(),
        name='category-list'),
    url(r'^categoria/nueva/$', views.CategoryCreate.as_view(),
        name='category-create'),
    url(r'^categoria-(?P<pk>\d+)/$', views.CategoryDetail.as_view(),
        name='category-detail'),
    url(r'^categoria-(?P<pk>\d+)/actualizar/$',
        views.category_update, name='category-update'),
    url(r'^categoria-(?P<pk>\d+)/eliminar/$',
        views.CategoryDelete.as_view(), name='category-delete'),

    # Tournament
    url(r'^categoria-(?P<category>\d+)/torneo/nuevo/$',
        views.tournament_create, name='tournament-create'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<pk>\d+)/$',
        views.TournamentDetail.as_view(), name='tournament-detail'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<pk>\d+)/actualizar/$',
        views.tournament_update, name='tournament-update'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<pk>\d+)/eliminar/$',
        views.tournament_delete, name='tournament-delete'),

    # Zone
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/zona/nueva/$',
        views.zone_create, name='zone-create'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/'
        'zona-(?P<pk>\d+)/$',
        views.ZoneDetail.as_view(), name='zone-detail'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/'
        'zona-(?P<pk>\d+)/fixture/$',
        views.zone_fixture, name='zone-fixture'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/'
        'zona-(?P<pk>\d+)/fixture/nuevo/$',
        views.zone_fixture_create, name='zone-fixture-create'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/'
        'zona-(?P<pk>\d+)/borrar/$',
        views.ZoneDelete.as_view(), name='zone-delete'),

    # Team
    url(r'^equipos/$',
        views.TeamList.as_view(), name='team-list'),
    url(r'^equipo/nuevo/$', views.TeamCreate.as_view(),
        name='team-create'),
    url(r'^equipo-(?P<pk>\d+)/$', views.TeamDetail.as_view(),
        name='team-detail'),
    url(r'^equipo-(?P<pk>\d+)/actualizar/$',
        views.TeamUpdate.as_view(), name='team-update'),
    url(r'^equipo-(?P<pk>\d+)/borrar/$',
        views.TeamDelete.as_view(), name='team-delete'),

    # Player
    url(r'^jugadores/$',
        views.PlayerList.as_view(), name='player-list'),
    url(r'^jugador/nuevo/$', views.PlayerCreate.as_view(),
        name='player-create'),
    url(r'^jugador-(?P<pk>\d+)/$', views.PlayerDetail.as_view(),
        name='player-detail'),
    url(r'^jugador-(?P<pk>\d+)/actualizar/$',
        views.PlayerUpdate.as_view(), name='player-update'),
    url(r'^jugador-(?P<pk>\d+)/borrar/$',
        views.PlayerDelete.as_view(), name='player-delete'),

    # Soccer Field
    url(r'^soccer-field/list/$',
        views.SoccerFieldList.as_view(), name='soccerField-list'),
    url(r'^soccer-field/create/$', views.SoccerFieldCreate.as_view(),
        name='soccerField-create'),
    url(r'^soccer-field/detail/(?P<pk>\d+)/$',
        views.SoccerFieldDetail.as_view(),
        name='soccerField-detail'),
    url(r'^soccer-field/detail/(?P<pk>\d+)/update/$',
        views.SoccerFieldUpdate.as_view(), name='soccerField-update'),
    url(r'^soccer-field/detail/(?P<pk>\d+)/delete/$',
        views.SoccerFieldDelete.as_view(), name='soccerField-delete'),

    # Match
    url(r'^match/list/$',
        views.MatchList.as_view(), name='match-list'),
    url(r'^match/create/$', views.MatchCreate.as_view(),
        name='match-create'),
    url(r'^match/detail/(?P<pk>\d+)/$',
        views.MatchDetail.as_view(),
        name='match-detail'),
    url(r'^categoria-(?P<category>\d+)/torneo-(?P<torneo>\d+)/'
        'zona-(?P<zone>\d+)/partido-(?P<pk>\d+)/actualizar/$',
        views.match_update, name='match-update'),
    url(r'^match/detail/(?P<pk>\d+)/delete/$',
        views.MatchDelete.as_view(), name='match-delete'),
]
