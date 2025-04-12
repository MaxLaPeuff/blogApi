from .models import Article,Auteur,Categorie,Comment,User
from .serializer import ArticleSerializer,AuteurSerializer,CategorieSerializer,CommentSerializer,UserInscriptionSerializer
from rest_framework import generics,mixins
from django.core.exceptions import PermissionDenied
from .permissions import IsAuthorOrReadOnly,Isadmin
from rest_framework.views import APIView
#from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

"""IMPLEMENTATION CRUD PAR LES VUES GENERIQUE """

#Vue generique pour affichage des articles 
class ArticleReadApiView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    @swagger_auto_schema(
        operation_description="Récupérer un article par ID",
        responses={200: ArticleSerializer(),404: "Article non trouvé"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

#Vue générique pour la creation et l'affichage des articles sous forme de liste 
class ArticleCreateApiView(generics.ListCreateAPIView):
    queryset=Article.objects.filter(is_approved=True)
    serializer_class=ArticleSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Créer un nouvel article",
        request_body=ArticleSerializer,
        responses={201: ArticleSerializer(), 400: "Erreur lors de la création de l'article"}
    )
    
    def get_serializer_context(self):
        # Ajouter la requête actuelle au contexte pour que le sérialiseur puisse y accéder
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
class AdminViewArticleApi(generics.ListAPIView):
    permission_classes=[Isadmin]
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    
    
    @swagger_auto_schema(
        operation_description="Récupérer la liste de tous les articles (admin)",
        responses={200: ArticleSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    
"""CETTE VUE EST UNIQUEMENT AUTORISÉ A L'ADMIN .
ON VERIFIE BIEN QUE L'ADMINA SELECTIONNER UN ARTICLE PUIS EN FONCTION DE L'ACTION QU'IL 
DECIDE DE FAIRE LA VUE VA SOIT ACCEPTER SOIT REJETER L'ARTICLE EN ATTENTE """
   
class ModerationArticle(APIView):
    permission_classes=[Isadmin]
    
    @swagger_auto_schema(
        operation_description="Approuver ou rejeter un article",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING, enum=['approuver', 'rejeter'], description="Action à effectuer sur l'article")
            }
        ),
        responses={
            200: "Article modifié avec succès",
            404: "Article non trouvé",
            400: "Action non valide"
        }
    )
    
    def post(self, request, id):
        return super().post(request, id)
    
    def post(self,request,id):
        try:
            article=Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response({"Erreur, veuillez sélectionner un article"}, status=status.HTTP_404_NOT_FOUND)
        
        action=request.data.get('action')
        if action=="approuver":
            article.is_approved=True
            article.save()
            return Response({"message":"Article validé avec succes"},status=status.HTTP_200_OK)
        elif action == "rejeter":
            article.delete()
            return Response({"message":"Article rejeté avec succes"},status=status.HTTP_200_OK)
        else:
            return Response({"erreur"},status=status.HTTP_400_BAD_REQUEST)

            
#Vue générique pour la mise à jour des articles 
class ArticleUpdateApiView(generics.UpdateAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    lookup_field='pk'
    
    @swagger_auto_schema(
        operation_description="Mettre à jour un article",
        request_body=ArticleSerializer,
        responses={200: ArticleSerializer(), 404: "Article non trouvé"}
    )
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def perform_update(self, serializer):
        # Vérifier que l'utilisateur connecté est bien l'auteur de l'article
        if self.request.user != serializer.instance.auteur:
            raise PermissionDenied("Vous n'avez pas la permission de modifier cet article.")
        serializer.save()
    
#Vue générique pour la supression des articles
class ArticleDeleteApiView(generics.DestroyAPIView):
    queryset=Article.objects.all()
    serializer_class=ArticleSerializer
    permission_classes=[IsAuthorOrReadOnly]
    lookup_field='pk'
    
    @swagger_auto_schema(
        operation_description="Supprimer un article",
        responses={204: "Article supprimé avec succès", 404: "Article non trouvé"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
#Vue pour la recherche des articles 
"""
class ArticleBlogRecherche(APIView):
    def get(self,request):
        query=request.query_params.get('q',None) # cette ligne récupère le paramètre nommé q qui est passé dans l'url , s'il n'y en a pas , on retourne None
        if query:
            articles=Article.objects.filter(
                Q(title__icontains=query)|Q(body__icontains=query)|Q(categorie__icontains=query) #cette ligne filtre les recherches d'articles en fonctions du titre , du body et de la categorie
            )
            serializer = ArticleSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response ({"message": "SVP rentrer l'élement de recherche!"} , status=status.HTTP_400_BAD_REQUEST)
""" 
         
"""IMPLEMENTENTION CRUD POUR LES COMMENTAIRES"""
#Vue générique pour la creation et l'affichage des commentaires sous forme de liste 
class CommentCreateApiView(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
    @swagger_auto_schema(
        operation_description="Créer un nouveau commentaire",
        request_body=CommentSerializer,
        responses={201: CommentSerializer(), 400: "Erreur lors de la création du commentaire"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
#Vue générique pour la mise à jour des commentaires 
class CommentUpdateApiView(generics.UpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'
    
    @swagger_auto_schema(
        operation_description="Mettre à jour un commentaire",
        request_body=CommentSerializer,
        responses={200: CommentSerializer(), 404: "Commentaire non trouvé"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
#Vue générique pour la supression des commentaires
class CommentDeleteApiView(generics.DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    lookup_field='pk'
    
    @swagger_auto_schema(
        operation_description="Supprimer un commentaire",
        responses={204: "Commentaire supprimé avec succès", 404: "Commentaire non trouvé"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    
"""VUE POUR L'INSCRIPTION DES UTILISATEURS """

class UserInscriptionView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserInscriptionSerializer
    
    @swagger_auto_schema(
        operation_description="Inscription d'un nouvel utilisateur",
        request_body=UserInscriptionSerializer,
        responses={201: UserInscriptionSerializer(), 400: "Erreur lors de l'inscription"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)