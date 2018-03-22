from string import ascii_lowercase
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from . import models
from .forms_widgets import SelectOptionsWithAttrs

CATEGORIES = (('a', 'A'),
              ('b', 'B'),
              ('c', 'C'),
              ('d', 'D'))

ZONES = tuple([(x, x.upper()) for x in ascii_lowercase])


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        choices = [(k, v) for k, v in CATEGORIES
                   if not models.Category.objects.filter(name=k)]
        self.fields['name'] = forms.ChoiceField(choices=choices,
                                                label='División')

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        name = cleaned_data.get('name')
        if models.Category.objects.filter(name=name):
            self.add_error(None, ValidationError('La categoria ya existe.'))


class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ChoiceField(choices=CATEGORIES,
                                                label='División')

    def clean(self):
        cleaned_data = super(CategoryUpdateForm, self).clean()
        new_name = cleaned_data.get('name')
        category = models.Category.objects.filter(name=new_name)
        if category.exists() and category[0].name != self.instance.name:
            self.add_error(None, ValidationError('La categoria ya existe.'))


class TournamentForm(forms.ModelForm):
    class Meta:
        model = models.Tournament
        fields = ['category', 'datefield', ]
        labels = {'category': _('Categoría'), 'datefield': _('Fecha'), }
        # widgets = {'datefield': forms.SelectDateWidget()}


class AddTeamsToZoneForm(forms.Form):
    name = forms.ChoiceField()
    teams = forms.MultipleChoiceField()

    def __init__(self, tournament, *args, **kwargs):
        super(AddTeamsToZoneForm, self).__init__(*args, **kwargs)
        t = models.Team.objects.filter(category=tournament.category)
        ch_z = [(k, v) for k, v in ZONES
                if not models.Zone.objects.filter(name=k)]
        self.fields['name'] = forms.ChoiceField(choices=ch_z, label='Zona')
        ch = [(team.pk, team.name) for team in t if not team.zone]
        self.fields['teams'] = forms.MultipleChoiceField(
            widget=forms.SelectMultiple(attrs={'id': 'my-select'}), choices=ch,
            label='Equipos')


class MatchUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Match
        fields = ['zone', 'soccerfield', 'local', 'visitor', 'date', ]
        labels = {'zone': _('Zona'), 'soccerfield': _('Cancha'),
                  'local': _('Local'), 'visitor': _('Visitante'),
                  'date': _('Fecha')}


class Prueba(forms.Form):
    teams = forms.MultipleChoiceField(widget=SelectOptionsWithAttrs())
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(Prueba, self).__init__(*args, **kwargs)

        choices = (
                    (1, 'Opcion 1'), (2, 'Opcion 2')
        )
        self.fields['teams'].choices = choices
