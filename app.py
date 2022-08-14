from logging import setLogRecordFactory
from threading import get_ident
from webbrowser import get
from MySQLdb import DATE
from flask import Flask, render_template , request , redirect
from flask_mysqldb import MySQL ,MySQLdb
import datetime
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "123456"
app.config['MYSQL_DB'] = 'emirdb'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register' , methods=['POST'])
def Create():
    if request.method == 'POST':
        now = datetime.datetime.utcnow()
        created_at = now.strftime('%Y-%m-%d %H:%M:%S')
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']
        about = request.form['about']
        updated_at = None
        cursor = mysql.connection.cursor()
        #sorgu = "INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute("INSERT INTO user(id,firstname,lastname,about,created_at,updated_at,age) VALUES(%s,%s,%s,%s,%s,%s,%s)",(None,firstname,lastname,about,created_at,updated_at,age))
        mysql.connection.commit()
        cursor.close()
        return redirect('/register')

@app.route('/getregister' , methods=['GET'])
def GetUsers():
        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM user"
        cursor.execute(sorgu) 
        users = cursor.fetchall()
        cursor.close()
        return render_template("register.html",registers=users)

@app.route('/delete')
def Delete():
    return render_template('delete.html')

@app.route('/delete' , methods=['POST'])
def DeleteTable():
    if request.method == 'POST':
        getid = request.form['Id']
        cursor = mysql.connection.cursor()
        #sorgu = "DELETE FROM user WHERE id = %s" % (id)
        cursor.execute("DELETE FROM user WHERE id = %s" % (getid))
        mysql.connection.commit()
        cursor.close()
        return redirect('/getregister')
    else:
        print('HATA OLDU..')

@app.route('/update')
def Update():
    return render_template('update.html')

@app.route('/update', methods=['POST'])
def DoUpdate():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        getid = request.form['Id']
        getAbout = request.form['About']
        now = datetime.datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        sorgu = """UPDATE user set about = %s WHERE id = %s"""
        cursor.execute(sorgu , (getAbout,getid))
        tarihsorgu = """UPDATE user set updated_at = %s WHERE id = %s"""
        cursor.execute(tarihsorgu , (now,getid))
        cursor.connection.commit()
        cursor.close()
        return redirect('/getregister')
    else:
        print('HATA OLDU..')

if __name__ == '__main__':
    app.run(debug=True)