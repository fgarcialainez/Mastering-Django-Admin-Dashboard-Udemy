from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from main.models import Blog


# Create a custom admin class. Subclass SummernoteModelAdmin to
# apply summernote rich text editor to all TextField in the model.
class BlogAdmin(SummernoteModelAdmin):
    # Configure blogs list view filters and actions
    list_display = ('title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation')
    list_filter = ('is_draft', 'date_created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10
    actions = ('set_blogs_to_published',)
    date_hierarchy = 'date_created'

    # Configure django-summernote
    summernote_fields = '__all__'

    # Configure blog creation form
    fieldsets = (
        ('Main', {
            'fields': (('title', 'slug'), 'body'),
        }),
        ('Advanced options', {
            'fields': ('is_draft',),
            'description': "Option to configure blog creation"
        }),
    )

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'title', '-date_created'
        return ('title',)

    def set_blogs_to_published(self, request, queryset):
        """Create custom action in the admin blog list"""
        count = queryset.update(is_draft=False)

        # Show success message
        self.message_user(request, f"{count} blogs have been published")

    # Set action name in the dropdown
    set_blogs_to_published.short_description = "Mark selected blogs as published"


# Register your models here.
admin.site.register(Blog, BlogAdmin)
