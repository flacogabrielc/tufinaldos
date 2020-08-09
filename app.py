import os, sys, math
from flask import Flask, render_template, session, flash, redirect, url_for, request, send_file, redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms.validators import DataRequired
import csv
from flask_login import LoginManager
from forms import LoginForm, AltaUsuario, AltaCliente, AltaProducto, ClientePais, CliRanEt, CliRanFec, ProductosMasVendidos
from forms import ClientesMasGastasron, ClientesProducto, ProductosCliente, VentaProducto
from flask_sqlalchemy import SQLAlchemy
#
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] =\
#     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)

#
# class Role(db.Model):
#     __tablename__='roles'
#     id=db.Column(db.Integer, primary_key=True)
#     name=db.Column(db.String(64), unique=True)
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
# class User(db.Model):
#     __tablename__='users'
#     id=db.Column(db.Integer, primary_key=True)
#     username=db.Column(db.String(64), unique=True, index=True)
#
#     def __repr__(self):
#         return '<User %r>' % self.username

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

def leerArchivoClientes():
    with open('csv/clientes.csv', 'r') as archivo:
        reader = csv.reader(archivo)
        listaClientes = list(reader)
    return listaClientes

#----------------------------------- funcion que da de alta un nuevo cliente -----------------------
def alta_cliente(name, age, add, cou, doc, dat, ema, pos):
    with open('csv/clientes.csv', 'a') as archivo:
        archivo.write('{},{},{},{},{},{},{},{}\n'.format(name, age, add, cou, doc, dat, ema, pos))

#----------------------------------- funcion que da de alta un nuevo usuario -----------------------
def alta_usuario(name, psw):
    with open('csv/usuarios.csv', 'a') as archivo:
        archivo.write('{},{}\n'.format(name, psw))

# --------------------------------------------------------------------------------------------------
@app.route('/login')
def login():
    return render_template('index.html', form=form, name=name )

# ---------------------------------- ruta de origen o principal  ----------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    password = None
    form = LoginForm()
    us_auth=('username' in session)

    if form.validate_on_submit():
        if(validar(form.name.data, form.password.data)):
            session ['username'] =form.name.data
            return redirect(url_for('home'))
        else:
            flash("contrasenia no valida")
            return redirect(url_for('index'))

    if us_auth:
        return redirect(url_for('home'))
    else:
        return (render_template('index.html', form=form))


# ---------------------------------- se muestra el listado de clientes  ----------------------------------
@app.route('/clientes', methods=['GET'])
def listaClientes():
    us_auth=('username' in session)
    if us_auth:
        with open('csv/clientes.csv', 'r') as archivo:
            reader=csv.reader(archivo)
            lista=list(reader)

        return render_template('clientes.html', model=lista, us_auth=us_auth)
    else:
        return redirect(url_for('index'))
    # leerArchivoClientes()

#------------------------------Cerrar sesion-------------------------------------------------------------------------
@app.route('/logout', methods=['GET'])
def logout():
    # name = None
    # password = None
    # form = LoginForm()
    if 'username' in session:
        session.pop('username')
        return render_template('logout.html')
    else:
        # return render_template('index.html', form=form, name=name)
        return redirect(url_for('index'))
# -------------------------------------------------------------------------------------------------------
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


#------------------------busqueda clientes por Pais----------------------------------------------------
@app.route('/clipais', methods=['GET', 'POST'])
def clipais():
    formulario = ClientePais()
    lista = []
    us_auth=('username' in session)

    if formulario.validate_on_submit() and us_auth:
        with open('csv/clientes.csv', 'r') as archivo:
            reader = csv.reader(archivo)
            for row in reader:
                if row[3].lower() == formulario.pais.data.lower():
                    lista.append(row)
    return render_template('country.html', form = formulario, lista = lista)

# @app.route('/about', methods=['GET', 'POST'])
# def about():
#     return render_template('about.html')

#------------------------busqueda clientes por Rango etario----------------------------------------------------
# @app.route('/cliedad', methods=['GET', 'POST'])
# def cliedad():
#     formulario = CliRanEt()
#     return render_template('cliedad.html', form=formulario)

@app.route('/cliedad', methods=['GET', 'POST'])
def cliedad():
    formulario = CliRanEt()
    lista = []
    us_auth=('username' in session)

    #leer desde fila + 1 en el csv
    if formulario.validate_on_submit() and us_auth:
        with open('csv/clientes.csv', 'r') as archivo:
            reader = csv.reader(archivo)
            next(reader)
            # self.age_ini = edadini
            # self.age_fin = edadfin
            # edad = int(row[1])
            for row in reader:
                # edad = int(row[1])
                if (int(row[1])  >= int(formulario.age_ini.data)) and (int(row[1]) <= int(formulario.age_fin.data)):
                    lista.append(row)

    return render_template('age.html', form = formulario, lista = lista)

#
# class CliRanEt(FlaskForm):
#     age_ini = IntegerField('Edad menor')
#     age_fin = IntegerField('Edad mayor')
#     submit = SubmitField('Buscar')




#------------------------busqueda clientes por fecha alta----------------------------------------------------
@app.route('/cliealta', methods=['GET', 'POST'])
def cliealta():
    formulario = CliRanFec()
    return render_template('cliealta.html', form=formulario)

# ---------------------------------- formulario de alta de usuario  ----------------------------------
@app.route('/altausuario', methods=['GET', 'POST'])
def alta():
    formulario = AltaUsuario()
    if formulario.validate_on_submit():
            if formulario.psw.data == formulario.pswr.data:
                alta_usuario(formulario.name.data, formulario.psw.data)
                return render_template('registrok.html', form=formulario)
            else:
                 flash('Las contrasenias no coinciden')
    return render_template('altausuario.html', form=formulario)
    # else:
    #     if formulario.psw.data != formulario.pswr.data:
    #         flash('Las contrasenias no coinciden')
    #     return render_template('altausuario.html', form=formulario)

# ---------------------------------- sobre la empresa ----------------------------------
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# ---------------------------------- formulario de alta cliente  ----------------------------------
@app.route('/altacliente', methods=['GET', 'POST'])
def altacliente():
    formulario = AltaCliente()
    if formulario.validate_on_submit():
        alta_cliente(formulario.name.data, formulario.age.data, formulario.add.data, formulario.cou.data, formulario.doc.data, formulario.dat.data, formulario.ema.data, formulario.pos.data)
        return render_template('altacliente.html', form=formulario)

        # formulario.name.data=''
        # formulario=os.system.clear
    else:
        flash('Ingrese todos los campos')
    return render_template('altacliente.html',form=formulario)
# ---------------------------------- Listado de productos  ----------------------------------
@app.route('/productos', methods=['GET', 'POST'])
def productos():
        us_auth=('username' in session)
        if us_auth:
            with open('csv/productos.csv', 'r') as archivo:
                reader=csv.reader(archivo)
                lista=list(reader)

            return render_template('productos.html', model=lista, us_auth=us_auth)
        else:
            return redirect(url_for('index'))

# ---------------------------------- funcion que da de alta nuevos  de productos  ----------------------------------
def alta_producto(cod, desc, precio, stock):
    with open('csv/productos.csv', 'a') as archivo:
        archivo.write('{},{},{},{}\n'.format(cod, desc, precio, stock))


# ---------------------------------- Alta nuevos  de productos  ----------------------------------
@app.route('/altaproducto', methods=['GET', 'POST'])
def altaproducto():
    formulario = AltaProducto()
    if formulario.validate_on_submit():
        alta_producto(formulario.cod.data, formulario.desc.data, formulario.precio.data, formulario.stock.data)
        return render_template('productos.html')
    else:
        flash('Ingrese todos los campos')
    return render_template('altaproducto.html',form=formulario)

#-------------------------------- Muestra los n productos mas vendidos--------------------------
@app.route('/prodmasvendido', methods =['GET', 'POST'])
def prodmasvendido():
    formulario = ProductosMasVendidos()
    return render_template('prodmasvendido.html', form=formulario)

# ----------------------------------------------
@app.route('/clientesmasgasto', methods= ['GET', 'POST'])
def clientesmasgasto():
    formulario = ClientesMasGastasron()
    return render_template('clientesmasgasto.html', form=formulario)

# ----------------------------------------------
@app.route('/clientesporprod', methods= ['GET', 'POST'])
def clientesporprod():
    formulario = ClientesProducto()
    return render_template('clientesporprod.html', form=formulario)

# ----------------------------------------------
@app.route('/prodporcliente', methods= ['GET', 'POST'])
def prodporcliente():
    formulario = ProductosCliente()
    return render_template('prodporcliente.html', form=formulario)



@app.route('/ventaproducto', methods= ['GET', 'POST'])
def ventaproducto():
    formulario= VentaProducto()
    return render_template('ventaproducto.html', form=formulario)


# ---------------------------------- busqueda clientes pais  ----------------------------------
# @app.route('/country')

# ---------------------------------- formulario de consultasl  ----------------------------------
# @app.route('/consultas', methods=['GET', 'POST'])
# def consultas():
#         return render_template('consultas.html')
#

# --------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
