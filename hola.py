from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import DataRequired
import csv
from flask_login import LoginManager
from forms import LoginForm, AltaUsuario, AltaCliente

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

# ---------------------------------- Manejo de errores  ----------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# ---------------------------------- login del usuario  ----------------------------------
def validar(user, passw):
    with open("csv/usuarios.csv", 'r') as archivo:
        encontrado = False
        for linea in archivo:
            lista = linea.split(",")
            usuario = lista[0].strip()
            password = lista[1].strip()
            if usuario == user:
                if password == passw:
                    encontrado = True
    return encontrado

# ---------------------------------- Lectura clientes   ----------------------------------
def lerrArchivoClientes():
    with open('csv/clietes.csv', 'r') as archivo:
        reader = csv.reader(archivo)
        listaClientes = list(reader)
    return listaClientes

# ---------------------------------- ruta de origen o principal  ----------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    psw = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


# ---------------------------------- se muestra el listado de clientes  ----------------------------------
@app.route('/clientes', methods=['GET'])
def listaClientes():
    leerArchivoClientes()
    return render_template('clientes.html')

# --------------------------------------------------------------------
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# ---------------------------------- formulario de alta de usuario  ----------------------------------
@app.route('/altausuario', methods=['GET', 'POST'])
def altausuario():
    name = None
    psw = None
    pswr = None
    form = AltaUsuario()
    return render_template('altausuario.html', form=form, name=name, psw=psw, pswr=pswr)

# ---------------------------------- sobre la empresa ----------------------------------
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

# ---------------------------------- formulario de alta cliente  ----------------------------------
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

# ---------------------------------- formulario de consultasl  ----------------------------------
@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
        return render_template('consultas.html')


# ----------------------------------   ----------------------------------
