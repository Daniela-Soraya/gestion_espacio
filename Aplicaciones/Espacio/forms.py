from django import forms
from .models import Espacio, ProyectoConstruccion, Cliente, Evaluacion

from django import forms
from .models import Espacio

class EspacioForm(forms.ModelForm):
    class Meta:
        model = Espacio
        fields = ['nombre', 'ubicacion', 'capacidad', 'estado', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'file', 'data-show-upload': 'true', 'data-show-caption': 'true'}),  # Widget para subida de archivos
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        ubicacion = cleaned_data.get("ubicacion")
        capacidad = cleaned_data.get("capacidad")
        estado = cleaned_data.get("estado")

        # Validación para asegurarse de que todos los campos obligatorios estén completos
        if not nombre or not ubicacion or capacidad is None or not estado:
            raise forms.ValidationError("Todos los campos obligatorios deben ser completados.")

        # Validación de que la capacidad sea mayor a 0
        if capacidad is not None and capacidad <= 0:
            self.add_error("capacidad", "La capacidad debe ser un número positivo.")

        return cleaned_data


class ProyectoConstruccionForm(forms.ModelForm):
    class Meta:
        model = ProyectoConstruccion
        fields = ['nombre', 'descripcion', 'costo_total', 'costo_mensual', 'espacio', 'estado', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'costo_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'espacio': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'file', 'data-show-upload': 'true', 'data-show-caption': 'true'}),  # Widget para subida de archivos
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        descripcion = cleaned_data.get("descripcion")
        costo_total = cleaned_data.get("costo_total")
        costo_mensual = cleaned_data.get("costo_mensual")
        espacio = cleaned_data.get("espacio")
        estado = cleaned_data.get("estado")

        # Validación para asegurarse de que todos los campos obligatorios estén completos
        if not nombre or not descripcion or costo_total is None or costo_mensual is None or not espacio or not estado:
            raise forms.ValidationError("Todos los campos obligatorios deben ser completados.")

        # Validación de costos positivos
        if costo_total <= 0:
            self.add_error("costo_total", "El costo total debe ser un valor positivo.")
        if costo_mensual <= 0:
            self.add_error("costo_mensual", "El costo mensual debe ser un valor positivo.")

        return cleaned_data

from django.core.exceptions import ValidationError
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono del cliente'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección del cliente'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r'^[A-Za-z]+(\s[A-Za-z]+){3}$', nombre):
            raise ValidationError("El nombre debe contener solo letras y tener exactamente 4 palabras.")
        return nombre

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{10}$', telefono):
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos y solo números.")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("La dirección de correo electrónico no es válida.")
        return email

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['cliente', 'proyecto', 'comentario', 'puntuacion','notificar']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'proyecto': forms.Select(attrs={'class': 'form-select'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'puntuacion': forms.Select(choices=Evaluacion._meta.get_field('puntuacion').choices),
            'notificar': forms.Select(choices=[('Si', 'Si'), ('No', 'No')]),
        }

from .models import Sugerencia

class SugerenciaForm(forms.ModelForm):
    class Meta:
        model = Sugerencia
        fields = ['nombre', 'apellido', 'cedula', 'detalle', 'evidencia', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su cédula'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describa su sugerencia'}),
            'evidencia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}),
        }
