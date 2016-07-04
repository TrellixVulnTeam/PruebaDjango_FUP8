from django.db import models

# Create your models here.


class rubro(models.Model):
	#nombre = models.CharField(max_length=60, unique=True, blank=True , null=True)
	nombre = models.CharField(max_length=60, unique=True)
	estado = models.CharField(max_length=1)

	def __str__(self):
		return self.nombre


class item(models.Model):
	nombre = models.CharField(max_length=120, unique=True)
	estado = models.CharField(max_length=1)

	def __str__(self):
		return self.nombre

class caracteristica(models.Model):
	nombre = models.CharField(max_length=250, unique=True)
	estado = models.CharField(max_length=1)

	def __str__(self):
		return self.nombre

class convocatoria(models.Model):
	periodo = models.CharField(max_length=10, unique=True)
	estado =  models.CharField(max_length=1)
	fecha_inicio = models.DateTimeField()
	fecha_fin = models.DateTimeField()

	def __str__(self):
		return self.periodo

class rubro_conv(models.Model):
	peso = models.IntegerField()
	numeracion = models.IntegerField()
	rubro = models.ForeignKey(rubro)
	convocatoria = models.ForeignKey(convocatoria)

class item_conv(models.Model):
	valor_max = models.IntegerField()
	numeracion = models.IntegerField()
	item = models.ForeignKey(item)
	rubro_conv = models.ForeignKey(rubro_conv)

class caracteristica_conv(models.Model):
	valor_max = models.IntegerField(blank=True , null=True)
	puntaje_max = models.IntegerField(blank=True , null=True)
	factor = models.CharField(max_length=20,blank=True , null=True)
	puntaje_fact = models.DecimalField(max_digits=5,decimal_places=2,blank=True , null=True)
	numeracion = models.IntegerField()
	caracteristica = models.ForeignKey(caracteristica)
	item_conv = models.ForeignKey(item_conv)

	def __str__(self):

		return self.caracteristica

class det_caracteristica_conv(models.Model):
	nombre = models.IntegerField(blank=True , null=True)
	puntaje = models.DecimalField(max_digits=5,decimal_places=2,blank=True , null=True)
	factor = models.CharField(max_length=20,blank=True , null=True)
	caracteristica = models.ForeignKey(caracteristica_conv)
		
		

		