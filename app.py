from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import requests
import os

from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class MBTI(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String(100), nullable=False)
  description = db.Column(db.String(10000), nullable=False)
  book = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/main")
def main():
  # 가져올 베스트셀러 권 수 (디폴트 4권)
  numOfBook = 4
  # 가져올 날짜 ('YYYY-MM-DD', 공백시 오늘날짜)
  date = ''

  # 날짜 구하기
  inputDate = datetime.strptime(date, "%Y-%m-%d") if date != '' else datetime.today()
  def getDate(inputDate):
    date = inputDate.strftime("%Y-%m-%d").split('-')
    year, month = date[0], date[1]
    firstDay = inputDate.replace(day=1)
    week = (inputDate - firstDay).days // 7 + 1
    return year, month, week
  
  # 구한 날짜로 해당 주의 베스트셀러 불러오기
  year, month, week = getDate(inputDate)
  res = requests.get(f"https://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbgarry94571426002&QueryType=Bestseller&MaxResults={numOfBook}&start=1&SearchTarget=Book&output=js&Year={year}&Month={month}&Week={week}&Version=20131101")
  rjson = res.json()
  context = rjson['item']
  return render_template("main.html", data=context)

@app.route("/team")
def team():
  context = {

  }
  return render_template("team.html", data=context)

@app.route("/question/")
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