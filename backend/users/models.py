from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.


# ------------------------
# User Profile Model
# ------------------------

class UserProfileManager(BaseUserManager):
    """"
    Custom manager for UserProfile to handle user creation.
     By extending AbstractUser:
    - You get username, password, permissions, groups, etc.
    - You can remove username if you want email-only login.
    - You can add your own custom fields.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class UserProfile(AbstractUser):
    """
    Custom user model that uses email as the unique identifier
    instead of username.
    """
    username = None  # Remove username field
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text="User's email address"
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        help_text="User's first name"
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        help_text="User's last name"
    )

    # Custom fields can be added here:
    favorite_teams = models.ManyToManyField(
        to='football_data.Team',
        related_name='fav_team',
        blank=True,
        help_text="User's favorite teams"        

    )

    favorite_players = models.ManyToManyField(
        to='football_data.Player',
        related_name='fav_player',
        blank=True,
        help_text="User's favorite players"        
    )

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = []  # Email & Password are required by default

    objects = UserProfileManager()

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['email']

    def __str__(self):
        return self.email