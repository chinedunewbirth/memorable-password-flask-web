from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint, sample
from sqlalchemy import DateTime


app = Flask(__name__)
app.config["SECRET_KEY"] = "&*&^^rt%%^^^&&"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'

#database object
db = SQLAlchemy(app)

#define shema
class Users(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    word =  db.Column(db.String(30))
    email = db.Column(db.String(30))
    userid = db.Column(db.String(6))
    
    def __repr__(self):
        return "%r %r".format(self.id, self.userid)
        
    
#generate random number
def randNum(n):
    start = 10**(n - 1)
    end = (10**n) -1 
    return randint(start, end)
    
data = None
lstPos = []
email = None

    
@app.route('/')
def index():
    return render_template('index.html', data=None)
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == "POST":
        
            word = request.form["word"]
            email = request.form["email"]
            
            #generate random number
            randid = str(randNum(6))
            
            #add user
            user = Users(word=word, email=email, userid=randid)
            db.session.add(user)
            db.session.commit()
            
            msg = f"User register! {randid} is login id"
            flash(msg)
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))
        
@app.route('/dashboard')
def dashboard():
    try:
        count = Email.query.filter_by(sender=session['email']).count()
        print(count)
        if session['email']:
            return render_template('dashboard.html', count=count)
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        global data, lstPos, email
        if request.method == "POST":
            codeid = request.form["codeid"]
            
            #query
            query = Users.query.filter_by(userid=codeid).first()
            if query:
                #convert to list
                data = sample(list(query.word.upper()), 3)
                pos = [list(query.word.upper()).index(item) for item in data]
                pos = [item + 1 for item in pos]
                lstPos.extend(pos)
                email = query.email
                print(pos)
                return render_template('index.html', trigger_modal=True, data=data, lstPos=lstPos)
            else:
                flash("Wrong logging code id!")
                return redirect(url_for("index"))
        return redirect(url_for('index'))
    except:    
        return redirect(url_for('index'))
    
    
@app.route('/check', methods=["POST", "GET"])
def check():
    try:
        if request.method == "POST":
            pos0 = request.form["pos0"]
            pos1 = request.form["pos1"]
            pos2 = request.form["pos2"]
            #add items to list
            lstAns = []
            lstAns.append(int(pos0))
            lstAns.append(int(pos1))
            lstAns.append(int(pos2))
            #convert string to list
            print(lstAns, lstPos)
            if lstAns == lstPos:
                session['email'] = email
                flash("Welcome user!")
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong letter to position match!!')
            return redirect(url_for('index'))
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))      
    
@app.route('/logout')
def logout():
    try:
        global data, lstPos
        data = None
        lstPos = []
        session.pop('email', None)
        flash('User logged out!')
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)