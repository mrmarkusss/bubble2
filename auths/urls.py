from django.conf import settings
from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGIN_URL}, name='logout'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
    url(r'^registration/(?P<token>.+)/$', views.RegistrationConfirmView.as_view(), name='registration_confirm'),
    url(r'^password-recovery/$', views.PasswordRecoveryView.as_view(), name='password_recovery'),
    url(r'^password-recovery/(?P<token>.+)/$', views.PasswordRecoveryConfirmView.as_view(), name='password_recovery_confirm'),
]
