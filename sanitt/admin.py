# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Target, Protein, Gene

admin.site.register(Target)
admin.site.register(Protein)
admin.site.register(Gene)
