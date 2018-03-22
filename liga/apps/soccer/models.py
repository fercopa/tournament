from django.db import models
from django.urls import reverse_lazy


class News(models.Model):
    title = models.CharField(max_length=50, verbose_name='Título')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    body = models.TextField(verbose_name='Texto')

    class Meta:
        verbose_name = 'Noticia'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('news-detail', args=[str(self.pk)])


class Category(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Categoria'

    def __str__(self):
        return "Categoria %s" % self.name.upper()

    def get_absolute_url(self):
        return reverse_lazy('category-detail', args=[str(self.pk)])


class Tournament(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    datefield = models.DateField()

    class Meta:
        verbose_name = 'Torneo'

    def __str__(self):
        category = self.category.name.upper()
        return "Categoría %s " % category + self.datefield.isoformat()

    def get_absolute_url(self):
        args = {'category': str(self.category.id), 'pk': str(self.pk)}
        return reverse_lazy('tournament-detail', kwargs=args)


class Zone(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Zona'

    def __str__(self):
        return "Zona %s" % self.name

    def get_absolute_url(self):
        args = {'category': str(self.tournament.category.pk),
                'torneo': str(self.tournament.pk),
                'pk': str(self.pk)}
        return reverse_lazy('zone-detail', kwargs=args)

    def create_fixture(self):
        """
        Create the matchs for this zone.
        """
        for match in Match.objects.filter(zone=self):
            match.delete()
        teams = Team.objects.filter(zone=self)
        n = len(teams)
        mid = n//2
        aux1 = teams[:mid]
        aux2 = teams[mid:]
        for i in range(len(aux1)):
            Match.objects.create(zone=self, local=aux1[i], visitor=aux2[i])
        for i in range(n-2):
            last = aux1.pop()
            first = aux2.pop(0)
            aux1.insert(1, first)
            aux2.append(last)
            for j in range(len(aux1)):
                Match.objects.create(zone=self, local=aux1[j], visitor=aux2[j])


class Team(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Categoría')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,
                             verbose_name='Zona', blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Equipo'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('team-detail', args=[str(self.pk)])


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                             verbose_name='Equipo')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    name = models.CharField(max_length=50, verbose_name='Nombres')
    dni = models.IntegerField(verbose_name='DNI')
    carnet = models.IntegerField()
    photo = models.ImageField(blank=True, null=True, verbose_name='Foto')

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('player-detail', args=[str(self.pk)])


class SoccerField(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    codeplus = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Cancha'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('soccerField-detail', args=[str(self.pk)])

    def get_url_map(self):
        return 'https://plus.codes/' + self.codeplus


class Match(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    soccerfield = models.ForeignKey(SoccerField, on_delete=models.CASCADE,
                                    null=True, blank=True)
    local = models.ForeignKey(Team, related_name='local_team',
                              on_delete=models.CASCADE)
    visitor = models.ForeignKey(Team, related_name='visitor_team',
                                on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Partido'

    def __str__(self):
        return "%s vs %s" % (self.local.name, self.visitor.name)

    def get_absolute_url(self):
        category = str(self.zone.tournament.category.pk)
        tournament = str(self.zone.tournament.pk)
        zone = str(self.zone.pk)
        kwargs = {'category': category,
                  'torneo': tournament,
                  'zone': zone,
                  'pk': str(self.pk)}
        return reverse_lazy('match-update', kwargs=kwargs)


class Goal(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Gol'
        verbose_name_plural = 'Goles'

    def __str__(self):
        return "Goool"

    def get_absolute_url(self):
        return reverse_lazy('goal-detail', args=[str(self.pk)])


class Point(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Punto'

    def __str__(self):
        return "1 pts of %s" % self.team.name

    def get_absolute_url(self):
        return reverse_lazy('point-detail', args=[str(self.pk)])
