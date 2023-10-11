from flask import Flask, render_template

app = Flask(__name__)


@app.route("/main")
def main():
  context = {

  }
  return render_template("main.html", data=context)

@app.route("/team")
def team():
  context = {

  }
  return render_template("team.html", data=context)

@app.route("/question/<number>")
def question():
  context = {

  }
  return render_template("question.html", data=context)

@app.route("/result")
def result():
  context = {

  }
  return render_template("result.html", data=context)


@app.route("/map")
def map():
  context = {

  }
  return render_template("map.html", data=context)

if __name__ == "__main__":
  app.run(debug=True)