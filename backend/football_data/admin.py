from django.contrib import admin

# Register your models here.
from .models import Country, League, Team

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'flag')
    search_fields = ('name', 'code')

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'league', 'country')
    search_fields = ('name',)
    list_filter = ('league', 'country')
