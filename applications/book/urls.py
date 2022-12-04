from django.urls import path

from applications.book import views

urlpatterns = [
    path('', views.BookListCreateApiView.as_view()),
    path('<int:pk>/', views.BookRetrieveUpdateApiView.as_view()),
    path('del/<int:pk>/', views.book_del_api_view),
]
