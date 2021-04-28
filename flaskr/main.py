import os
from os import abort

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_googlemaps import GoogleMaps, Map, icons
from werkzeug.utils import secure_filename

import DataBaseConnection
import randomCode
import mensaje
import time

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyAio1R0jHxwsqABXYFP-5d-nJSWFEZTojc"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

GoogleMaps(app, key="AIzaSyAio1R0jHxwsqABXYFP-5d-nJSWFEZTojc")

class car:
    def __init__(self, tag, price, model, year, lat, lng):
        self.tag  = tag
        self.price = price
        self.model = model
        self.year = year
        self.lat  = lat
        self.lng  = lng

class user:
    def __init__(self, id, bday, Dir, Mail):
        self.id = id
        self.bday = bday
        self.Dir = Dir
        self.Mail = Mail

cars = [
    car('HGW537', '50000' ,  'Chevy Spark',    '2015',   37.9045286, -122.1445772),
    car('EIO242', '100000',  'Ford Ecosport',  '2015',   37.8884474, -122.1155922),
    car('GEM247', '75000' ,  'Chevy Spark gt', '2015',   37.9093673, -122.0580063)
]
car_by_tag = {car.tag: car for car in cars}

@app.route('/', methods=['GET', 'POST'])
def redirection():
    return redirect(url_for('login'))

@app.route('/Login', methods=['GET', 'POST'])
def login():
    db = DataBaseConnection
    error = None
    if request.method == 'POST':

        correo = request.form['username']
        pssw = request.form['password']
        q = 'select password from usuario where correo = %s;'
        query = db.sql_query_var(q, (correo, ))

        if(len(query)==0):
            error = 'Invalid Credentials. Please try again.'
        elif( pssw != query[0]['password']):
            error = 'Invalid Credentials. Please try again.'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('home'))
    return render_template('Login.html', error=error)

@app.route('/SignUp', methods=['GET', 'POST'])
def register():
    db = DataBaseConnection
    error = None
    if request.method == 'POST':

        correo = request.form['Mail']
        id = request.form['Id']
        birth = request.form['Birth']
        address = request.form['Address']
        pssw = request.form['Password']

        q = 'insert into usuario (cedula, Bday, Dir, correo, password) values (%s, %s, %s, %s, %s);'
        db.DBInsert(q, (id, birth, address, correo, pssw,))
        time.sleep(1)
        code = randomCode.generarCodigo.get_random_alphanumeric_string(6)
        mensaje.enviar.codigo(correo, code)
        return redirect(url_for('confirmation'))

    return render_template('SignUp.html')

@app.route('/Confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'POST':

        codigo = request.form['Code']
        code=codigo
        if code==codigo:
            flash("tu correo ha sido confirmado")
            return redirect(url_for('login'))
        else:
            print("F")
    return render_template('confirmation.html')

@app.route('/Home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/Search', methods=['GET', 'POST'])
def Search():
    markers=[]
    for car in cars:
        markers.append({
                'lat': car.lat,
                'lng': car.lng,
                'infobox': "<h1>"+car.model+"</h1>"
                           "<p>Modelo: "+car.year+" </p>"
                           "<p2>Precio: $"+car.price+"/día </p>"
                           "<br>"
                           "<br>"
                           "<img src='/static/"+car.tag+".jpg' />",
            }
        )
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers=markers,
        fullscreen_control=True,
        style="position: absolute;left:0px;height:100%;width: 75%;padding: 0;"
    )
    return render_template("carro.html", gmap=gmap, cars=cars)

@app.route('/Rented', methods=['GET', 'POST'])
def Rented():
    markers=[]
    for car in cars:
        markers.append({
                'lat': car.lat,
                'lng': car.lng,
                'infobox': "<h1>"+car.model+"</h1>"
                           "<p>Modelo: "+car.year+" </p>"
                           "<p2>Precio: $"+car.price+"/día </p>"
                           "<br>"
                           "<br>"
                           "<img src='/static/"+car.tag+".jpg' />",
            }
        )
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers=markers,
        fullscreen_control=True,
        style="position: absolute;left:0px;height:100%;width: 75%;padding: 0;"
    )
    return render_template("carro.html", gmap=gmap, cars=cars)

@app.route("/Display/<car_code>")
def show_car(car_code):
    car = car_by_tag.get(car_code)
    if car:
        if "submit_button" in request.form:
                print("tumamaen4")

        return render_template('display.html', car=car)
    else:
        abort(404)

@app.route('/EditProfile', methods=['GET', 'POST'])
def Editprofile():
    db = DataBaseConnection
    u1 = db.sql_query("select * from usuario where numUsr = 1")
    LIuser= user(u1[0]['cedula'], u1[0]['Bday'], u1[0]['Dir'], u1[0]['correo'])
    if request.method == 'POST':
        Dir = request.form['Address']
        Mail = request.form['Mail']
        db.sql_edit("update usuario set Dir = %s, correo = %s where numUsr = 1;", (Dir, Mail, ))
        return redirect(url_for('home'))
    return render_template('Editprofile.html', user=LIuser)

@app.route('/AddCar', methods=['GET', 'POST'])
def registrarCarro():
    return render_template('registrarCarro.html')



if __name__ == "__main__":
    app.run(debug=True)