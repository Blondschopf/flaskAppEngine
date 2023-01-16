from flask import Flask, redirect, url_for, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from flask_login import LoginManager

app = Flask(__name__)

# Setup MYSQL
db = yaml.full_load(open("db.yaml"))
app.config['MYSQL_USER'] = db["mysql_user"]
app.config['MYSQL_PASSWORD'] = db["mysql_password"]
app.config['MYSQL_HOST'] = db["mysql_host"]
app.config['MYSQL_DB'] = db["mysql_db"]

mysql = MySQL(app)

@app.route("/")
def home():
  return render_template("index.html", title="Home", content="Home")

@app.route("/insert", methods=["GET", "POST"])
def insert():

  # Check if request method is POST
  if request.method == "POST":

    # Get Data from the Form
    formData = request.form
    name = formData["name"]
    password = formData["password"]

    # Write data to the database
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users(name, password) VALUES(%s, %s)", (name, password))
    mysql.connection.commit()
    cursor.close()

    # redirecting to view the users
    return redirect(url_for("users"))

  return render_template("insert.html", title="insert")

@app.route("/delete/<string:id>")
def delete(id):
  cursor = mysql.connection.cursor()
  cursor.execute("DELETE FROM users WHERE id = %s", (id))
  mysql.connection.commit()
  cursor.close()
  return redirect(url_for("home"))


@app.route("/check", methods=["GET", "POST"])
def check():

  # Check if request method is POST
  if request.method == "POST":
     
     ## Get Data from the Form
    formData = request.form
    name = formData["name"]
    password = formData["password"]

    # Write check data with database
    cursor = mysql.connection.cursor()
    resultValue = cursor.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
    
    # Redirect to home with success if success
    print(resultValue)
    if resultValue > 0:
      return render_template("index.html", title="Home", content="It worked! :)")
    
    # Else say it didn't work
    return render_template("index.html", title="Home", content="It didn't work :(")
  
  # If Get tive the render template of check
  return render_template("check.html", title="Check")

@app.route("/users")
def users():
  cursor = mysql.connection.cursor()
  resultValue = cursor.execute("SELECT * FROM users")
  if resultValue > 0:
    resultDetails = cursor.fetchall()
    return render_template("users.html", resultDetails=resultDetails, title="users")
  return "There was an error"

@app.route("/<name>")
def name(name):
  return render_template("index.html", content=name, title=name)

if __name__ == "__main__":
  app.run(debug=True)