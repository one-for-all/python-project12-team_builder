from django.contrib import admin

from . import models


class PositionInline(admin.StackedInline):
    model = models.Position
    extra = 0


class SiteProjectAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'timeline', 'applicant_requirements',
              'owner']
    inlines = [PositionInline]


admin.site.register(models.SiteProject, SiteProjectAdmin)
admin.site.register(models.Application)
