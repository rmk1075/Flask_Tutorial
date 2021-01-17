# Flask_Tutorial

> flask documentation을 따라 만든 flask tutorial

## 2021.01.17

### flask 환경 설정

<details>

<summary>virtual environments</summary>

- 프로젝트 디렉토리 내부에 가상환경 설치

- py -m venv venv

- . venv/Scripts/activate

  - 가상환경 실행
  
  - 가상환경 중단 시 deactivate
  
</details>

<details>

<summary>flask 설치</summary>

- 가상환경 실행 후 flask 설치

- pip install Flask

- pip install -U <https://github.com/pallets/flask/archive/master.tar.gz>
  
</details>

### A minimal Application

<details>

<summary>Hello World</summary>

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

1. import Flask class

> from flask import Flask

- Flask class의 instance가 WSGI application으로 작동

- WSGI (Web Server Gateway Interface)

  - 파이썬에서 application이 web server와 통신하기 위한 interface

  - server, app 양단으로 나뉘어져 있음
  
    - server - Nginx, Apache

    - app - python script

  - WSGI request 처리를 위해서는 server에서 환경정보와 콜백함수를 app에 제공해야함

  - app은 그 요청을 처리하고 콜백함수를 통해 server에 응답

  > request -> web server -> WSGI Server (middleware) -> WSGI web application (Django, flask)

2. Flask instance 생성

> app - Flast(__name__)

- \_\_name__: application module이나 package의 이름

  - \_\_main__: main module에서 사용시 가지는 이름

- Flask가 템플릿이나 파일들의 위치를 알 수 있도록한다.

3. route()

> @app.route('/')

- 함수 시작이 될 URL을 매핑시켜준다.

4. 함수 선언

> def hello_world():
>
> return 'Hello, World!'

- '/' url에서 호출될 함수 선언

5. 서버 실행

- FLASK_APP 설정

  - export FLASK_APP=hello.py

- FLASK 서버 실행

  - flask run

</details>
