from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# ------------------------
# Country Model
# ------------------------
class Country(models.Model):
    code = models.CharField(
        primary_key=True,
        max_length=10,
        help_text="ISO code or API-provided unique country code"
    )
    name = models.CharField(
        max_length=100,
        help_text="Country name"
    )
    flag = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the country flag"
    )

    class Meta:
        db_table = 'country'
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


# ------------------------
# League Model
# ------------------------
class League(models.Model):
    id = models.IntegerField(
        primary_key=True,
        help_text="Unique league ID from API"
    )
    name = models.CharField(
        max_length=100,
        help_text="League name"
    )
    type = models.CharField(
        max_length=50,
        help_text="Type of league (e.g., League or Cup)"
    )
    logo = models.URLField(
        blank=True,
        null=True,
        help_text="URL to league logo"
    )

    # Foreign key to Country
    country = models.ForeignKey(
        to=Country,               # direct reference, works even with custom PK
        to_field='code',       # link to Country.code instead of id
        db_column='country_code',
        on_delete=models.CASCADE,
        related_name='leagues',
        help_text="Country that the league belongs to"
    )

    class Meta:
        db_table = 'league'
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'
        ordering = ['name']

    def __str__(self):
        # safer string representation in case country is None
        country_name = self.country.name if self.country else 'N/A'
        return f"{self.name} ({country_name})"

# ------------------------
# Team Model
# ------------------------
class Team(models.Model):
    id = models.IntegerField(        
        primary_key=True,
        help_text="Unique team ID from API"
    )  

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the team"
        )
    code = models.CharField(
        max_length=10,
        # unique=True,
        blank=True,
        null=True,
        help_text="Team code (if available)"
        )

    # Foreign keys
    country = models.ForeignKey(
        to='football_data.Country',
        to_field='code',              # Links to Country.code
        db_column='country_code',
        on_delete=models.CASCADE,
        related_name='teams'
    )

    league = models.ForeignKey(
        to='football_data.League',
        to_field='id',                # Links to League.id (custom PK)
        db_column='league_id',
        on_delete=models.CASCADE,
        related_name='teams'
    )

    founded = models.IntegerField(blank=True, null=True)
    national = models.BooleanField(default=False)

    logo = models.URLField(blank=True, null=True)

    # Venue details
    venue_id = models.IntegerField(unique=True, null=True, blank=True)
    venue_name = models.CharField(max_length=100)
    venue_city = models.CharField(max_length=100, blank=True, null=True)
    venue_capacity = models.IntegerField(blank=True, null=True)
    venue_surface = models.CharField(max_length=50, blank=True, null=True)
    venue_address = models.CharField(max_length=255, blank=True, null=True)
    venue_image = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'team'
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (L: {self.league.name}, C: {self.country.code})"


# ------------------------
# Player Model
# ------------------------

class Player(models.Model):
    id = models.IntegerField(
        primary_key=True,
        help_text="Unique player ID from API"
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Name of player from API"
    )

    firstname = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="First name of player from API"
    )

    lastname = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Last name of player from API"
    )

    age = models.IntegerField(
        help_text="Age of player from API",
        null=True,
        blank=True
    )

    nationality = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Player nationaility from API. (Not the same as country ID)"
    )

    birth_place = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Player birth_place from API. (Not the same as country ID)"
    )

    birth_country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Player birth_country from API. (Not the same as country ID)"
    )

    height = models.FloatField(
        help_text="Player height in centimeters",
        null=True,
        blank=True
    )
    weight = models.FloatField(
        help_text="Player weight in kilograms",
        null=True,
        blank=True
    )

    birth_date = models.DateField(
        help_text="Player birth date",
        null=True,
        blank=True
    )

    photo = models.URLField(
        help_text="URL to player's photo",
        null=True,
        blank=True
    )

    postion = models.CharField(
        max_length=50,
        help_text="Player position",
        null=True,
        blank=True
    )

    injured = models.BooleanField(
        help_text="Is the player injured?",
        default=False
    )

    # Foreign key to Team
    team = models.ForeignKey(
        to='football_data.Team',
        to_field='id',
        db_column='team_id',
        on_delete=models.CASCADE,
        related_name='players',
        help_text="Team that the player belongs to"
    )

    # Foreign key to League
    league = models.ForeignKey(
        to='football_data.League',
        to_field='id',
        db_column='league_id',
        on_delete=models.CASCADE,
        related_name='players'

    )

    class Meta:
        db_table = 'player'
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Team: {self.team.name}, League: {self.league.name})"
    
    def __repr__(self):
        return super().__repr__()

