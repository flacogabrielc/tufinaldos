from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class LoginForm(FlaskForm):
    name = StringField('Cual es tu Usuario', validators=[DataRequired(message="Por favor ingres el Usuario")])
    psw = PasswordField('Ingrese Password', validators=[DataRequired(message="Ingrese su contrasenia")])
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    psw = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    return render_template('clientes.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/altausuario', methods=['GET', 'POST'])
def altausuario():
    name = None
    psw = None
    pswr = None
    form = AltaUsuario()
    return render_template('altausuario.html', form=form, name=name, psw=psw, pswr=pswr)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/altacliente', methods=['GET', 'POST'])
def altacliente():
    name = None
    age = None
    add = None
    cou = None
    doc = None
    dat = None
    ema = None
    pos = None
    form=AltaCliente()
    return render_template('altacliente.html',form=form, name=name, age=age, add=add, cou=cou, doc=doc, dat=dat, ema=ema, pos=pos)

@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
        return render_template('consultas.html')
