from django.contrib import admin
from main.models import Blog


# Create a custom admin class
class BlogAdmin(admin.ModelAdmin):

    list_display = ('title', 'date_created', 'last_modified', 'is_draft')
    list_filter = ('is_draft', 'date_created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'title', '-date_created'
        return ('title',)


# Register your models here.
admin.site.register(Blog, BlogAdmin)
