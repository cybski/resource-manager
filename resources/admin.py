from django.contrib import admin
from . import models

admin.site.register(models.Resource)
admin.site.register(models.Employee)


class ResourceReleaseAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url="", extra_context=None):
        data = request.GET.copy()
        data["released_by"] = request.user
        request.GET = data

        return super(ResourceReleaseAdmin, self).add_view(
            request, form_url, extra_context
        )


admin.site.register(models.ResourceRelease, ResourceReleaseAdmin)
