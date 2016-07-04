from django.shortcuts import render

# Create your views here.
def menu(request):
	return render(request,"index/menu.html",{})

def index(request):
	return render(request,"index/listar.html",{})

def registro(request):
	return render(request,"index/formulario.html",{})