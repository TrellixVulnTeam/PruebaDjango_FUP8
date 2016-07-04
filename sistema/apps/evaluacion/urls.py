from django.conf.urls import url
from .views import registrarRubro,registrarItem,registrarCaracteristica,registrarConvocatoria,configEvaluacion,itemConv,caracteristicaConv,eliminarRubroConv,editarRubroConv,eliminaritemConv,editarItemConv,eliminarCaractConv,editarCaractConv,listarItem


urlpatterns = [
    url(r'^regRubro/$', registrarRubro.as_view(), name="registrar-rubro" ),
   # url(r'^opRubro/$', openRubro.as_view(), name="open-rubro" ),
    url(r'^regItem/$', registrarItem.as_view(), name="registrar-item" ),
    url(r'^regCaracteristica/$', registrarCaracteristica.as_view(), name="registrar-caracteristica" ),
    url(r'^regEvaluacion/$', registrarConvocatoria.as_view(), name='registrar-convocatoria'),
    url(r'^configEvaluacion/(?P<pk>\w+)/$', configEvaluacion.as_view(), name='config-convocatoria'),
    url(r'^itemConv/(?P<pk>\w+)/(?P<conv>\w+)/$', itemConv.as_view(), name='item-conv'),
    url(r'^caracteristicaConv/(?P<pk>\w+)/(?P<rub>\w+)/$', caracteristicaConv.as_view(), name='caracteristica-conv'),

    url(r'^alex/$', 'apps.evaluacion.views.importarEvaluacion', name='impor-conv'),
    url(r'^eliminarRubConv/(?P<id>\w+)/(?P<conv>\w+)/$', eliminarRubroConv.as_view(), name='eliminar-rubro-conv'),
    url(r'^editarRubConv/(?P<pk>\w+)/$', editarRubroConv.as_view(), name='editar-rubro-conv'),
    url(r'^eliminarItemConv/(?P<id>\w+)/(?P<conv>\w+)/$', eliminaritemConv.as_view(), name='eliminar-item-conv'),
    url(r'^editarItemConv/(?P<pk>\w+)/(?P<conv>\w+)/$', editarItemConv.as_view(), name='editar-item-conv'),
    url(r'^eliminarCaractConv/(?P<id>\w+)/$', eliminarCaractConv.as_view(), name='eliminar-caracteristica-conv'),
    url(r'^editarCaractConv/(?P<pk>\w+)/$', editarCaractConv.as_view(), name='editar-caracteristica-conv'),
    #url(r'^eliminarRubro/(?P<pk>\w+)/$', eliminarRubro.as_view(), name="eliminar-rubro" ),
    url(r'^crearRubro/$', 'apps.evaluacion.views.crearRubro', name='crear-rubro'),
    url(r'^crearItem/$', 'apps.evaluacion.views.crearItem', name='crear-item'),
    url(r'^crearCaracteristica/$', 'apps.evaluacion.views.crearCaracteristica', name='crear-caracteristica'),

    url(r'^listarItem/(?P<pk>\w+)/$', listarItem.as_view(), name='listar-item'),
    
]
