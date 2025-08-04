from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String,DateTime
from datetime import datetime
import os
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'todo.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    desc: Mapped[str] = mapped_column(String(200), nullable=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.title}, {self.desc}, {self.date_created}>"

with app.app_context():
    # print("Creating DB...")
    db.create_all()
    # print("Done!")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        # print(title)

        todo = User(title=title, desc=desc, date_created=datetime.utcnow())
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todos= User.query.all()
        # print(todos)
    return render_template('index.html', todos=todos)
    # return render_template('index.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_me = User.query.filter_by(id=id).first()
    if delete_me:
        db.session.delete(delete_me)
        db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    todo = User.query.filter_by(id=id).first()  # or: User.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')

        todo.title = title
        todo.desc = desc
        todo.date_created = datetime.utcnow()
        db.session.commit()
        return redirect('/')

    return render_template('update.html', todo=todo)
# Uncomment the following route if you want to display all todos in a simple format

    


# @app.route('/show')
# def show():
#     todos= User.query.all()
#     print(todos)
#     return "<br>".join([f"{todo.title} - {todo.desc} - {todo.date_created}" for todo in todos])
if __name__ == "__main__":
    app.run(debug=True)
