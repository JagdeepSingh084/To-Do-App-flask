from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)

# SQLite database URI

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(800), nullable=False)
    due_date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

#default end point 
@app.route('/', methods=['GET','POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        todo = ToDo(title = title, description = description)
        db.session.add(todo)
        db.session.commit()
        print("Task posted Successfully!!!")

    alltodos = ToDo.query.all()
    return render_template('index.html', alltodos = alltodos)
    #return 'Hello World!'

#Delete end Point
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

#Update end Point
@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        print("Task updated Successfully!!!")
        return redirect("/")
    
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = todo)

if __name__ == '__main__':
    
    app.run(debug = True)

