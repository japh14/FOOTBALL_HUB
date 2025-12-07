from django.contrib import admin

# Register your models here.
from .models import Country, League, Team, Player

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'flag')
    search_fields = ('name', 'code')

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name','type','country__name')
    list_filter = ('country',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league')
    search_fields = ('name','country__name','league__name')
    list_filter = ('league', 'country')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'league')
    search_fields = ('name','team__name','league__name')
    list_filter = ('league', 'team')