from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse,reverse_lazy
from django.shortcuts import render_to_response,HttpResponse,RequestContext,HttpResponseRedirect
from django.views.generic import CreateView,TemplateView,ListView,UpdateView,DeleteView
from .models import rubro,item,caracteristica,convocatoria,rubro_conv,item_conv,caracteristica_conv
from apps.convocado.models import tipo_evidencia

# Create your views here.


class registrarRubro(CreateView):
	template_name = 'evaluacion/reg_rubro.html'
	model = rubro
	fields = ('nombre',)
	#success_url = reverse_lazy('registrar_marca')

	def form_valid(self, form):
		self.object = form.save(commit=False) 
		self.object.estado = '1'
		self.object.save()
		return HttpResponseRedirect('/regRubro/')

def crearRubro(request):
    if request.method == 'POST':
        r_rubro = request.POST['rubro']
        pk = request.POST['conv']
        rubro_b = rubro.objects.filter(nombre=r_rubro)
        if not rubro_b:
            rub = rubro(nombre = r_rubro,
                                estado = "1")
            rub.save()

    return HttpResponseRedirect(reverse('config-convocatoria', kwargs={'pk': pk}))
class registrarItem(CreateView):
	template_name = 'evaluacion/reg_item.html'
	model = item
	fields = ('nombre',)
	#success_url = reverse_lazy('registrar_marca')

	def form_valid(self, form):
		self.object = form.save(commit=False) 
		self.object.estado = '1'
		self.object.save()
		return HttpResponseRedirect('/regItem/')


def crearItem(request):
    if request.method == 'POST':
        r_item = request.POST['item']
        pk = request.POST['rubro']
        conv = request.POST['conv']
        item_b = item.objects.filter(nombre=r_item)
        if not item_b:
            ite = item(nombre = r_item,
                                estado = "1")
            ite.save()

    return HttpResponseRedirect(reverse('item-conv', kwargs={'pk': pk,'conv':conv}))

class registrarCaracteristica(CreateView):
	template_name = 'evaluacion/reg_caracteristica.html'
	model = caracteristica
	fields = ('nombre',)
	print("hhhhh")
	#success_url = reverse_lazy('registrar_marca')

	def form_valid(self, form):
		print("xxxxx")
		self.object = form.save(commit=False) 
		self.object.estado = '1'
		print("sssss")
		self.object.save()
		return HttpResponseRedirect('/regCaracteristica/')

def crearCaracteristica(request):
    if request.method == 'POST':
        r_caract = request.POST['caracteristica']
        r_item = request.POST['item']
        r_rubro = request.POST['rubro']
        carct_b = caracteristica.objects.filter(nombre=r_caract)
        if not carct_b:
            caract = caracteristica(nombre = r_caract,
                                estado = "1")
            caract.save()

    return HttpResponseRedirect(reverse('caracteristica-conv', kwargs={'pk': r_item,'rub':r_rubro}))

class registrarConvocatoria(CreateView):
	template_name = 'evaluacion/reg_convocatoria.html'
	model = convocatoria
	fields = ('periodo','fecha_inicio','fecha_fin')
	#success_url = reverse_lazy('registrar_marca')

	def form_valid(self, form):
		self.object = form.save(commit=False) 
		self.object.save()
		pk = self.object.id
		return HttpResponseRedirect(reverse('config-convocatoria', kwargs={'pk': pk}))


class configEvaluacion(CreateView):
    template_name = 'evaluacion/rubro_conv.html'
    model = rubro_conv
    fields = ('peso','rubro','numeracion')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        self.object = form.save(commit=False)
        rub = rubro.objects.all()
        msj = "alexlo"
       # r_id=""
        val =0
        #for r in rub:
           # if r.id == self.object.rubro_id:
               # msj = "el rubro ya exixte"
               # print(msj)
               # r_id = r.id   #si existe obtengo el id para intsertar en la tabla rubro evaluacion

        rubro_c = rubro_conv.objects.filter(convocatoria_id=pk)
        for r in rubro_c:
            if r.rubro_id == self.object.rubro_id:
                val = 1

        if val==0:
           # self.object.rubro_id = r_id
            self.object.convocatoria_id = pk
            self.object.save()
            print("alexlo27")
        else:
            self.success_message = " El rubro ya existe"
            print('el rubro ya existe para la evalucion')
            print(self.success_message)
        return HttpResponseRedirect(reverse('config-convocatoria', kwargs={'pk': pk}))

    def get_context_data(self, **kwargs):
        context = super(configEvaluacion, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['convocatorias'] = convocatoria.objects.all()
        context['convocatoria'] = convocatoria.objects.get(id=pk)
        context['rubro'] = rubro_conv.objects.filter(convocatoria_id=pk).order_by('numeracion')
        context['rubros'] = rubro.objects.all()
        return context


class eliminarRubroConv(TemplateView):
    template_name = 'evaluacion/config_evaluacion.html'

    def get(self, request, *args, **kwargs):
    	pk = self.kwargs['id']
    	conv = self.kwargs['conv']
    	rub = rubro_conv.objects.get(pk=pk)
    	rub.delete()
    	return HttpResponseRedirect(reverse('config-convocatoria', kwargs={'pk':conv}))



class editarRubroConv(UpdateView):
    template_name = 'evaluacion/rubro_conv.html'
    model = rubro_conv
    fields = ['rubro','peso','numeracion']

    def get_success_url(self):
        pk=self.kwargs['pk']
        rub = rubro_conv.objects.get(pk=pk)
        return reverse('config-convocatoria', kwargs={'pk': rub.convocatoria_id})

    def form_valid(self, form):
        pk = self.kwargs['pk']
        val = 0
        rub = rubro_conv.objects.get(pk=pk)
        self.object = form.save(commit=False)
        rubro_c = rubro_conv.objects.filter(convocatoria_id=rub.convocatoria_id)
        for r in rubro_c:
            if r.rubro_id == self.object.rubro_id:
                if rub.rubro_id == self.object.rubro_id:
                    val = 0
                else:
                    val = 1

            if val == 0:
                rubro_conv.objects.filter(pk=pk).update(rubro_id=self.object.rubro_id,peso=self.object.peso,numeracion=self.object.numeracion)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
		# Llamamos ala implementacion para traer un primer context
        context = super(editarRubroConv, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        rub = rubro_conv.objects.get(pk=pk)
        context['convocatoria'] = convocatoria.objects.get(id=rub.convocatoria_id)
        context['rubro'] = rubro_conv.objects.filter(convocatoria_id=rub.convocatoria_id).order_by('numeracion')
        context['rubros'] = rubro.objects.all()
        context['rubro_pk'] = rub
        return context


class itemConv(CreateView):
    template_name = 'evaluacion/item_conv.html'
    model = item_conv
    fields = ('valor_max','item','numeracion')

    def form_valid(self, form):
        pk = self.kwargs['pk']
        conv = self.kwargs['conv']
        self.object = form.save(commit=False)
        it = item.objects.all()
        it_id=""
        val = 0
        for i in it:
            if i.id == self.object.item_id:
                msj = "el item ya existe"
                print(msj)
                it_id = i.id

        alex = rubro_conv.objects.get(rubro_id=pk,convocatoria_id=conv)
        self.object.item_id = it_id
        self.object.rubro_conv_id = alex.id
        item_c = item_conv.objects.filter(rubro_conv_id=alex.id)
        for ite in item_c:
            if ite.item_id == self.object.item_id:
                val=1

        if val == 0:
            self.object.save()
        else:
            print("ya existe item para ese rubro")

        return HttpResponseRedirect(reverse('item-conv', kwargs={'pk': pk,'conv':conv}))

    def get_context_data(self, **kwargs):
        context = super(itemConv, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        conv = self.kwargs['conv']
        alex = rubro_conv.objects.get(rubro_id=pk,convocatoria_id=conv)
        context['items'] = item.objects.all()
        context['rubro'] = alex
        context['conv'] = conv
        context['item'] = item_conv.objects.filter(rubro_conv_id=alex.id).order_by('numeracion')
        return context


class listarItem(ListView):
    context_object_name = "item"
    template_name = "evaluacion/listar_item.html"

    def get_queryset(self,*args, **kwargs):
        rub = self.kwargs['pk']
        #self.publisher = get_object_or_404(Publisher, name__iexact=self.args[0])
        return item_conv.objects.filter(rubro_conv_id=rub).order_by('numeracion')

class eliminaritemConv(TemplateView):
	template_name = 'evaluacion/item_conv.html'

	def get(self, request, *args, **kwargs):
		pk = self.kwargs['id']
		conv = self.kwargs['conv']
		rub = item_conv.objects.get(pk=pk)
		rubro_pk = rubro_conv.objects.get(pk=rub.rubro_conv_id)
		id_rubro = rubro_pk.rubro_id
		rub.delete()
		return HttpResponseRedirect(reverse('item-conv', kwargs={'pk':id_rubro ,'conv':conv}))


class editarItemConv(UpdateView):
    template_name = 'evaluacion/item_conv.html'
    model = item_conv
    fields = ['item','valor_max','numeracion']

    def get_success_url(self):
        pk=self.kwargs['pk']
        conv = self.kwargs['conv']
        rub = item_conv.objects.get(pk=pk)
        rubro_pk = rubro_conv.objects.get(pk=rub.rubro_conv_id)
        return reverse('item-conv', kwargs={'pk': rubro_pk.rubro_id,'conv':conv})

    def form_valid(self, form):
        pk = self.kwargs['pk']
        val = 0
        self.object = form.save(commit=False)
        rub_id = item_conv.objects.get(pk=pk)
        item_c = item_conv.objects.filter(rubro_conv_id=rub_id.rubro_conv_id)
        for ite in item_c:
            if ite.item_id == self.object.item_id:
                if rub_id.item_id == self.object.item_id:
                    val == 0
                else:
                    val=1
        if val == 0:
            item_conv.objects.filter(pk=pk).update(item_id=self.object.item_id,valor_max=self.object.valor_max,numeracion=self.object.numeracion)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(editarItemConv, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        conv = self.kwargs['conv']
        rub = item_conv.objects.get(pk=pk)
        alex = rubro_conv.objects.get(id=rub.rubro_conv_id)  #xxxxxxxxxxxxxxxxxx
        context['rubro'] = alex
        context['conv'] = conv
        context['item'] = item_conv.objects.filter(rubro_conv_id=alex.id).order_by('numeracion')
        context['items'] = item.objects.all()
        context['item_pk'] = rub
        return context





class caracteristicaConv(CreateView):
    template_name = 'evaluacion/caracteristica_conv.html'
    model = caracteristica_conv
    fields = ('valor_max','puntaje_max','factor','puntaje_fact','caracteristica','numeracion')


    def form_valid(self, form):
        pk = self.kwargs['pk']
        rub = self.kwargs['rub']
        self.object = form.save(commit=False)
        car = caracteristica.objects.all()
        it_id=""
        val = 0
        for i in car:   
            if i.id == self.object.caracteristica_id:
                msj = "caracteristica ya existe"
                print(msj)
                it_id = i.id   
        alex = item_conv.objects.get(item_id=pk,rubro_conv_id=rub)
        self.object.caracteristica_id = it_id
        self.object.item_conv_id = alex.id
        caracteristica_c = caracteristica_conv.objects.filter(item_conv_id=alex.id)

        for car in caracteristica_c:
        	if car.caracteristica_id == self.object.caracteristica_id:
        		val=1

        if val == 0:
        	self.object.save()
        else:
        	print("caracteristica ya esiste para ese rubro")

        return HttpResponseRedirect(reverse('caracteristica-conv', kwargs={'pk': pk,'rub':rub}))

    def get_context_data(self, **kwargs):
        # Llamamos ala implementacion para traer un primer context
        context = super(caracteristicaConv, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        rub = self.kwargs['rub']
        alex = item_conv.objects.get(item_id=pk,rubro_conv_id=rub)
        rubro = rubro_conv.objects.get(pk=alex.rubro_conv_id)
        context['conv'] = rubro.convocatoria_id
        context['rubro'] =rubro
        context['item'] = alex
        context['caracteristica'] = caracteristica_conv.objects.filter(item_conv_id=alex.id).order_by('numeracion')
        context['caracteristicas'] = caracteristica.objects.all()


        return context

class eliminarCaractConv(TemplateView):
    template_name = 'evaluacion/caracteristica_conv.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['id']
        caract= caracteristica_conv.objects.get(pk=pk)
        ite = item_conv.objects.get(pk=caract.item_conv_id)
        caract.delete()
        return HttpResponseRedirect(reverse('caracteristica-conv', kwargs={'pk':ite.item_id ,'rub':ite.rubro_conv_id}))

class editarCaractConv(UpdateView):
    template_name = 'evaluacion/caracteristica_conv.html'
    model = caracteristica_conv
    fields = ['caracteristica','valor_max','puntaje_max','factor','puntaje_fact','numeracion']

    def get_success_url(self):
        pk=self.kwargs['pk']
        caract = caracteristica_conv.objects.get(pk=pk)
        ite = item_conv.objects.get(pk=caract.item_conv_id)
        return reverse('caracteristica-conv', kwargs={'pk':ite.item_id ,'rub':ite.rubro_conv_id})

    def form_valid(self, form):
        pk = self.kwargs['pk']
        val = 0
        self.object = form.save(commit=False)
        caract = caracteristica_conv.objects.get(pk=pk)
        caracteristica_c = caracteristica_conv.objects.filter(item_conv_id=caract.item_conv_id)
        for car in caracteristica_c:
            if car.caracteristica_id == self.object.caracteristica_id:
                if caract.caracteristica_id == self.object.caracteristica_id:
                    val = 0
                else:
                    val=1
        if val == 0:
            caract = caracteristica_conv.objects.filter(pk=pk).update(caracteristica_id=self.object.caracteristica_id,valor_max=self.object.valor_max,puntaje_max=self.object.puntaje_max,factor=self.object.factor,puntaje_fact=self.object.puntaje_fact,numeracion=self.object.numeracion)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(editarCaractConv, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        caract = caracteristica_conv.objects.get(pk=pk)
        ite = item_conv.objects.get(pk=caract.item_conv_id)
        rubro = rubro_conv.objects.get(pk=ite.rubro_conv_id)
        context['conv'] = rubro.convocatoria_id
        context['rubro'] =rubro
        context['item'] = ite
        context['caract'] = caract
        context['caracteristica'] = caracteristica_conv.objects.filter(item_conv_id=ite.id).order_by('numeracion')
        context['caracteristicas'] = caracteristica.objects.all()
        context['caracteristica_pk'] = caract

        return context


def importarEvaluacion(request):
    if request.method == 'POST':
		#valor = request.POST['valor']
        id_nuev_conv = request.POST['id_nuev_con']
        id_imp_conv = request.POST['id_imp_conv']
        #id_convocatoria = convocatoria.objects.get(periodo=id_nuev_conv)
        rub = rubro_conv.objects.filter(convocatoria_id=id_imp_conv)
        rub_n = rubro_conv.objects.filter(convocatoria_id=id_nuev_conv)
        if not rub_n:
            for rub in rub:
                rubro_c = rubro_conv(peso = rub.peso,
    									convocatoria_id = id_nuev_conv,
                                        numeracion = rub.numeracion,
    									rubro_id = rub.rubro_id)
                rubro_c.save()
                print(rubro_c.id)
                

                ite = item_conv.objects.filter(rubro_conv_id = rub.id)
                for it in ite:
                    item_c = item_conv( valor_max = it.valor_max,
    	    							item_id = it.item_id,
                                        numeracion = it.numeracion,
    	    							rubro_conv_id = rubro_c.id)
                    item_c.save()
                    print(item_c.id)
                    caract = caracteristica_conv.objects.filter(item_conv_id=it.id)
                    for car in caract:
                        caract_c = caracteristica_conv(valor_max = car.valor_max,
                                                        caracteristica_id = car.caracteristica_id,
                                                        item_conv_id = item_c.id,
                                                        puntaje_fact = car.puntaje_fact,
                                                        numeracion = car.numeracion,
                                                        factor = car.factor,
                                                        puntaje_max = car.puntaje_max)
                        caract_c.save()
        conv = convocatoria.objects.get(id=id_nuev_conv)
        rub = rubro_conv.objects.filter(convocatoria_id=id_nuev_conv)
    return render_to_response('evaluacion/rubro_conv.html', {'pk':id_nuev_conv,'convocatoria':conv,'rubro':rub,'val':'1'}, context_instance=RequestContext(request))
    #return HttpResponseRedirect(reverse('config-convocatoria', kwargs={'pk':id_nuev_conv,'convocatoria':conv,'rubro':rub,'val':'1'}))
