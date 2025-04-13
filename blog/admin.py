from django.contrib import admin
from .models import Article,Auteur,Categorie,Comment
# Register your models here.

admin.site.register(Article)
admin.site.register(Categorie)
admin.site.register(Auteur)
admin.site.register(Comment)

