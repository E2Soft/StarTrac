from django.contrib import admin

from . import models


admin.site.register(models.Task)
admin.site.register(models.Requirement)

admin.site.register(models.Milestone)

admin.site.register(models.Comment)
admin.site.register(models.StateChange)

admin.site.register(models.Commit)
admin.site.register(models.PriorityChange)
admin.site.register(models.AddEvent)
admin.site.register(models.ResolveEvent)

admin.site.register(models.UserExtend)

