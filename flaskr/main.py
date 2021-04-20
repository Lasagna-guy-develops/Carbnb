from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
import DataBaseConnection
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

@app.route('/Register', methods=['GET', 'POST'])
def register():
    db = DataBaseConnection
    error = None
    if request.method == 'POST':

        correo = request.form['username']
        pssw = request.form['password']


    return render_template('SignUp.html')

@app.route('/Home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')