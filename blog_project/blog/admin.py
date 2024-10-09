from django.contrib import admin

from blog.models import Post

# Register your models here.

# first default way
# admin.site.register(Post)

#second custom way
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', ]
    list_filter = ['created_at', ]
