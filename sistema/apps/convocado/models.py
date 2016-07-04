from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.evaluacion.models import convocatoria,caracteristica_conv,item_conv
# Create your models here.


class ubigeo(models.Model):
	codDpto = models.CharField(max_length=2)
	codProv = models.CharField(max_length=2)
	codDist = models.CharField(max_length=2)
	nombre = models.CharField(max_length=40)
		


class perfil(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	nombre = models.CharField(max_length=50, blank=True )
	ap_pat = models.CharField(max_length=30, blank=True)
	ap_mat = models.CharField(max_length=30, blank=True)
	foto = models.ImageField(upload_to='foto_perfil/', blank=True)
	dni  = models.CharField(max_length=8 , unique=True)
	fecha_nac = models.DateField(blank=True , null=True)
	estado_civil = models.CharField(max_length=1, blank=True)
	sexo = models.CharField(max_length=1, blank=True)
	direccion = models.CharField(max_length=50, blank=True)
	ubigeo = models.CharField(max_length=6, blank=True , null=True)
	direccion_act = models.CharField(max_length=50, blank=True)
	telefono = models.CharField(max_length=10, blank=True)
	celular = models.CharField(max_length=10, blank=True)
	email = models.EmailField(max_length=50, blank=True,unique=True)
	ubigeo_act = models.CharField(max_length=6)
	
	def __str__(self):
		return self.nombre

		

class convocado_convocatoria(models.Model):
	puntaje = models.IntegerField(blank=True , null=True)
	estado_conv = models.CharField(max_length=1)
	convocado = models.ForeignKey(perfil)
	convocatoria = models.ForeignKey(convocatoria)

class tipo_evidencia(models.Model):
	nombre = models.CharField(max_length=20)
	estado = models.CharField(max_length=1)

	def __str__(self):
		return self.nombre

def generate_filename(self, filename):
    url = "evidencia/%s/%s" % ("alex", filename)
    return url

class evidencia_convocatoria(models.Model):

	evidencia = models.ImageField(upload_to=generate_filename)
	numero_evidencia = models.CharField(max_length=20,blank=True , null=True)
	cargo_rol = models.CharField(max_length=60)
	tiempo = models.IntegerField(blank=True , null=True)
	puntaje_obtenido = models.DecimalField(max_digits=5,decimal_places=2,blank=True , null=True)
	puntaje_calculado = models.DecimalField(max_digits=5,decimal_places=2,blank=True , null=True)
	estado_eval =  models.CharField(max_length=1)
	item_conv = models.ForeignKey(item_conv)
	tipo_evidencia = models.ForeignKey(tipo_evidencia)
	convocado_convocatoria = models.ForeignKey(convocado_convocatoria)
	caracteristica_conv = models.ForeignKey(caracteristica_conv)

	def __str__(self):
		return self.cargo_rol