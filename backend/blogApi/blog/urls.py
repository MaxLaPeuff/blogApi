from django.urls import path
from .views import (ArticleReadApiView,ArticleCreateApiView,ArticleUpdateApiView,
                    ArticleDeleteApiView,CommentCreateApiView,CommentDeleteApiView,
                    CommentUpdateApiView,UserInscriptionView,AdminViewArticleApi,
                    ModerationArticle)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns=[
    #urls pour les articles 
    path('<int:pk>/read',ArticleReadApiView.as_view()),
    path('create-list',ArticleCreateApiView.as_view()), #endpoint=http://127.0.0.1:8000/create-list
    path('<int:pk>/update',ArticleUpdateApiView.as_view()),
    path('<int:pk>/delete',ArticleDeleteApiView.as_view()),     
    path('',AdminViewArticleApi.as_view()),
    path('<int:id>/moderer',ModerationArticle.as_view()),
    #path("rechercher/",ArticleBlogRecherche.as_view()),
    
    #urls pour les commentaires 
    path('comment-create',CommentCreateApiView.as_view()), #endpoint=http://127.0.0.1:8000/comment-create
    path('<int:pk>/edit-comment',CommentUpdateApiView.as_view()),
    path('<int:pk>/delete-comment',CommentDeleteApiView.as_view()),
    
    #url d'attribution d'un tokrn a tout les utilisateurs authentifié
    #TokenObtainPairView : permet à l'utilisateur d'obtenir un access token et un refresh token après s'être authentifié (via ses identifiants).
    #TokenRefreshView : permet de rafraîchir l'access token avec le refr
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #endpoint=http://127.0.0.1:8000/api/token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #endpoint=http://127.0.0.1:8000/api/token/refresh/
    
    #url pour l'inscription
    path('register',UserInscriptionView.as_view(),name='register'), #endpoint=http://127.0.0.1:8000/register
    
]
    
    
