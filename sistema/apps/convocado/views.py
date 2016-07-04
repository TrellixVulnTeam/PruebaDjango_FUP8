from django.shortcuts import render
from django.contrib.auth.decorators  import  login_required
#@ Login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import HttpResponseBadRequest
import django_excel as excel
from django import forms
from django.shortcuts import render_to_response,HttpResponse,RequestContext,HttpResponseRedirect
from django.views.generic import CreateView,ListView,TemplateView,UpdateView
from .models import ubigeo, perfil, evidencia_convocatoria,tipo_evidencia,convocado_convocatoria
from apps.evaluacion.models import rubro_conv, caracteristica_conv,item_conv,convocatoria
import os

# Create your views here.

class crearUsuario(CreateView):
	model = User
	fields = ('username','password')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.password2 = self.request.POST['password2']
		if self.object.password == self.object.password2:
			user= User.objects.create_user(self.object.username,'', self.object.password2)
			user.save()
		return HttpResponseRedirect(reverse('perfil'))

class perfill(TemplateView):
    template_name = 'convocado/perfil.html'

    def get_context_data(self, **kwargs):
        context = super(perfill, self).get_context_data(**kwargs)
        dpt = ubigeo.objects.filter(codProv='00', codDist='00')
        per = perfil.objects.get(user_id=self.request.user)
        ## sesion
        #del self.request.session['convocado']
        conv = convocatoria.objects.get(estado="1")
        convocado_conv = convocado_convocatoria.objects.get(convocado_id=per.id,convocatoria_id=conv.id)
        self.request.session['convocado'] = convocado_conv.id
        # fin sesion
        if per.ubigeo:
            context['provincia'] = ubigeo.objects.exclude(codProv='00').values().filter(codDpto=per.ubigeo[0:2],codDist='00')
            context['distrito'] = ubigeo.objects.exclude(codDist='00').values().filter(codDpto=per.ubigeo[0:2],codProv=per.ubigeo[2:4])
        if per.ubigeo_act:
            context['provincia2'] = ubigeo.objects.exclude(codProv='00').values().filter(codDpto=per.ubigeo_act[0:2],codDist='00')
            context['distrito2'] = ubigeo.objects.exclude(codDist='00').values().filter(codDpto=per.ubigeo_act[0:2],codProv=per.ubigeo_act[2:4]) 
        context['perfil'] = per
        context['dpt'] = dpt
        context['rubro'] = rubro_conv.objects.filter(convocatoria_id=1)
        return context

class user2(CreateView):
    template_name = 'index/index.html'
    model = User
    fields = ('username','password','email')
    #fields = ('nombre','ap_pat','ap_mat','dni','fecha_nac','estado_civil','sexo','direccion','ubigeo','direccion_act','telefono','celular','email','ubigeo_act')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.password2 = self.request.POST['password2']
        self.object.email = self.request.POST['email']
        nombres= self.request.POST['nombres']
        paterno = self.request.POST['paterno']
        materno = self.request.POST['materno']
        if self.object.password == self.object.password2:
            user= User.objects.create_user(self.object.username,self.object.email, self.object.password2)
            user.save()
            if user:
                per = perfil(user_id = user.id,
                            email = user.email,
                            dni = user.username,
                            nombre = nombres,
                            ap_pat = paterno,
                            ap_mat = materno

                )
            per.save()
            if per:
                conv = convocatoria.objects.get(estado="1")
                convocado = convocado_convocatoria(convocado_id=per.id,
                                                    convocatoria_id= conv.id,
                                                    estado_conv = "0"

                    )
            convocado.save()
            
        return HttpResponseRedirect(reverse('login'))

class editarPerfil(UpdateView):
    template_name = 'convocado/perfil.html'
    model = perfil
    fields = ['nombre','ap_pat','ap_mat','dni','fecha_nac','estado_civil','sexo','direccion','ubigeo','direccion_act','telefono','celular','email','ubigeo_act','foto']
    success_url = '/perfil/'

    def get_context_data(self, **kwargs):
        context = super(editarPerfil, self).get_context_data(**kwargs)
        dpt = ubigeo.objects.filter(codProv='00', codDist='00')
        context['dpt'] = dpt
        context['rubro'] = rubro_conv.objects.filter(convocatoria_id=1)
        perf = perfil.objects.get(user_id=self.request.user)
        context['perfil'] = perf
        print(perf)
        context['provincia'] = ubigeo.objects.exclude(codProv='00').values().filter(codDpto=perf.ubigeo[0:2],codDist='00')
        context['distrito'] = ubigeo.objects.exclude(codDist='00').values().filter(codDpto=perf.ubigeo[0:2],codProv=perf.ubigeo[2:4])
        context['provincia2'] = ubigeo.objects.exclude(codProv='00').values().filter(codDpto=perf.ubigeo_act[0:2],codDist='00')
        context['distrito2'] = ubigeo.objects.exclude(codDist='00').values().filter(codDpto=perf.ubigeo_act[0:2],codProv=perf.ubigeo_act[2:4])
        return context


def buscarProv(request):
	if request.method == 'POST':
		dpt = request.POST['dept']			
	ubigeo_prov = ubigeo.objects.exclude(codProv='00').values().filter(codDpto=dpt,codDist='00')
	return render_to_response('convocado/prov.html', {'prov' : ubigeo_prov }, context_instance=RequestContext(request))

def buscarDist(request):
	if request.method == 'POST':
		dpt = request.POST['dpt']
		
	else:
		dpt = ''
	print(dpt)	
	print(dpt[3:4])
	ubigeo_dist = ubigeo.objects.exclude(codDist='00').values().filter(codDpto=dpt[0:2],codProv=dpt[2:4])
	return render_to_response('convocado/prov.html', {'dist' : ubigeo_dist }, context_instance=RequestContext(request))

def registrarEvidencia(request):
	if request.method == 'POST':
		cargo_rol = request.POST['cargo_rol']
		tipo_evidencia = request.POST['tipo_evidencia']
		evidencia = request.FILES['evidencia']
		caracteristica = request.POST['caracteristica']
		numero_evidencia = request.POST['numero_evidencia']
		tiempo = request.POST['tiempo']
		item = request.POST['item']
		if not tiempo:
			tiempo=0

		caract = caracteristica_conv.objects.get(id=caracteristica)
		if caract.valor_max:
			puntaje_calculado = caract.valor_max
		if caract.puntaje_max and caract.factor:
			puntaje_calculado = caract.puntaje_fact*tiempo
		if caract.factor:
			puntaje_calculado = caract.puntaje_fact*tiempo
		if caract.puntaje_max and not caract.factor:
			puntaje_calculado = puntaje_max
		print(puntaje_calculado)
		evidencia_conv = evidencia_convocatoria(cargo_rol = cargo_rol,
												tipo_evidencia_id = tipo_evidencia,
												evidencia = evidencia,
												convocado_convocatoria_id = self.request.session.get('convocado'),
												numero_evidencia  = numero_evidencia,
												estado_eval = '0',
												tiempo = tiempo,
												item = item,
												puntaje_calculado = int(puntaje_calculado),
												caracteristica_conv_id = caracteristica) 
		evidencia_conv.save()
	return HttpResponseRedirect(reverse('listar-caracteristica', kwargs={'pk':caract.item_conv_id}))
	#return render_to_response('convocado/listar_caracteristica.html', { }, context_instance=RequestContext(request))

def contarEvidencia(request):
	if request.method == 'POST':
		conv_conv = request.POST['conv_conv']
		caract = request.POST['caract']
		contador = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=request.session.get('convocado'),caracteristica_conv_id=caract).count()
		print("alexlo")
	return render_to_response('convocado/contar_evidencia.html', {'contador' : contador }, context_instance=RequestContext(request))

def puntajeCaracteristica(request):
	if request.method == 'POST':
		conv_conv = request.POST['conv_conv']
		caract = request.POST['caract']
		evidencia = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=request.session.get('convocado'),caracteristica_conv_id=caract)
		suma = 0
		for evid in evidencia:
			suma =  suma + evid.puntaje_calculado
	return render_to_response('convocado/suma_caracteristica.html', {'suma' : suma }, context_instance=RequestContext(request))

def valorMaxCaracteristica(request):
	if request.method == 'POST':
		caract = request.POST['caract']
		caracteristica = caracteristica_conv.objects.get(pk=caract)

	return render_to_response('convocado/puntaje_caracteristica.html', {'caracteristica' : caracteristica }, context_instance=RequestContext(request))


class listarEvidencia(ListView):
    context_object_name = "evidencia"
    template_name = "convocado/listar_evidencia.html"

    def get_queryset(self,*args, **kwargs):
        caract = self.kwargs['pk_caract']
        #self.publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return evidencia_convocatoria.objects.filter(convocado_convocatoria_id=self.request.session.get('convocado'),caracteristica_conv_id=caract)

    def get_context_data(self, **kwargs):
    	caract = self.kwargs['pk_caract']
    	context = super(listarEvidencia, self).get_context_data(**kwargs)
    	#context['caract'] = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=2,caracteristica_conv_id=caract).values('caracteristica_conv').distinct()
    	context['caract'] = caracteristica_conv.objects.get(pk=caract)
    	return context

class eliminarEvidencia(TemplateView):
    #template_name = 'evaluacion/caracteristica_conv.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        evidencia= evidencia_convocatoria.objects.get(pk=pk)
        caract = evidencia.caracteristica_conv_id
        evidencia.delete()
        return HttpResponseRedirect(reverse('listar-evidencia', kwargs={'pk_caract':caract}))

class editarEvidencia(UpdateView):
    template_name = 'convocado/listar_evidencia.html'
    model = evidencia_convocatoria
    fields = ['evidencia','numero_evidencia','cargo_rol','tipo_evidencia']

    def get_success_url(self):
        pk=self.kwargs['pk']
        evidencia = evidencia_convocatoria.objects.get(pk=pk)
        return reverse('listar-evidencia', kwargs={'pk_caract': evidencia.caracteristica_conv_id})

    def get_context_data(self, **kwargs):
    	pk_evid = self.kwargs['pk']
    	evidencia = evidencia_convocatoria.objects.get(pk=pk_evid)
    	context = super(editarEvidencia, self).get_context_data(**kwargs)
    	context['evidencia'] = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=self.request.session.get('convocado'),caracteristica_conv_id=evidencia.caracteristica_conv)
    	context['caract'] = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=self.request.session.get('convocado'),caracteristica_conv_id=evidencia.caracteristica_conv).values('caracteristica_conv').distinct()
    	context['evidencia_pk'] = evidencia
    	context['tipo_evidencia'] = tipo_evidencia.objects.all()
    	return context


class listarCaracteristica(ListView):
    context_object_name = "caracteristica"
    template_name = "convocado/listar_caracteristica.html"

    def get_queryset(self,*args, **kwargs):
        item = self.kwargs['pk']
        #self.publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return caracteristica_conv.objects.filter(item_conv_id=item).order_by('numeracion')

    def get_context_data(self, **kwargs):
    	item = self.kwargs['pk']
    	suma = 0
    	evid = evidencia_convocatoria.objects.filter(convocado_convocatoria_id=self.request.session.get('convocado'),item_conv_id=item)
    	for evid in evid:
    		suma = suma + evid.puntaje_calculado

    	context = super(listarCaracteristica, self).get_context_data(**kwargs)
    	context['tipo_evid'] = tipo_evidencia.objects.all()
    	context['item'] = item_conv.objects.get(pk=item)
    	context['sumaPorItem'] = suma
    	return context
"""
def import_data2(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        def choice_func(row):
            print row[0]
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        if form.is_valid():
            request.FILES['file'].save_book_to_database(
                models=[
                    (Question, ['question_text', 'pub_date', 'slug'], None, 0),
                    (Choice, ['question', 'choice_text', 'votes'], choice_func, 0)
                 ]
                )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
    else:
"""
def import_data(request):
    if request.method == "POST":
        listaConvocado = request.FILES['convocado']

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row
        request.FILES['file'].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ['question_text', 'pub_date', 'slug'],
                    ['question', 'choice_text', 'votes']]
            )
        return HttpResponse("OK", status=200)
    else:
        form = UploadFileForm()
    return render_to_response(
        'upload_form.html',
        {
            'form': form,
            'title': 'Import excel data into database example',
            'header': 'Please upload sample-data.xls:'
        },
        context_instance=RequestContext(request))