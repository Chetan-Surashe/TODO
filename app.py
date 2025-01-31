from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

class Todo(db.Model):
    SrNo=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



def __repr__(self) -> str:
        return f"{self.SrNo} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
       title=request.form['title']
       desc=request.form['desc']
       todo=Todo(title=title,desc=desc)
       db.session.add(todo)
       db.session.commit()
    alltodo=Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/show')
def show_todos():
    alltodo = Todo.query.all()  # Query all records
    result = "\n".join([f"{todo.SrNo}: {todo.title} - {todo.desc}" for todo in alltodo])
    print(result)
    return f"<pre>{result}</pre>"  # Display in a preformatted block for readability

@app.route('/delete/<int:SrNo>')
def delete(SrNo):
    todo = Todo.query.filter_by(SrNo=SrNo).first()  
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:SrNo>',methods=['GET','POST'])
def update(SrNo):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(SrNo=SrNo).first()  
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(SrNo=SrNo).first()  
    return render_template('update.html',todo=todo)
    

if __name__ ==  "__main__":
    app.run(debug=True)