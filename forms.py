from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask import Flask
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class LoginForm(FlaskForm):
    name = StringField('Cual es tu Usuario', validators=[DataRequired(message="Por favor ingres el Usuario")])
    password = PasswordField('Ingrese Password', validators=[DataRequired(message="Ingrese su contrasenia")])
    submit = SubmitField('Ingresar')

class AltaUsuario(FlaskForm):
    name = StringField('Cual es tu Usuario', validators=[DataRequired(message="Por favor ingres el Usuario")])
    psw = PasswordField('Ingrese Password', validators=[DataRequired(message="Ingrese su contrasenia")])
    pswr = PasswordField('Repita Password', validators=[DataRequired(message="Repita la contrasenia")])
    submit = SubmitField('Aceptar')

class AltaCliente(FlaskForm):
    name = StringField('Nombre del Cliente', validators=[DataRequired(message="Ingrese su Nombre")])
    age = IntegerField('Edad', validators=[DataRequired(message="Ingrese su edad")])
    add = StringField('Direccion', validators=[DataRequired(message="Ingrese la direccion")])
    cou = StringField('Pais', validators=[DataRequired(message="Ingrese su Pais")])
    doc = IntegerField('Documento sin puntos ni guiones', validators=[DataRequired(message="Ingrese su Documento")])
    dat = DateField('Ingrese su fecha de alta',validators=[DataRequired(message="Ingrese la fecha de alta")])
    ema = EmailField('Ingrese su correo electronico', validators=[DataRequired(message="Ingrese el correo electronico")])
    pos = StringField('Ingrese la posicion de Trabajo', validators=[DataRequired(message="Ingrese su posicion de trabajo")])
    submit = SubmitField('Aceptar')

class AltaProducto(FlaskForm):
    cod = StringField('Codigo del producto', validators=[DataRequired(message="Ingrese el codigo")])
    desc = StringField('Descripcion del producto', validators=[DataRequired(message="Ingrese la descripcion")])
    precio = DecimalField('Ingrese el precio del producto', validators=[DataRequired(message="Ingrese el precio del producto")])
    stock = IntegerField('Ingrese el stock del producto', validators=[DataRequired(message="Ingrese el stock disponible")])
    submit = SubmitField('Aceptar')
    
