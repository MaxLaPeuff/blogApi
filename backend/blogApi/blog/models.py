from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Categorie(models.Model):
    nom=models.CharField(max_length=200)
    
    def __str__(self):
        return self.nom

class Auteur(models.Model):
    nom=models.CharField(max_length=200)
    prenom=models.CharField(max_length=200)
class Article(models.Model):
    title=models.CharField(max_length=200)
    intro=models.CharField(max_length=400)
    body=models.TextField()
    image=models.ImageField(upload_to='media')
    auteur=models.ForeignKey(User,on_delete=models.CASCADE)#L'auteur est lié a l'utilisateur connecté
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    date_created=models.DateTimeField(default=timezone.now)
    slug=models.SlugField(unique=True,blank=True)
    is_approved=models.BooleanField(default=False)
    
    class Meta :
        ordering=['-date_created']
        
    def __str__(self):
        
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    nom=models.CharField(max_length=200)
    email=models.EmailField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        
    def __str__(self):
        return f"Commenté par :{self.nom} sur {self.article}"
