#import Flask class from flask module
from flask import Flask,render_template,request
#creating app object
app=Flask(__name__)
#import SQLAlchemy class from flask_sqlalchemy module
from flask_sqlalchemy import SQLAlchemy
#creating uri for db connection
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///storage.db'
#creating connection from SQLAlchemy to db using app object
db=SQLAlchemy(app)
#creating model in db
class user(db.Model):
    sno=db.Column('sno',db.Integer,primary_key=True)
    user_name=db.Column(db.String(30))
    user_email=db.Column(db.String(30))
    user_age=db.Column(db.Integer)

    def __init__(self,name,email,age):
        self.user_name=name
        self.user_email=email
        self.user_age=age
#creating database
db.create_all()
#url routing
@app.route('/')
#creating views
def retrive():
    return render_template('retrive.html',details=user.query.all())
    #return render_template('retrive.html',details=user.query.filter_by(sno=3))

@app.route('/insert')
def insert():
    return render_template("register.html")

@app.route('/register',methods=['POST','GET'])
def register():
    details=user(request.form['name'],request.form['email'],request.form['age'])
    db.session.add(details)#for data insertion
    db.session.commit()
    return render_template('retrive.html',details=user.query.all())

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/edit',methods=['POST','GET'])
def edit():
    u=request.form['uid']
    user_details=user.query.filter_by(sno=u)
    return render_template('edit.html',data=user_details)

@app.route('/save_updates',methods=['POST','GET'])
def save_updates():
    u=request.form['uid']
    details=user.query.filter_by(sno=u).first()
    details.user_name=request.form['uname']
    details.user_email=request.form['email']
    details.user_age=request.form['age']
    db.session.commit()
    return render_template('retrive.html',details=user.query.all())
#application running
app.run(debug=True)
