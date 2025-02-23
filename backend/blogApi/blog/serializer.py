from rest_framework import serializers
from .models import Article,Auteur,Categorie,Comment,User
from django.utils.text import slugify

#Construction des serializeurs pour chaque model


class UserInscriptionSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    
    class Meta :
        model=User
        fields=('username','email','password')
        
    def create(self, validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AuteurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Auteur
        fields=('nom','prenom')
        
class CategorieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Categorie
        fields=('nom',)
        
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('nom','email','body','date_added','article')

class ArticleSerializer(serializers.ModelSerializer):
    auteur=serializers.StringRelatedField(read_only=True)#champ en lecture seul qui affiche l'auteur qui est immediatemenet l'utilisateur connecté
    categorie=serializers.PrimaryKeyRelatedField(queryset=Categorie.objects.all())# On choisi une categorie qui existe déja dans la base de donnée
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    
    
    class Meta:
        model=Article
        fields=('title','intro','body','auteur','categorie','date_created','image','comments')
        
    def create(self, validated_data):
        # Assosier l'article à l'utilisateur connecté
        request=self.context.get ('request') #récupère la requête actuelle depuis le contexte fourni par la vue.
        validated_data['auteur']=request.user #L'auteur devient l'utilisateur connecté
        
              # Générer le slug automatiquement
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['title'])
            
        return super().create(validated_data)
        
