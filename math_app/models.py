from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class User(AbstractUser):
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

class Exercise(models.Model):
    TYPES = [
        ('addition', 'Suma'),
        ('subtraction', 'Resta'),
        ('multiplication', 'Multiplicación'),
        ('division', 'División'),
        ('exponentiation', 'Potenciación'),
        ('root', 'Raíz cuadrada'),
        ('logarithm', 'Logaritmo'),
        ('trigonometry', 'Trigonometría'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, choices=TYPES)
    difficulty = models.IntegerField()
    question = models.CharField(max_length=255)
    correct_answer = models.FloatField()
    user_answer = models.FloatField(null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    explanation = models.TextField(blank=True)  # New field for step-by-step explanation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - Difficulty: {self.difficulty}"

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    level_required = models.IntegerField(default=0)  # Nuevo campo

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    related_exercise_type = models.CharField(max_length=50, choices=Exercise.TYPES)