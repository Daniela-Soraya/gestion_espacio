from django.shortcuts import render, redirect, get_object_or_404
from .models import Espacio, ProyectoConstruccion, Cliente, Evaluacion,Sugerencia
from .forms import EspacioForm, ProyectoConstruccionForm, ClienteForm, EvaluacionForm,SugerenciaForm

# Vista para listar todos los espacios
def lista_espacios(request):
    espacios = Espacio.objects.all()
    return render(request, 'espacios/lista_espacios.html', {'espacios': espacios})

# Vista para crear un espacio
def crear_espacio(request):
    if request.method == 'POST':
        form = EspacioForm(request.POST, request.FILES)  # Agregamos request.FILES para manejar archivos
        if form.is_valid():
            form.save()
            return redirect('lista_espacios')
    else:
        form = EspacioForm()
    return render(request, 'espacios/crear_espacio.html', {'form': form})

def editar_espacio(request, espacio_id):
    espacio = get_object_or_404(Espacio, id=espacio_id)
    if request.method == 'POST':
        form = EspacioForm(request.POST, request.FILES, instance=espacio)  # Se incluye request.FILES
        if form.is_valid():
            form.save()
            return redirect('lista_espacios')
    else:
        form = EspacioForm(instance=espacio)

    return render(request, 'espacios/editar_espacio.html', {'form': form,'espacio': espacio})

# Vista para eliminar un espacio
def eliminar_espacio(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    if request.method == 'POST':
        espacio.delete()
        return redirect('lista_espacios')
    return render(request, 'espacios/eliminar_espacio.html', {'espacio': espacio})

# Vista para listar todos los proyectos
def lista_proyectos(request):
    proyectos = ProyectoConstruccion.objects.all()
    return render(request, 'proyectos/lista_proyectos.html', {'proyectos': proyectos})

# Vista para crear un proyecto de construcción
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoConstruccionForm(request.POST, request.FILES)  # Se incluye request.FILES
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoConstruccionForm()
    
    return render(request, 'proyectos/crear_proyecto.html', {'form': form})

# Vista para editar un proyecto de construcción
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(ProyectoConstruccion, id=proyecto_id)
    
    if request.method == 'POST':
        form = ProyectoConstruccionForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('lista_proyectos')
    else:
        form = ProyectoConstruccionForm(instance=proyecto)

    # 🔹 PASAR EL PROYECTO AL CONTEXTO
    return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyecto': proyecto})


# Vista para eliminar un proyecto de construcción
def eliminar_proyecto(request, pk):
    proyecto = get_object_or_404(ProyectoConstruccion, pk=pk)
    if request.method == 'POST':
        proyecto.delete()
        return redirect('lista_proyectos')
    return render(request, 'proyectos/eliminar_proyecto.html', {'proyecto': proyecto})

# Vista para listar todos los clientes
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

# Vista para crear un cliente
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

# Vista para editar un cliente
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar_cliente.html', {'form': form})

# Vista para eliminar un cliente
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

# Vista para listar todas las evaluaciones
def lista_evaluaciones(request):
    evaluaciones = Evaluacion.objects.all()
    return render(request, 'evaluaciones/lista_evaluaciones.html', {'evaluaciones': evaluaciones})

# Vista para crear una evaluación

def crear_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            # Guardar la evaluación
            evaluacion = form.save()

            # Obtener la opción seleccionada en el campo 'notificar_cliente'
            notificar = form.cleaned_data.get('notificar')

            if notificar == 'Si':
                # Obtener el cliente seleccionado (suponiendo que se selecciona un cliente)
                cliente = Cliente.objects.get(id=request.POST.get('cliente'))  # Aquí asumo que 'cliente_id' es el campo de selección

                # Enviar el correo al cliente
                send_mail(
                    subject="Notificación de Evaluación",
                    message=f"Se ha registrado una nueva evaluación: {evaluacion}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[cliente.email],
                )

            # Redirigir después de guardar y enviar el correo
            return redirect('lista_evaluaciones')
    else:
        form = EvaluacionForm()

    return render(request, 'evaluaciones/crear_evaluacion.html', {'form': form})

# Vista para editar una evaluación
def editar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            return redirect('lista_evaluaciones')
    else:
        form = EvaluacionForm(instance=evaluacion)
    return render(request, 'evaluaciones/editar_evaluacion.html', {'form': form})

# Vista para eliminar una evaluación
def eliminar_evaluacion(request, pk):
    evaluacion = get_object_or_404(Evaluacion, pk=pk)
    if request.method == 'POST':
        evaluacion.delete()
        return redirect('lista_evaluaciones')
    return render(request, 'evaluaciones/eliminar_evaluacion.html', {'evaluacion': evaluacion})

#INICIO
def inicio(request):
    return render(request, 'inicio1.html')


#Sugerencia

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Sugerencia
from .forms import SugerenciaForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SugerenciaForm

def crear_sugerencia(request):
    if request.method == 'POST':
        form = SugerenciaForm(request.POST, request.FILES)
        if form.is_valid():
            sugerencia = form.save()

            # Datos del correo
            asunto = "Nueva Sugerencia Registrada"
            mensaje = (
                f"Hola {sugerencia.nombre} {sugerencia.apellido},\n\n"
                "Gracias por enviar tu sugerencia. Aquí están los detalles de tu registro:\n\n"
                f"Nombre: {sugerencia.nombre}\n"
                f"Apellido: {sugerencia.apellido}\n"
                f"Cédula: {sugerencia.cedula}\n"
                f"Detalle: {sugerencia.detalle}\n\n"
                "Nuestro equipo revisará tu sugerencia y te contactará si es necesario.\n\n"
                "Saludos,\nEl equipo de soporte."
            )
            remitente = settings.EMAIL_HOST_USER
            destinatario = [sugerencia.email]

            # Crear correo con adjunto
            email = EmailMessage(asunto, mensaje, remitente, destinatario)

            # Adjuntar imagen si existe
            if 'evidencia' in request.FILES:
                evidencia = request.FILES['evidencia']
                email.attach(evidencia.name, evidencia.read(), evidencia.content_type)

            # Enviar el correo
            email.send(fail_silently=False)

            return redirect('lista_sugerencias')  # Redirige a la lista de sugerencias después de guardar
    else:
        form = SugerenciaForm()
    
    return render(request, 'sugerencias/crear_sugerencia.html', {'form': form})

def lista_sugerencias(request):
    sugerencias = Sugerencia.objects.all()
    return render(request, 'sugerencias/lista_sugerencias.html', {'sugerencias': sugerencias})
