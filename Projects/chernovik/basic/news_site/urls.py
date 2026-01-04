from django.urls import path
from news_site import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_page, name='contact'),
    path('elements/', views.elements_page, name='elements'),
    # 'single-post/' o'rniga dinamik 'post/<slug:slug>/' qo'ydik
    path('post/<slug:slug>/', views.singlepost_page, name='single-post'),
    path('category/<slug:slug>/', views.category_page, name='category'),
  path('post/<slug:slug>/', views.singlepost_page, name='single-post'),
    path('category/<slug:slug>/', views.category_page, name='category'),
    path('search/', views.search_results, name='search'), # Yangi yo'l
]
