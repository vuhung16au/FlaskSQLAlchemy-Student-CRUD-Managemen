# https://pythonbasics.org/flask-sqlalchemy/

import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking, improve performance 

# Add a random secret key to your app
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))  
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin


@app.route('/')
@app.route('/show_all')
@app.route('/show_all_students')
def show_all_students():
   return render_template('show_all_students.html', students = students.query.all() )

# update student record with the given id
@app.route('/update_student/<int:id>', methods = ['GET', 'POST'])
def update_student(id):
   student = students.query.get(id)
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student.name = request.form['name']
         student.city = request.form['city']
         student.addr = request.form['addr']
         student.pin = request.form['pin']
         
         db.session.commit()
         flash('Record was successfully updated')
         return redirect(url_for('show_all_students'))
   return render_template('update_student.html', student = student)

# delete the student record with the given id
@app.route('/delete_student/<int:id>', methods = ['GET', 'POST'])
def delete_student(id):
   student = students.query.get(id)
   db.session.delete(student)
   db.session.commit()
   flash('Record was successfully deleted')
   return redirect(url_for('show_all_students'))

# create a new student record
@app.route('/new_student', methods = ['GET', 'POST'])
def new_student():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Please enter all the fields', 'error')
      else:
         student = students(request.form['name'], request.form['city'],
            request.form['addr'], request.form['pin'])
         
         db.session.add(student)
         db.session.commit()
         
         flash('Record was successfully added')
         return redirect(url_for('show_all_students'))
      
   return render_template('new_student.html')

if __name__ == '__main__':
   with app.app_context():
       db.create_all()
   app.run(debug=True, port=5430)  