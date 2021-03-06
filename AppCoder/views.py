
from msilib.schema import Class
from django.http import HttpResponse
from AppCoder.models import Avatar, Club, Jugadora
from django.shortcuts import render
from django.template import Template
from AppCoder.forms import ClubFormulario, JugadoraForm, RegistroFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

def register(request):
    if request.method == 'POST':
    
        form = RegistroFormulario(request.POST) #LEER LA DATA DEL FORMULARIO DE INICIO DE SESION

        if form.is_valid():
            user = form.cleaned_data['username']
            form.save()

            return render(request, 'AppCoder/inicio.html', {'mensaje':"Usuario Creado"})
    else:
        form = RegistroFormulario()
    
    return render(request, 'AppCoder/registro.html', {'form': form})

def editarUsuario(request):

    usuario = request.user 

    if request.method == 'POST':

        miFormulario1 = RegistroFormulario(request.POST)
        
        if miFormulario1.is_valid():

            info3 = miFormulario1.cleaned_data

            usuario.username = info3['username']
            usuario.email = info3['email']
            usuario.password1 = info3['password1']
            usuario.password2 = info3['password2']
            usuario.save()

            return render(request, 'AppCoder/inicio.html')
    else:
        miFormulario1 = RegistroFormulario(initial={'username':usuario.username, 'email':usuario.email})
    
    return render(request, 'AppCoder/editarUsuario.html',{'miFormulario1':miFormulario1, 'usuario':usuario.username})


def login_request(request):

    if request.method == 'POST': #al presionar el boton iniciar sesion
        
        form = AuthenticationForm(request, data=request.POST) #LEER LA DATA DEL FORMULARIO DE INICIO DE SESION

        if form.is_valid():

            usuario= form.cleaned_data.get('username') #leer el usuario ingresado
            contra= form.cleaned_data.get('password')

            user=authenticate(username=usuario, password=contra) #buscar al usuario con los datos ingresados

            if user:  #si ha encontrado un usuario con esos datos

                login(request, user) #hacemos login
                #mostramos la pg de inicio con un mensaje de bienvenida
                return render(request, 'AppCoder/inicio.html', {'mensaje':f"Bienvenido {user}"})
            
        else: # si el formulario no es valido(no encuentra el usuario)
                #mostramos la pag de inicio junto a un mensaje de error
            return render(request, 'AppCoder/inicio.html', {'mensaje':"Error. Datos incorrectos"})
    
    else:
        
        form = AuthenticationForm() #mostrar el formulario

    return render(request, "AppCoder/login.html", {'form':form}) #vincular la vista con la plantilla de html


def club(request):

    if request.method == 'POST':

        miFormulario = ClubFormulario(request.POST) #aca llega la info del formulario

        print(miFormulario) #muestra en terminal

        if miFormulario.is_valid():        #comprobar si la info es valida

            informacion = miFormulario.cleaned_data

            club = Club(nombre=informacion['nombre'], division=informacion['division'], deporte=informacion['deporte']) #creo el curso con la info recivida

            club.save()

            return render(request, 'AppCoder/inicio.html') #una vez guardado mostramos la plantilla de inicio

    else:
        miFormulario = ClubFormulario()  #me muestra un formulario vacio


    return render(request, 'AppCoder/clubes/club.html', {'miFormulario':miFormulario})



class ClubList(LoginRequiredMixin, ListView):
    model = Club
    template_name = 'AppCoder/clubes/clubes_list.html'

class ClubDetalle(DetailView):
    model = Club
    template_name= 'AppCoder/clubes/club_detalle.html'

class ClubCreacion(CreateView):
    model = Club
    template_name= 'AppCoder/clubes/club_form.html'
    success_url= '/AppCoder/club/lista'
    fields= ['nombre', 'division', 'deporte']

class ClubUpdate(UpdateView):
    model = Club
    template_name= 'AppCoder/clubes/club_form.html'
    success_url= '/AppCoder/club/lista'
    fields= ['nombre', 'division', 'deporte']

class ClubDelete(DeleteView):
    model = Club
    template_name= 'AppCoder/clubes/club_confirm_delete.html'
    success_url= '/AppCoder/club/lista'

def jugadora(request):
  
     if request.method == 'POST':

        miFormulario = JugadoraForm(request.POST) 

        print(miFormulario) 

        if miFormulario.is_valid():        

            info1 = miFormulario.cleaned_data

            jugadora = Jugadora(nombre=info1['nombre'], apellido=info1['apellido'], mail=info1['mail'], club=info1['club'])  

            jugadora.save()

            return render(request, 'AppCoder/inicio.html') 

     else:
        miFormulario = JugadoraForm() 


     return render(request, 'AppCoder/jugadoras/jugadora.html', {'miFormulario': miFormulario})


class JugadoraList(LoginRequiredMixin, ListView):
    model = Jugadora
    template_name = 'AppCoder/jugadoras/jugadora_list.html'

class JugadoraDetalle(DetailView):
    model = Jugadora
    template_name= 'AppCoder/jugadoras/jugadora_detalle.html'

class JugadoraCreacion(CreateView):
    model = Jugadora
    template_name= 'AppCoder/jugadoras/jugadora_form.html'
    success_url= '/AppCoder/jugadora/lista'
    fields= ['nombre', 'apellido', 'mail', 'club']

class JugadoraUpdate(UpdateView):
    model = Jugadora
    template_name= 'AppCoder/jugadoras/jugadora_form.html'
    success_url= '/AppCoder/jugadora/lista'
    fields= ['nombre', 'apellido', 'mail', 'club']

class JugadoraDelete(DeleteView):
    model = Jugadora
    template_name= 'AppCoder/jugadoras/jugadora_form.html'
    success_url= '/AppCoder/jugadora/lista'
    fields= ['nombre', 'apellido','mail', 'club']


@login_required  
def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    mensaje = 'Pagina oficial del Torneo Metropolitano de Hockey'
    return render(request, 'AppCoder/inicio.html',{'mensaje': mensaje, 'url':avatares[0].imagen.url})

def buscar(request):

    if request.GET['division']:

        division= request.GET['division']
        #curso = Curso.objects.filter(camada__icontains=camada) #icontains significa que el numero que buscamos esta dentro del numero de camada
        club = Club.objects.filter(division__iexact=division)

        return render(request, 'AppCoder/resultadosBusqueda.html', {'club':club, 'division':division})

    else:
        respuesta= 'No enviaste datos'

    return HttpResponse(respuesta)
  
def torneo(request):
     return render(request, 'AppCoder/torneo.html')

def acercaDeMi(request):
    return render(request, 'AppCoder/aboutMe.html' )
