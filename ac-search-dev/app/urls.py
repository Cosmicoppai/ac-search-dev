from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api', views.SearchApi.as_view(), name='search-api'),
    path('search', views.SearchView.as_view(), name='search-post'),
    ]



