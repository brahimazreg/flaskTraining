from flask import Flask,render_template,redirect , request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# My app
app=Flask(__name__) # app is the name of my flask application
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flasktestdb.db"

# this line is for deployment
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

# Data class row of data
class MyTask(db.Model):
    id=db.Column(db.Integer , primary_key=True)
    content =db.Column(db.String(150),nullable=False)
    complete =db.Column(db.Integer ,default=0 )
    created =db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"
# this change is made in order to deploy 
#with app.app_context():
    #db.create_all()


@app.route('/',methods=['GET','POST'])
def index():
    # Add a task
    # I have to test which action is taken
    if request.method=='POST':
        current_task=request.form['content']
        new_task=MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
    # See all Tasks 
    else:
        tasks=MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html',tasks=tasks)
    

# Delete  an Item
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task=MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error :{e}"
    
# Edit  an Item
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edite(id:int):
    task=MyTask.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']      
        try:            
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html',task=task)





# to deploy the application we have to make change in app.py




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    #app.run(host="0.0.0.0", port=5000)
    app.run()
