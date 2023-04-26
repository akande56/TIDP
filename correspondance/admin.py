from django.contrib import admin
from .models import Folder_Content, Folder, File, Routing, Comment
 # Register your models here.


admin.site.register(Folder_Content)
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Routing)
admin.site.register(Comment)