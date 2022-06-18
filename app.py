"""Flask API Authentication Method."""
from flask import (
   Flask,
   url_for,
   render_template,
   request,
   redirect,
   session,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
database = SQLAlchemy(app)


class User(database.Model):
   """
   Model to persist user registrations.
   """
   id = database.Column(database.Integer, primary_key=True)
   username = database.Column(database.String(30), unique=True)
   password = database.Column(database.String(30))

   def __init__(self, username, password):
      self.username = username
      self.password = password


@app.route('/', methods=['GET'])
def index():
   """
   Method to render frontend templates.
   """
   if session.get('logged_in'):
      return render_template(
         'home.html',
      )
   else:
      return render_template(
         'index.html',
         message="HOME !",
      )


@app.route('/register/', methods=['GET', 'POST'])
def register():
   """
   Method to register users.
   """
   if request.method == 'POST':
      try:
         database.session.add(
            User(
            username=request.form['username'],
            password=request.form['password'],
            ),
         )
         database.session.commit()
         return redirect(url_for('login'))
      except:
         return render_template(
            'index.html',
            message="The User Already Exists",
         )
   else:
      return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
   """
   Method to log in existing users.
   """
   if request.method == 'GET':
      return render_template('login.html')
   else:
      username = request.form['username']
      password = request.form['password']
      data = User.query.filter_by(
         username=username,
         password=password,
      ).first()

      if data is not None:
         session['logged_in'] = True
         return redirect(url_for('index'))

      return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
   """
   Method to log out existing users.
   """
   session['logged_in'] = False
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.secret_key = "SecretKey"
   database.create_all()
   app.run()
