from flask import Flask, render_template, request
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
@app.route('/home', methods=['GET','POST'])
def add_todo():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        
        todo = ToDo(title = title, description = description)
        db.session.add(todo)
        db.session.commit()
        print("Task posted Successfully!!!")

    alltodos = ToDo.query.all()
    return render_template('index.html', alltodos = alltodos)
    #return 'Hello World!'

#Second end Point
@app.route('/cart')
def cart():
    return "This is to show cart products"

if __name__ == '__main__':
    
    app.run(debug = True)

