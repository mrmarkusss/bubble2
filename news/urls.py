from django.conf.urls import url
from news import views

urlpatterns = [
    url(r'^news/$', views.NewsView.as_view(), name='news'),

]