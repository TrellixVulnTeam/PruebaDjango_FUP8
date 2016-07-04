from django.conf.urls import url
#from .views import registrarArea,


urlpatterns = [
	url(r'^$', 'django.contrib.auth.views.login',{'template_name':'index/index.html'}, name='login'),
	url(r'^cerrar/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
   # url(r'^$', 'apps.index.views.index', name='index'),
    #url(r'^menu/$', 'apps.index.views.menu', name='menu'),
    url(r'^registro/$', 'apps.index.views.registro', name='registro'),
    
]
