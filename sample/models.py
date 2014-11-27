from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, db_index=True, unique=True)
    name = models.TextField()
    USERNAME_FIELD = 'username'
    objects = BaseUserManager()


class Test(models.Model):
    testName = models.TextField()
    description = models.TextField()
    duration = models.IntegerField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()


class Question(models.Model):
    value = models.TextField()
    test = models.ForeignKey(Test)


class Options(models.Model):
    question = models.ForeignKey(Question)
    optionType = models.CharField(max_length=20)
    value = models.TextField()


class Answers(models.Model):
    question = models.ForeignKey(Question)
    option = models.ForeignKey(Options)


class TestSummary(models.Model):

    attemptedAt = models.DateTimeField()
    submittedAt = models.DateTimeField()
    test = models.ForeignKey(Test)
    submittedQuestions = models.IntegerField()
    correctlyAnswered = models.IntegerField()


class UserAnswers(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    option = models.ForeignKey(Options)
    test = models.ForeignKey(Test)
    isCorrect = models.BooleanField()


class Admin(models.Model):
    adminName = models.TextField()
    adminEmail = models.EmailField()
    adminPassword = models.TextField()


class Scores(models.Model):
    user = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    score = models.IntegerField()


class Store(models.Model):
    test = models.IntegerField()
    overall_percentage = models.TextField()
    cutoff_count = models.IntegerField()