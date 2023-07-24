from sqlalchemy.exc import IntegrityError
from flask import Flask,flash, render_template,request,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select,and_
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ='sqlite:///test.db'
app.secret_key='key'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstName=db.Column(db.String(30),nullable=False)
    lastName=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)
with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        try:
            session['user']=None
            password=request.form['password'] 
            email=request.form['email']
            users=User.query.order_by(User.id.desc()).all()
            flag=False
            for user in users:
                if user.email==str(email).strip() and user.password==str(password).strip():
                    flag=True            
            if flag:
                session['user']=str(email).strip()
                return redirect(url_for('secret_page'))
            else:
                return render_template('index.html',messages="Invalid email or password",email=email)

        except Exception as e:
            return render_template('index.html',messages=e)
    return render_template('index.html')

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    if request.method=='POST':
        try:
            firstName=request.form['firstName'] 
            lastName=request.form['lastName'] 
            email=request.form['email'] 
            password=request.form['password']
            conformpass=request.form['conformpass']

            lc=False
            uc=False
            len_pass=False
            dig_check=False
            for i in password:
                if(i.islower()):
                    lc=True
            for i in password:
                if(i.isupper()):
                    uc=True
            if (len(password)>=8):
                len_pass=True
            if(password[len(password)-1].isdigit()):
                dig_check=True
            check_status= lc and uc and len_pass and dig_check

            if check_status == False:
                return render_template('signUp.html',firstName=firstName,
                                   lastName=lastName,email=email,password=password,conformpass=conformpass,
                                   check_status=check_status,lc=lc,uc=uc,len_pass=len_pass,dig_check=dig_check)

            if password!=conformpass:
                return render_template('signUp.html',messages="Password and Confirm Password must same",firstName=firstName,
                                   lastName=lastName,email=email,password=password,conformpass=conformpass,check_status=check_status)
            
            users=User(firstName=firstName,lastName=lastName,email=email,password=password)
            db.session.add(users)
            db.session.commit()
            #return render_template('Thankyou.html')
            return redirect(url_for('thanks_page'))
        except IntegrityError:
            return render_template('signUp.html',messages="Already regiestered with this mail id",firstName=firstName,
                                   lastName=lastName,email=email,password=password,conformpass=conformpass,check_status=check_status)

    return render_template('signUp.html',check_status=True)

@app.route('/thanks')
def thanks_page():
    return render_template('Thankyou.html')

@app.route('/secretpage',methods=['GET','POST'])
def secret_page():
    if request.method=='POST':
        session['user']=None
        return redirect(url_for('index'))
    if session['user']==None:
        return redirect(url_for('index'))
    return render_template('SecretPage.html')


if __name__=='__main__':
    app.run(debug=True)
