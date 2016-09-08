from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Student(models.Model):
	name = models.CharField(max_length = 200)
	age = models.CharField(max_length=11)
	sex = models.CharField(max_length=11)

class Classes(models.Model):
	student = models.ManyToManyField('Student')
	classname = models.CharField(max_length=10)


class Recipe(models.Model):
	name = models.CharField(max_length=200)
	user = models.CharField(max_length=40, blank=True)
	exihibitpic = models.ImageField(upload_to='images/exhibited_picture/%Y/%m/%d', blank=False)
	introduce = models.TextField(blank=False)
	tag = models.ManyToManyField('Tag')
	def __unicode__(self):
		return self.name

class Material(models.Model):
	recipe = models.ForeignKey('Recipe')
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	measureunits = models.CharField(max_length=20)
	def __unicode__(self):
		return '%s %s' % (self.recipe.name, self.name)

class Procedure(models.Model):
	recipe = models.ForeignKey('Recipe')
	seq = models.IntegerField()
	describe = models.TextField(blank=False)
	image = models.ImageField(upload_to='images/procedure_picture/%Y/%m/%d', blank=True)
	def __unicode__(self):
		return '%s %s' % (self.recipe.name, self.seq)

class Tag(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey('Category')
	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.name

