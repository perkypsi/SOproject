from django.urls import path

from . import views

urlpatterns = [
    path('rating/rating_so', views.rating, name='rating'),
    path('documentation/documents', views.documents, name='documents'),
    path('documentation/download_document', views.download_document, name='download_document'),
    path('documentation/<int:document_id>/delete_document', views.delete_document, name='delete_document'),

]