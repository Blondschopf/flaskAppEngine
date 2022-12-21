from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/test")
def test():
  return "Woooooooah"

@app.route("/path")
def path():
  return "<h1>This is crazy shiiiit</h1>"

if __name__ == "__main__":
  app.run()