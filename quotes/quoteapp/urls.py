from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('quote/', views.quote, name='quote'),
    path('author/', views.author, name='author'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('authordetail/<int:author_id>', views.authordetail, name='authordetail'),
    path('migrateDB/', views.migrate_db, name='migrateDB')
]
