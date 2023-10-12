from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os

from flask_sqlalchemy import SQLAlchemy

# API 인증키
API_KEY_CODE_ALADIN = 'ttbgarry94571426002'
API_KEY_CODE_LIB = 'e269317ce6c8a313d58e210bebd35514f8eab2c77b24e3d5f2ee65e593982b5b'
# 한번에 불러올 수 있는 최대 도서관 갯수
LIB_SIZE = 350

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
  'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

# MBTI 검사 질문지 DB
class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  choose_type = db.Column(db.String(2))
  option_A = db.Column(db.String(255))
  option_B = db.Column(db.String(255))
  answer = db.Column(db.Integer)

# MBTI 검사 결과 DB
class MBTI(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  mbti_type = db.Column(db.String(100), nullable=False)
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
  res = requests.get(f"https://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey={API_KEY_CODE_ALADIN}&QueryType=Bestseller&MaxResults={numOfBook}&start=1&SearchTarget=Book&output=js&Year={year}&Month={month}&Week={week}&Version=20131101")
  rjson = res.json()
  context = rjson['item']
  return render_template("main.html", data=context)

@app.route("/team")
def team():
  return render_template("team.html")

# MBTI 결과 계산 함수
def calculate_mbti():
  types = {}  # 각 choose_type에 대한 누적 점수를 저장할 딕셔너리
  questions = Question.query.all()

  # 모든 질문에 대해 choose_type에 따라 누적 점수 계산
  for question in questions:
    if question.choose_type not in types:
      types[question.choose_type] = 0
    types[question.choose_type] += question.answer

  # 각 choose_type의 누적 점수가 양수면 두 번째 글자를 사용, 음수면 첫 번째 글자 사용
  mbti_result = ""
  for choose_type, score in types.items():
    if score >= 0:
      mbti_result += choose_type[1]
    else:
      mbti_result += choose_type[0]

  return mbti_result

@app.route("/test")
def test():
  # 첫번쨰 질문만 제시, 다음 이어지는 질문들을 가져오는건 일단은 answer에서 진행 (개선 예정)
  question = Question.query.first()
  return render_template("test.html", data=question)

@app.route("/answer", methods=["POST"])
def answer():
  question_id = request.form['question_id']
  selected_option = request.form['option']  # 선택된 옵션 (A 또는 B)
  question = Question.query.get(question_id)

  # 사용자의 선택에 따라 answer 값을 저장
  if selected_option == 'A':
    question.answer = -1
  elif selected_option == 'B':
    question.answer = 1
  db.session.commit()

  # 다음 질문 가져오기 (id값 대조)
  next_question = Question.query.filter(Question.id > question.id).first()
  # 다음 질문이 있으면 진행, 아니면 MBTI 계산
  if next_question:
    return render_template('test.html', data=next_question)
  else:
    calculated_mbti = calculate_mbti()
    answer = MBTI.query.filter_by(mbti_type=calculated_mbti).first()
    return render_template("answer.html", data=answer)


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

# 지역코드와 ISBN13코드로 책을 보유중인 도서관 검색 (미구현)
@app.route("/loan")
def loan(isbnCode=9791192389325, regionCode=11):
	# res = requests.get(f"http://data4library.kr/api/libSrchByBook?authKey={API_KEY_CODE_LIB}&isbn={isbnCode}&region={regionCode}&pageSize={LIB_SIZE}&format=json")
	# rjson = res.json()
	return render_template("loan.html")

if __name__ == "__main__":
  app.run(debug=True)