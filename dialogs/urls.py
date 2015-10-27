from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^messages/$', views.DialogView.as_view(), name='messages'),
    url(r'^messages/(?P<user_id>\d+)/$', views.DialogView.as_view(), name='messages'),

]