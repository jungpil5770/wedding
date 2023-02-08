from flask import Flask, render_template, request, redirect
import datetime
#날짜계산 datetime
from flask_pymongo import PyMongo
import math


app = Flask(__name__)

# flask에 사용할 MongoDB의 URI를 설정(db이름까지 입력)
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)


@app.route('/')
#def hello_world():
def invitation():
    now = datetime.datetime.now()
    wedding = datetime.datetime(2023, 10, 21, 0, 0,0)
    #결혼날짜 - 현재날짜를 뺀 날짜
    diff = (wedding-now).days

    # QueryString을 통해 전달받은 page를 가져오기 위해 사용, 없을 경우 디폴트 값 지정
    # 퀘리로 페이지 번호를 받을 경우 전달 받은 해당 값은 문자열이기 때문에 숫자형으로 변환
    page = int(request.args.get('page',1))
    # 방명록의 개수를 제한해서 가져옴
    limit = 3
    # page마다 보여줄 대상을 지정하기 위해 건너뛰기 사용
    skip = (page-1)*limit
    guestbooks = mongo.db['wedding'].find().limit(limit).skip(skip)

    # count_documents라는 함수를 이용해서 도큐먼트의 개수를 알아냄
    count = mongo.db['wedding'].count_documents({})

    # 최대 페이지 계산 = 전체개수 / 개수제한의 결과값에 올림을 실행
    max_pages = math.ceil(count/limit)

    # range(1부터 최대 페이지만큼의 범위를 가져옴)
    pages = range(1, max_pages+1)

    # 왼쪽 diff(index.html) = 오른쪽 diff(app.py)
    return render_template('index.html', 
                            diff=diff, 
                            guestbooks=guestbooks,
                            pages=pages)

@app.route('/write', methods=["POST"])
def write():
    # form안의 name, content을 꺼냄
    name = request.form.get('name')
    content = request. form. get('content')

    #이름이나 내용의 글씨를 작성하였을시 남기기 글 저장
    #or : 조건이 둘중에 하나만 만족해도 참, not : 부정연산자)참 -> 거짓, 거짓 -. 참)
    #name이나 content의 내용이 둘중에 하나라도 공백이면 아래의 db에 내용을 넣지 않음.
    if not(name=="" or content==""):
    #form에서 받은 값들을 wedding collect에 저장
        mongo.db['wedding'].insert_one({
            "name": name,
            "content": content
         })
         
# @app.route('/') 이동
    return redirect('/')

if __name__ == '__main__':
    app.run()