#!/usr/bin/env Python
# coding=utf-8
from __future__ import unicode_literals

from django.db import models
# Create your models here.

# 菜谱     创建时间 名字 作者 图片 简介 小贴士 标签
class Recipe(models.Model):
	create_time = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=200)
	user = models.CharField(max_length=40, blank=True)
	exihibitpic = models.ImageField(upload_to='exhibited_picture/%Y/%m/%d', blank=False)
	introduce = models.TextField(blank=False)
	tips = models.TextField(blank=True)
	tag = models.ManyToManyField('Tag')
	def __unicode__(self):
		return self.name

# 用料    菜谱 名字 用量 详情
class Material(models.Model):
	recipe = models.ForeignKey('Recipe')
	name = models.CharField(max_length=200)
	quantity = models.IntegerField()
	measureunits = models.CharField(max_length=20)
	def __unicode__(self):
		return '%s %s' % (self.recipe.name, self.name)

# 做法步骤    菜谱 排序 详情 图片 创建时间
class Procedure(models.Model):
	recipe = models.ForeignKey('Recipe')
	seq = models.IntegerField()
	describe = models.TextField(blank=False)
	image = models.ImageField(upload_to='exhibited_picture/%Y/%m/%d', blank=False)
	create_time = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.recipe.name
# 标签    名字 分类( 年龄 营养 烹饪 等)
class Tag(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey('Category')
	def __unicode__(self):
		return self.name
# 分类    名字 is_tag 来区分类别 
class Category(models.Model):
	name = models.CharField(max_length=100)
	is_tag =models.IntegerField(blank=False)
	def __unicode__(self):
		return self.name
# 推荐 创建时间 菜谱 图片 时间
class Recommend(models.Model):
	create_time = models.DateTimeField(auto_now=True)
	recipe = models.ForeignKey('Recipe')
	image = models.ImageField(upload_to='exhibited_picture/%Y/%m/%d', blank=False)
	pubdate = models.DateTimeField()
	def __unicode__(self):
		return self.recipe.name
