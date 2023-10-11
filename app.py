from flask import Flask, render_template
from datetime import datetime
import requests
import json

app = Flask(__name__)


@app.route("/main")
def main():
  # 가져올 베스트셀러 권 수 (디폴트 4권)
  numOfBook = 4
  # 가져올 날짜 ('YYYY-MM-DD', 공백시 오늘날짜)
  date = ''
  # 날짜 구하기
  def getDate(inputDate=datetime.today().strftime("%Y-%m-%d")):
    dateObj = datetime.strptime(inputDate, "%Y-%m-%d")
    date = dateObj.strftime("%Y-%m-%d").split('-')
    year, month = date[0], date[1]
    firstDay = dateObj.replace(day=1)
    week = (dateObj - firstDay).days // 7 + 1
    return year, month, week

  year, month, week = getDate(date) if date != '' else getDate()
  res = requests.get(f"https://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey=ttbgarry94571426002&QueryType=Bestseller&MaxResults={numOfBook}&start=1&SearchTarget=Book&output=js&Year={year}&Month={month}&Week={week}&Version=20131101")
  rjson = res.json()
  context = rjson['item']
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