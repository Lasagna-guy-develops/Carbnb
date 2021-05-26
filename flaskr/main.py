import os
from os import abort
from pprint import pprint

from flask import Flask, send_from_directory
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from flask_googlemaps import GoogleMaps, Map, icons
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

import DataBaseConnection
import randomCode
import mensaje
import time

from flaskr import dbHandler

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['GOOGLEMAPS_KEY'] = "AIzaSyAio1R0jHxwsqABXYFP-5d-nJSWFEZTojc"
GoogleMaps(app, key="AIzaSyAio1R0jHxwsqABXYFP-5d-nJSWFEZTojc")
socketio = SocketIO(app)

class car:
    def __init__(self, tag, price, model, year):
        self.tag  = tag
        self.price = price
        self.model = model
        self.year = year

class User:
    authentication = False
    def __init__(self, Nombre, Apellido, Cedula, Correo, Bday, Dir):
        self.name = Nombre
        self.lname = Apellido
        self.id = Cedula
        self.bday = Bday
        self.Dir = Dir
        self.Mail = Correo

class rent:
    def __init__(self, start, end, price, cid, oid, rid, tag):
        self.inicio = start
        self.final = end
        self.precio = price
        self.carro = cid
        self.dueño = oid
        self.rentador = rid
        self.placa = tag

class u:
    def __init__(self, name):
        self.name = name

def no_session():
    if "id" in session:
        print("you're cool man")
    else:
        return redirect(url_for("login"))

@app.route('/', methods=['GET', 'POST'])
def redirection():
    if "id" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for("login"))


# Cosas del Login ..........................................................

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
            info = db.sql_query_var('select Id, Nombre, Apellido from usuario where correo = %s', (correo, ))
            session["id"] = info[0]['Id']
            session["name"] = info[0]['Nombre']+ " " + info[0]['Apellido']
            return redirect(url_for('home'))
    return render_template('Login.html', error=error)

@app.route('/Logout', methods=['GET', 'POST'])
def logout():
    session.pop("id", None)
    return redirect(url_for("login"))

@app.route('/SignUp', methods=['GET', 'POST'])
def register():
    db = DataBaseConnection
    error = None
    if request.method == 'POST':

        correo = request.form['Mail']
        name = request.form['Name']
        lname = request.form['LName']
        id = request.form['Id']
        birth = request.form['Birth']
        address = request.form['Address']
        pssw = request.form['Password']

        q = 'insert into usuario (Nombre, Apellido, Cedula, Password, Correo, Bday, Dir) values (%s, %s, %s, %s, %s, %s, %s);'
        db.DBInsert(q, (name, lname, id, pssw, correo, birth, address, ))
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


# Cosas de Alquilar ............................................................

@app.route('/Home', methods=['GET', 'POST'])
def home():
    no_session()
    return render_template('home.html')

@app.route('/Search', methods=['GET', 'POST'])
def Search():
    no_session()
    db = DataBaseConnection

    if request.method == "GET":
        from random import uniform
        x, y = uniform(-180, 180), uniform(-90, 90)

        markers=[]
        carros = db.sql_query('select * from carro;')
        cars=[]
        for car1 in carros:
            cars.append(car(car1['Placa'], car1['Precio'], car1['Marca'], car1['Modelo']))
            x, y = uniform(-180, 180), uniform(-90, 90)
            markers.append({
                    'lat': y,
                    'lng': x,
                    'infobox': "<h1>"+car1['Marca']+"</h1>"
                               "<p>Modelo: "+car1['Modelo']+" </p>"
                               "<p2>Precio: $"+car1['Precio']+"/día </p>"
                               "<br>"
                               "<br>"
                               "<img src='/static/cars/"+car1['Placa']+"/fotos/0.png' width='128' height='128'>",
                }
            )
        print(markers)
        gmap = Map(
            identifier="gmap",
            varname="gmap",
            lat=37.4419,
            lng=-122.1419,
            markers=markers,
            fullscreen_control=True,
            style="position: absolute;left:0px;height:100%;width: 75%;padding: 0;"
        )

    elif request.method == "POST":
        from random import uniform
        x, y = uniform(-180, 180), uniform(-90, 90)

        markers=[]
        marcaReq = request.form['marca']
        modeloReq = request.form['modelo']
        precioReq = request.form['precio']

        myQuery =""" SELECT *
        FROM carro WHERE
         Marca Like "%"+%s+"%" AND
         Modelo Like "%"+%s+"%" AND
         Precio Like "%"+%s+"%";"""


        carros = db.sql_query_var(myQuery, (marcaReq, modeloReq,precioReq))
        cars=[]
        for car1 in carros:
            cars.append(car(car1['Placa'], car1['Precio'], car1['Marca'], car1['Modelo']))
            x, y = uniform(-180, 180), uniform(-90, 90)
            markers.append({
                    'lat': y,
                    'lng': x,
                    'infobox': "<h1>"+car1['Marca']+"</h1>"
                               "<p>Modelo: "+car1['Modelo']+" </p>"
                               "<p2>Precio: $"+car1['Precio']+"/día </p>"
                               "<br>"
                               "<br>"
                               "<img src='/static/cars/"+car1['Placa']+"/fotos/0.png' width='128' height='128'>",
                }
            )
        print(markers)
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

@app.route("/Display/<car_code>", methods=['GET', 'POST'])
def show_car(car_code):
    no_session()
    db = DataBaseConnection
    q = db.sql_query_var('select * from carro where Placa = %s;', (car_code, ))
    carD = car(q[0]['Placa'], q[0]['Precio'], q[0]['Marca'], q[0]['Modelo'])
    if carD:
        if "submit_button" in request.form:
                print("tumamaen4")

        return render_template('display.html', car=carD)
    else:
        abort(404)

@app.route('/AddCar', methods=['GET', 'POST'])
def registrarCarro():
    no_session()
    db = DataBaseConnection

    if request.method == 'POST':
        tag = request.form['Placa'].upper()
        model = request.form['Modelo']
        year = request.form['Año']
        price = request.form['Precio']

        db.DBInsert('insert into carro (Placa, Marca, Modelo, Id_user, Precio) values (%s, %s, %s, %s, %s);', (tag, model, year, session["id"], price, ))

        fotos = request.files.getlist('Fotos[]')
        seguro = request.files['Seguro']
        soat = request.files['Seguro']
        matricula = request.files['Seguro']
        tecnicoM = request.files['Seguro']

        path = 'static/cars/' + tag
        os.makedirs(os.path.join(os.getcwd(), path))
        path = 'static/cars/' + tag + '/fotos'
        os.makedirs(os.path.join(os.getcwd(), path))

        i=0
        for foto in fotos:
            extension = foto.filename.split(".")
            path = 'static/cars/' + tag + '/fotos/' + str(i) + "." +extension[1]
            foto.save(path)
            i=i+1

        if seguro.filename != '':
            path = 'static/cars/' + tag + '/seguro.pdf'
            seguro.save(path)
        if soat.filename != '':
            path = 'static/cars/' + tag + '/soat.pdf'
            soat.save(path)
        if matricula.filename != '':
            path = 'static/cars/' + tag + '/matricula.pdf'
            matricula.save(path)
        if tecnicoM.filename != '':
            path = 'static/cars/' + tag + '/seguro.pdf'
            tecnicoM.save(path)

    # print(os.getcwd())
    # os.makedirs(os.path.join(os.getcwd(), 'static/car_images/HGW537'))

    return render_template('registrarCarro.html')

@app.route("/MyRent", methods=['GET', 'POST'])
def show_rent():
    no_session()
    db = DataBaseConnection
    if db.sql_query_var('select count(*) from prestamo where Id_rentb = %s and Fecha_f between CURRENT_DATE() and "2040-07-05";', (session['id'],))[0]['count(*)']>0:
        q = db.sql_query_var('select * from prestamo where Id_rentb = %s;', (session['id'], ))
        car_id = q[0]['Id_carro']
        print(car_id)
        p = rent(q[0]['Fecha_i'], q[0]['Fecha_f'], q[0]['precio'], car_id, q[0]['Id_renta'], q[0]['Id_rentb'], db.sql_query_var('select Placa from carro where id_car = %s', (car_id, ))[0]['Placa'])
        print(p.placa)
    else:
        p=None
    return render_template('Myrent.html', p=p)

@app.route('/return-files/matricula/<car_code>', methods=['GET', 'POST'])
def return_filem(car_code):
    path = 'static/cars/' + car_code + '/'
    return send_from_directory(directory=path, filename='matricula.pdf', as_attachment=True)

@app.route('/return-files/seguro/<car_code>', methods=['GET', 'POST'])
def return_filese(car_code):
    path = 'static/cars/' + car_code + '/'
    return send_from_directory(directory=path, filename='seguro.pdf', as_attachment=True)

@app.route('/return-files/soat/<car_code>', methods=['GET', 'POST'])
def return_fileso(car_code):
    path = 'static/cars/' + car_code + '/'
    return send_from_directory(directory=path, filename='soat.pdf', as_attachment=True)

@app.route('/fc', methods=['GET', 'POST'])
def fc():
    no_session()
    return render_template('formaDueno.html')

@app.route('/fd', methods=['GET', 'POST'])
def fd():
    no_session()
    return render_template('formaCliente.html')


# Cosas del chat ............................................................


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    chatRooms = dbHandler.allChatRooms()
    rooms=[]
    for r in dbHandler.allChatRooms():
        rooms.append(''.join(r))
    return render_template("cuasihome.html", rooms=rooms)


@app.route('/createChatRoom', methods=['GET', 'POST'])
def createChatRoom():
    chatRoomDb = 'lolazo'  # Creating new Name of the chatroom ID according to UNIX timestamp.

    dbHandler.createChatRoomDB(chatRoomDb)  # Creating new table in database for new chatroom.
    dbHandler.createChatRoomID(chatRoomDb)  # Enlisting new 'database ID' to 'ChatRoomID' table.

    return (chatRoomDb)  # returning name of the new chatroom, client side script will be executed according to this.


@app.route('/<chatRoomName>')  # variable 'url' for any chatroom
def chatRoom(chatRoomName):
    u = User('lol')
    return render_template("index.html", chatRoomName=chatRoomName,
                           u=u)  # This is common chatroom page, this will be renderd for any chatroom.


@app.route('/addChatToDB', methods=['GET', 'POST'])
def addChatToDB():
    chatRoomID = request.form['chatRoomID']  # This data will come via ajax request, check 'main.js' file
    username = request.form['username']  # same as previous
    comment = request.form['comment']  # same as previous
    # chatCount = request.form['chatCount'] #This data will come via ajax request, this chat count will be incremented acoording to client side.

    dbHandler.addChatToDB(chatRoomID, username,
                          comment)  # comment and username will be inserted to db according to chatRoomID.

    return ('', 204)  # For returning null value to client


@app.route('/fetchChatData', methods=['GET', 'POST'])
def fetchChatData():
    chatCount = request.form['chatCount']
    chatRoomID = request.form['chatRoomID']

    chats = dbHandler.retrieveChatRoom(chatRoomID, chatCount)

    return jsonify(chats)

# Cosas del Perfil ..........................................................

@app.route('/EditProfile', methods=['GET', 'POST'])
def Editprofile():
    no_session()
    user = session["id"]
    db = DataBaseConnection
    u1 = db.sql_query_var("select * from usuario where Id = %s", (user, ))
    LIuser= User(u1[0]['Nombre'], u1[0]['Apellido'], u1[0]['Cedula'],  u1[0]['Correo'], u1[0]['Bday'], u1[0]['Dir'])
    if request.method == 'POST':
        Dir = request.form['Address']
        Mail = request.form['Mail']
        db.sql_edit("update usuario set Dir = %s, correo = %s where id = %s;", (Dir, Mail, user ))
        return redirect(url_for('Editprofile'))
    return render_template('Editprofile.html', User=LIuser)



if __name__ == "__main__":
    app.run(debug=True)
