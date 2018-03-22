from django.contrib import admin
from .models import (Category, Tournament, Zone, Team, Player, SoccerField,
                     Match, Goal, Point)


admin.site.register(Category)
admin.site.register(Tournament)
admin.site.register(Zone)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(SoccerField)
admin.site.register(Match)
admin.site.register(Goal)
admin.site.register(Point)
