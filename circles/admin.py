# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):

    list_display = (
        'slug_name',
        'name',
        'is_public',
        'verified',
        'is_limited',
        'members_limit'
    )
    search_fields=('slug_name','name')
    list_filter = (
        'is_public',
        'verified',
        'is_limited'
    )