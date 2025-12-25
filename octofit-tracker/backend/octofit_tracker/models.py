from djongo import models
from django.contrib.auth.models import AbstractUser

# User model
class User(AbstractUser):
    # Additional fields can be added here
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='octofit_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='octofit_users_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Team model
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Activity model
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories_burned = models.FloatField()
    date = models.DateField()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

# Workout model
class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    duration = models.IntegerField()  # in minutes
    suggested_for = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Leaderboard model (for aggregation, not a real table)
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_calories = models.FloatField()
    total_duration = models.IntegerField()
    rank = models.IntegerField()

    class Meta:
        managed = False  # Not a real table
        verbose_name = 'Leaderboard Entry'
        verbose_name_plural = 'Leaderboard Entries'
