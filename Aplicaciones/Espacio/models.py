import re
from django.db import models
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from django.db import models

class Espacio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False, blank=False)  # Obligatorio
    ubicacion = models.CharField(max_length=255, null=False, blank=False)  # Obligatorio
    capacidad = models.IntegerField(null=False, blank=False)  # Obligatorio
    estado = models.CharField(
        max_length=50, 
        choices=[('Disponible', 'Disponible'), ('En construcción', 'En construcción'), ('Cerrado', 'Cerrado')],
        null=False, 
        blank=False  # Obligatorio
    )
    foto = models.FileField(upload_to='espacio', null=True, blank=True)  # Opcional

    def __str__(self):
        return self.nombre



class ProyectoConstruccion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=False, blank=False)  # Obligatorio
    descripcion = models.TextField(null=False, blank=False)  # Obligatorio
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)  # Obligatorio
    costo_mensual = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)  # Obligatorio
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE, null=False, blank=False)  # Obligatorio
    estado = models.CharField(
        max_length=50,
        choices=[('En progreso', 'En progreso'), ('Finalizado', 'Finalizado'), ('Cancelado', 'Cancelado')],
        null=False, 
        blank=False  # Obligatorio
    )
    foto = models.FileField(upload_to='proyecto', null=True, blank=True)  # Opcional

    def __str__(self):  
        return self.nombre


class Cliente(models.Model):    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)

    def clean(self):
        # Validación para el campo nombre (solo letras y exactamente 4 palabras)
        nombre = self.nombre
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+){3}$', nombre):
            raise ValidationError("El nombre debe contener solo letras y tener exactamente 4 palabras.")
        
        # Validación para el campo teléfono (exactamente 10 dígitos y solo números)
        telefono = self.telefono
        if not re.match(r'^\d{10}$', telefono):
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos y solo números.")
        
        # Validación de email (esto es gestionado por el EmailField, pero se puede extender si se desea más control)
        email = self.email
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("La dirección de correo electrónico no es válida.")
    
    def __str__(self):
        return self.nombre

class Evaluacion(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(ProyectoConstruccion, on_delete=models.CASCADE)
    comentario = models.TextField()
    puntuacion = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # Puntuación del 1 al 10
    NOTIFICAR_CHOICES = [('Si', 'Si'), ('No', 'No')]
    notificar = models.CharField(
        max_length=2,
        choices=NOTIFICAR_CHOICES,
        
    )

    def __str__(self):
        return f"Evaluación de {self.cliente.nombre} para {self.proyecto.nombre}"

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator

class Sugerencia(models.Model):
    nombre = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex='^[a-zA-Z]+$', message='El nombre solo puede contener letras.')
        ]
    )
    apellido = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex='^[a-zA-Z]+$', message='El apellido solo puede contener letras.')
        ]
    )
    cedula = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex='^[0-9]{10}$', message='La cédula debe tener exactamente 10 dígitos.')
        ],
        unique=True
    )
    detalle = models.TextField()  # Texto largo para la sugerencia
    evidencia = models.ImageField(upload_to='evidencias', blank=True, null=True)  # Campo para imágenes
    email = models.EmailField(validators=[EmailValidator(message='Ingrese un correo válido.')])

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"
