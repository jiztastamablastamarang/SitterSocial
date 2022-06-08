from django.urls import include, re_path
from django.contrib import admin
from django.views.generic import TemplateView
from .views import UserLoginView, RegisterView
admin.autodiscover()

urlpatterns = [
    re_path(r'user_login/$', UserLoginView.as_view(), name='user_login'),
    re_path(r'user_signup/$', RegisterView.as_view(), name='user_signup'),
    re_path(r'signup/$', TemplateView.as_view(template_name="signup.html"), name='signup'),
    re_path(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    re_path(r'^login/', TemplateView.as_view(template_name="login.html"), name='login'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^dj-rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]



