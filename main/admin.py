from django_summernote.admin import SummernoteModelAdmin
from django.db.models import Count
from django.contrib import admin
from main.models import Blog, Comment, Category


class CommentInline(admin.TabularInline):
    """Edit comments in the blog details page"""
    model = Comment
    fields = ('text', 'is_active')
    classes = ('collapse',)
    extra = 1


class BlogAdmin(SummernoteModelAdmin):
    """
    Create a custom admin class. Subclass SummernoteModelAdmin to
    apply summernote rich text editor to all TextField in the model.
    """

    # Configure blogs list view filters and actions
    list_display = ('title', 'date_created', 'last_modified', 'is_draft', 'days_since_creation',
                    'number_of_comments')
    list_filter = ('is_draft', 'date_created',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10
    actions = ('set_blogs_to_published',)
    date_hierarchy = 'date_created'
    inlines = [CommentInline]

    # Configure django-summernote
    summernote_fields = '__all__'

    # Configure blog creation form
    fieldsets = (
        ('Main', {
            'fields': (('title', 'slug'), 'body'),
        }),
        ('Advanced options', {
            'fields': ('is_draft', 'categories',),
            'description': "Option to configure blog creation",
            'classes': ('collapse',)
        }),
    )

    # Improve blog categories selection UI
    filter_horizontal = ('categories',)

    def get_queryset(self, request):
        # Include a new field to count the number of comments
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comments_count=Count('comments'))
        return queryset

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'title', '-date_created'
        return ('title',)

    def number_of_comments(self, blog):
        return blog.comments_count

    def set_blogs_to_published(self, request, queryset):
        """Create custom action in the admin blog list"""
        count = queryset.update(is_draft=False)

        # Show success message
        self.message_user(request, f"{count} blogs have been published")

    # Set action name in the dropdown
    set_blogs_to_published.short_description = "Mark selected blogs as published"

    # Add sorting by comments_count calculated field
    number_of_comments.admin_order_field = "comments_count"


class CommentAdmin(admin.ModelAdmin):
    """Create a custom admin class for the Comment model"""
    list_display = ('blog', 'text', 'date_created', 'is_active')
    list_editable = ('is_active',)
    list_per_page = 20


# Register your models here.
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)
