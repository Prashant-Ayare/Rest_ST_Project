from django.db import models

class Student(models.Model):
    name=models.CharField(max_length=100)
    standard=models.PositiveIntegerField()
    email=models.EmailField(unique=True)
    roll_no=models.IntegerField()
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name



