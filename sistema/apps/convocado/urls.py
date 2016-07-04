from django.conf.urls import url
from .views import perfill,listarEvidencia,eliminarEvidencia,editarEvidencia,listarCaracteristica,crearUsuario,editarPerfil,user2

urlpatterns = [
   
    url(r'^perfil/$', perfill.as_view(), name="perfil" ),
    url(r'^user/$', crearUsuario.as_view(), name="user" ),
    url(r'^user2/$', user2.as_view(), name="user2" ),
    url(r'^buscarProv/$', 'apps.convocado.views.buscarProv', name='buscar-prov'),
    url(r'^buscarDist/$', 'apps.convocado.views.buscarDist', name='buscar-dist'),
    url(r'^listarCaracteristica/(?P<pk>\w+)/$', listarCaracteristica.as_view(), name='listar-caracteristica'),
    url(r'^registrarEvidencia/$', 'apps.convocado.views.registrarEvidencia', name='registrar-evidencia'),
    url(r'^contarEvidencia/$', 'apps.convocado.views.contarEvidencia', name='contar-evidencia'),
    url(r'^valorMaxCaracteristica/$', 'apps.convocado.views.valorMaxCaracteristica', name='puntajeMax-caracteristica'),
    url(r'^puntajeCaracteristica/$', 'apps.convocado.views.puntajeCaracteristica', name='puntaje-caracteristica'),
    url(r'^listarEvidencia/(?P<pk_caract>\w+)/$', listarEvidencia.as_view(), name='listar-evidencia'),
    url(r'^eliminarEvidencia/(?P<pk>\w+)/$', eliminarEvidencia.as_view(), name='eliminar-evidecia'),
    url(r'^editarEvidencia/(?P<pk>\w+)/$', editarEvidencia.as_view(), name='editar-evidecia'),
    url(r'^editarPerfil/(?P<pk>\w+)/$', editarPerfil.as_view(), name='editar-perfil'),
    #url(r'^excel/$', 'apps.convocado.views.upload', name='excel'),
    
]
