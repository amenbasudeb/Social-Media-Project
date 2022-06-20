from django.contrib import admin
from .models import Post,Profile

class AdminPost(admin.ModelAdmin):
    list_display = ['title','slug','author','body']
    prepopulated_fields = {'slug':('title',)}
    search_fields = ('title','author__username')
    date_hierarchy = ('created')

class AdminProfile(admin.ModelAdmin):
    list_display = ('user','dob','photo')

admin.site.register(Post,AdminPost)
admin.site.register(Profile,AdminProfile)






#USERNAME-admin PASSWORD-admin
#USERNAME-venkat PASSWORD-admin@12345
#USERNAME-siva PASSWORD-admin@12345
#USERNAME-roshan PASSWORD-admin@12345
#USERNAME-kumar PASSWORD-admin@12345
#USERNAME-swaraj PASSWORD-admin@12345
