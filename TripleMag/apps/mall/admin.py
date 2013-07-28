# -*- coding:utf8 -*-

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django import forms
from django.forms import ModelForm

from TripleMag.apps.mall.models import *


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category,CategoryAdmin)

class CategoryFirstAdmin(admin.ModelAdmin):
    pass

admin.site.register(CategoryFirst, CategoryFirstAdmin)

class CategorySecondAdmin(admin.ModelAdmin):
    pass

admin.site.register(CategorySecond,CategorySecondAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product,ProductAdmin)


