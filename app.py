from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
# app.config['SQLALCHEMY_POOL_TIMEOUT'] =  60
app.config['SQLALCHEMY_POOL_RECYCLE'] =  60
db = SQLAlchemy(app)

class myTodo(db.Model):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(30), default=dt_string)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.desc} - {self.date}"

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST' :
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        tit = request.form.get('title')
        des = request.form.get('desc')
        tit+=" "
        des+=" "
        if (tit.isspace() == False and des.isspace() == False):
            todo = myTodo(title=tit, desc=des, date=dt_string)
            db.session.add(todo)
            db.session.commit()

    allTodo = myTodo.query.all()
    return render_template('index.html', allTodos = allTodo)

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/delete/<int:sno>')
def delete(sno): 
    delTodo = myTodo.query.filter_by(sno=sno).first()
    db.session.delete(delTodo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno): 
    if request.method == 'POST' :
        tit = request.form.get('title')
        des = request.form.get('desc')
        tit+=" "
        des+=" "
        if (tit.isspace() == False and des.isspace() == False):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            todo = myTodo.query.filter_by(sno=sno).first()
            todo.title = tit
            todo.desc = des
            todo.date = dt_string
            db.session.add(todo)
            db.session.commit()
            return redirect("/")

    updTodo = myTodo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = updTodo)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', message=e)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
