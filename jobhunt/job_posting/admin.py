from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.register(Job, JobAdmin)