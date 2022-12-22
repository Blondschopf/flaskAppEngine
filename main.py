from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
  return render_template("index.html", content="user")

@app.route("/<name>")
def name(name):
  return render_template("index.html", content=name)

@app.route("/admin/")
def admin():
  return redirect(url_for("name", name="Admin!"))

if __name__ == "__main__":
  app.run()