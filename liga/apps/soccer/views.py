from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from . import forms
from . import models


def prueba(request):
    form = forms.Prueba(request.POST or None)
    teams = models.Team.objects.all()
    if form.is_valid():
        print(form.cleaned_data['teams'])
    return render(request, 'prueba.html', {'form': form, 'teams': teams})


class HomeView(TemplateView):
    template_name = "home.html"


# New
class NewsList(ListView):
    model = models.News
    template_name = 'news_list.html'


class CreateNews(SuccessMessageMixin, CreateView):
    model = models.News
    fields = ['title', 'body', ]
    template_name = 'news_create.html'
    success_url = reverse_lazy('news-list')
    success_message = 'Se ha creado exitósamente'


class NewsDetail(DetailView):
    model = models.News
    template_name = 'news_detail.html'


class NewsDelete(DeleteView):
    model = models.News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news-list')


class NewsUpdate(UpdateView):
    model = models.News
    fields = ['title', 'body', ]
    template_name = 'news_update.html'
    success_url = reverse_lazy('news-list')


# Category
class CategoryList(ListView):
    model = models.Category
    template_name = 'category_list.html'


class CategoryCreate(SuccessMessageMixin, CreateView):
    form_class = forms.CategoryForm
    template_name = 'category_create.html'
    success_url = reverse_lazy('category-list')
    success_message = 'Se ha creado exitósamente'


class CategoryDetail(DetailView):
    model = models.Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        obj = context['object']
        context['tournaments'] = models.Tournament.objects.filter(category=obj)
        return context


class CategoryDelete(DeleteView):
    model = models.Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


def category_update(request, pk=None):
    obj = get_object_or_404(models.Category, pk=pk)
    form = forms.CategoryUpdateForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('category-list'))
    ctx = {'form': form}
    return render(request, 'category_update.html', ctx)


# Tournament
def tournament_create(request, category):
    form = forms.TournamentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('category-detail',
                                     kwargs={'pk': category}))
    else:
        print(form)
    ctx = {'form': form}
    return render(request, 'tournament_create.html', ctx)


class TournamentDetail(DetailView):
    model = models.Tournament
    template_name = 'tournament_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TournamentDetail, self).get_context_data(**kwargs)
        obj = context['object']
        context['zones'] = models.Zone.objects.filter(tournament=obj)
        return context


def tournament_delete(request, category, pk):
    tournament = get_object_or_404(models.Tournament, pk=pk)
    if request.POST:
        tournament.delete()
        return redirect(reverse_lazy('category-detail', args=[category, ]))
    return render(request, 'object_confirm_delete.html',
                  {'object': tournament})


def tournament_update(request, category, pk):
    tournament = get_object_or_404(models.Tournament, pk=pk)
    form = forms.TournamentForm(request.POST or None, instance=tournament)
    if form.is_valid():
        form.save()
        return redirect(reverse_lazy('category-detail',
                                     kwargs={'pk': category}))
    categ = get_object_or_404(models.Category, pk=category)
    ctx = {'form': form, 'tournament': tournament}
    return render(request, 'tournament_update.html', ctx)


# Zone
def zone_create(request, category, torneo):
    trnmnt = get_object_or_404(models.Tournament, id=torneo)
    form = forms.AddTeamsToZoneForm(trnmnt, request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        teams = form.cleaned_data['teams']
        zone = models.Zone.objects.create(tournament=trnmnt, name=name)
        for k in teams:
            try:
                team = models.Team.objects.get(pk=k)
                team.zone = zone
                team.save()
                return redirect(trnmnt.get_absolute_url)
            except models.Team.DoesNotExist:
                zone.delete()
                form = forms.AddTeamsToZoneForm(trnmnt, request.POST or None)
    ctxt = {'form': form, 'tournament': trnmnt}
    return render(request, 'add_teams_to_zone.html', ctxt)


def zone_fixture_create(request, category, torneo, pk):
    z = get_object_or_404(models.Zone, pk=pk)
    z.create_fixture()
    return redirect(z)


def zone_fixture(request, category, torneo, pk):
    z = get_object_or_404(models.Zone, pk=pk)
    ctx = {'matchs': models.Match.objects.filter(zone=z), 'zone': z}
    return render(request, 'zone_fixture.html', ctx)


class ZoneDetail(DetailView):
    model = models.Zone
    template_name = 'zone_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ZoneDetail, self).get_context_data(**kwargs)
        obj = context['object']
        context['teams'] = models.Team.objects.filter(zone=obj)
        return context


class ZoneDelete(DeleteView):
    model = models.Zone
    template_name = 'zone_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Team
class TeamList(ListView):
    model = models.Team
    template_name = 'team_list.html'


class TeamCreate(SuccessMessageMixin, CreateView):
    model = models.Team
    fields = ['category', 'zone', 'name', ]
    template_name = 'team_create.html'
    success_url = reverse_lazy('team-list')
    success_message = 'Se ha creado exitósamente'


class TeamUpdate(UpdateView):
    model = models.Team
    fields = ['category', 'zone', 'name', ]
    template_name = 'team_update.html'
    success_url = reverse_lazy('team-list')


class TeamDetail(DetailView):
    model = models.Team
    template_name = 'team_detail.html'


class TeamDelete(DeleteView):
    model = models.Team
    template_name = 'team_confirm_delete.html'
    success_url = reverse_lazy('team-list')


# Player
class PlayerList(ListView):
    model = models.Player
    template_name = 'player_list.html'


class PlayerCreate(SuccessMessageMixin, CreateView):
    model = models.Player
    fields = ['team', 'last_name', 'name', 'dni', 'carnet', 'photo', ]
    template_name = 'player_create.html'
    success_url = reverse_lazy('player-list')
    success_message = 'Se ha creado exitósamente'


class PlayerUpdate(UpdateView):
    model = models.Player
    fields = ['team', 'name', 'dni', 'carnet', 'photo', ]
    template_name = 'object_update.html'
    success_url = reverse_lazy('player-list')

    def get_context_data(self, **kwargs):
        context = super(PlayerUpdate, self).get_context_data(**kwargs)
        obj = {'title': 'Jugador',
               'cancel_url': 'player-list'}
        context['element'] = obj
        return context


class PlayerDetail(DetailView):
    model = models.Player
    template_name = 'player_detail.html'


class PlayerDelete(DeleteView):
    model = models.Player
    template_name = 'object_confirm_delete.html'
    success_url = reverse_lazy('player-list')

    def get_context_data(self, **kwargs):
        context = super(PlayerDelete, self).get_context_data(**kwargs)
        obj = {'title': 'Eliminar Jugador',
               'cancel_url': 'player-list'}
        context['element'] = obj
        return context


# Soccer field
class SoccerFieldList(ListView):
    model = models.SoccerField
    template_name = 'object_list.html'

    def get_context_data(self, **kwargs):
        context = super(SoccerFieldList, self).get_context_data(**kwargs)
        obj = {'title': 'Canchas',
               'text_create': 'Nueva Cancha',
               'create_url': reverse_lazy('soccerField-create'),
               'edit': 'soccerField-update',
               'delete': 'soccerField-delete',
               }
        context['element'] = obj
        return context


class SoccerFieldCreate(SuccessMessageMixin, CreateView):
    model = models.SoccerField
    fields = ['name', 'address', 'codeplus', ]
    template_name = 'object_create.html'
    success_url = reverse_lazy('soccerField-list')
    success_message = 'Se ha creado exitósamente'

    def get_context_data(self, **kwargs):
        context = super(SoccerFieldCreate, self).get_context_data(**kwargs)
        obj = {'title': 'Nueva Cancha',
               'cancel_url': 'soccerField-list'}
        context['element'] = obj
        return context


class SoccerFieldUpdate(UpdateView):
    model = models.SoccerField
    fields = ['name', 'address', 'codeplus', ]
    template_name = 'object_update.html'
    success_url = reverse_lazy('soccerField-list')

    def get_context_data(self, **kwargs):
        context = super(SoccerFieldUpdate, self).get_context_data(**kwargs)
        obj = {'title': 'Cancha',
               'cancel_url': 'soccerField-list'}
        context['element'] = obj
        return context


class SoccerFieldDetail(DetailView):
    model = models.SoccerField
    template_name = 'soccerField_detail.html'


class SoccerFieldDelete(DeleteView):
    model = models.SoccerField
    template_name = 'object_confirm_delete.html'
    success_url = reverse_lazy('soccerField-list')

    def get_context_data(self, **kwargs):
        context = super(SoccerFieldDelete, self).get_context_data(**kwargs)
        obj = {'title': 'Eliminar Cancha',
               'cancel_url': 'soccerField-list'}
        context['element'] = obj
        return context


# Match
class MatchList(ListView):
    model = models.Match
    template_name = 'object_list.html'

    def get_context_data(self, **kwargs):
        context = super(MatchList, self).get_context_data(**kwargs)
        obj = {'title': 'Partidos',
               'text_create': 'Nuevo Partido',
               'create_url': reverse_lazy('match-create'),
               'edit': 'match-update',
               'delete': 'match-delete',
               }
        context['element'] = obj
        return context


class MatchCreate(SuccessMessageMixin, CreateView):
    model = models.Match
    fields = ['zone', 'soccerfield', 'local', 'visitor', 'date', ]
    template_name = 'object_create.html'
    success_url = reverse_lazy('match-list')
    success_message = 'Se ha creado exitósamente'

    def get_context_data(self, **kwargs):
        context = super(MatchCreate, self).get_context_data(**kwargs)
        obj = {'title': 'Nuevo Partido',
               'cancel_url': 'match-list'}
        context['element'] = obj
        return context


def match_update(request, category, torneo, zone, pk):
    match = get_object_or_404(models.Match, pk=pk)
    zone = get_object_or_404(models.Zone, pk=zone)
    form = forms.MatchUpdateForm(request.POST or None, instance=match)
    if form.is_valid():
        form.save()
        return redirect(zone.get_absolute_url() + "fixture/")

    return render(request, 'match_update.html', {'form': form, 'zone': zone})


class MatchDetail(DetailView):
    model = models.Match
    template_name = 'match_detail.html'


class MatchDelete(DeleteView):
    model = models.Match
    template_name = 'object_confirm_delete.html'
    success_url = reverse_lazy('match-list')

    def get_context_data(self, **kwargs):
        context = super(MatchDelete, self).get_context_data(**kwargs)
        obj = {'title': 'Eliminar Partido',
               'cancel_url': 'match-list'}
        context['element'] = obj
        return context


def add_teams_to_zone(request, div, torneo, zone):
    zone_obj = get_object_or_404(models.Zone, id=zone)
    form = forms.AddTeamsToZoneForm(zone_obj, request.POST or None)
    if form.is_valid():
        print(form.cleaned_data['teams'])
    ctx = {'form': form}
    return render(request, 'add_teams_to_zone.html', ctx)
