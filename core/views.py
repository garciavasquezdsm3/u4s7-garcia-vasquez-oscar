from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Servicio
from .forms import ServicioForm


def inicio(request):
    info_bd = connection.settings_dict
    contexto = {
        'motor': info_bd['ENGINE'],
        'host': info_bd['HOST'],
    }
    return render(request, 'core/inicio.html', contexto)


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, '¡Cuenta creada con éxito!')
            return redirect('servicios')
    else:
        form = UserCreationForm()
    return render(request, 'core/registro.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bienvenido de nuevo, {usuario.username}')
            return redirect('servicios')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')


@login_required
def servicios(request):
    lista_servicios = Servicio.objects.filter(propietario=request.user).order_by('-creado_en', '-id')
    query = request.GET.get('q', '').strip()
    if query:
        lista_servicios = lista_servicios.filter(titulo__icontains=query)
    
    paginator = Paginator(lista_servicios, 5)
    numero_pagina = request.GET.get('page')
    pagina = paginator.get_page(numero_pagina)
    
    return render(request, 'core/servicios.html', {'servicios': pagina, 'query': query})


@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.propietario = request.user
            nuevo.save()
            messages.success(request, 'Servicio creado exitosamente.')
            return redirect('servicios')
    else:
        form = ServicioForm()
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Nuevo servicio'})


@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado exitosamente.')
            return redirect('servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})


@login_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk, propietario=request.user)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado exitosamente.')
        return redirect('servicios')
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})
