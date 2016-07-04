from django.db import models
from apps.evaluacion.models import convocatoria, caracteristica_conv
from apps.convocado.models import convocado
# Create your models here.

class tipo_evidencia(models.Model):
	nombre = models.CharField(max_length=20)
	estado = models.CharField(max_length=1)

	def __str__(self):
		return self.nombre

class convocado_conv(models.Model):
	puntaje = models.IntegerField()
	convocado = models.ForeignKey(convocado)
	convocatoria = models.ForeignKey(convocatoria)

	def __str__(self):
		return self.convocado	

		

class convocado_evid(models.Model):
	evidencia = models.CharField(max_length=30)
	numero_evid = models.CharField(max_length=15 , blank=True , null=True)
	cargo_rol = models.CharField(max_length=60)
	valor = models.IntegerField()
	cantidad = models.IntegerField()
	puntaje = models.IntegerField()
	tipo_evidencia = models.ForeignKey(tipo_evidencia)
	caracteristica_conv = models.ForeignKey(caracteristica_conv)
	convocatoria = models.ForeignKey(convocatoria)

	def __str__(self):
		return self.convocatoria


		