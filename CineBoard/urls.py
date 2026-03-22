from django.urls import path
from .views import *

urlpatterns = [
    path('', FilmListView.as_view(), name='film_list'),
    path('film/<int:pk>/', FilmDetailView.as_view(), name='film_detail'),

    path('create/', FilmCreateView.as_view(), name='film_create'),
    path('update/<int:pk>/', FilmUpdateView.as_view(), name='film_update'),
    path('delete/<int:pk>/', FilmDeleteView.as_view(), name='film_delete'),

    path('comment/<int:pk>/', CommentCreateView.as_view(), name='add_comment'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]