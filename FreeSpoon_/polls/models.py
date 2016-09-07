from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):

        name = models.CharField(max_length = 200)
        age = models.CharField(max_length = 11)
        sax = models.CharField(max_length =11)


class Classes(models.Model):

        student =models.ManyToManyField('Student')
        classname = models.CharField(max_length = 10)

