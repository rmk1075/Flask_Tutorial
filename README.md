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

## 2021.01.19

### Debug Mode

<details>

<summary>Development server</summary>

```shell
export FLASK_ENV=development
flask run
```

- FLASK_ENV: environment variable

  - development

1. activates the debugger

2. activates the automatic reloader

3. enables the devbug mode on the Flask application

※ development server guide: <https://flask.palletsprojects.com/en/1.1.x/server/#server>

</details>

### Routing

<details>

<summary>Routing</summary>

- hello2.py

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
```

</details>

<details>

<summary>Variable Rules</summary>

```python
from markupsafe import escape

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)
```

- URL에 varaible section을 더할수 있다.

- <variable_name>을 URL에 사용시 variable_name을 argument로 수신하게 된다.

- <converte:variable_name>: converter를 option으로 사용가능

  - converter types: string(default), int, float, path, uuid

</details>

<details>

<summary>Unique URLs/Redirection Behavior</summary>

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

- '/projects/'의 경우 마지막 '/'없이 '/projects'로 접근시 '/prjects/로 redirect

- '/about'의 경우 '/about/'으로 접속시 404 Not Found 발생

</details>

<details>

<summary>URL Building</summary>

- url_for()

  - 첫번째 argument로 함수의 이름을 입력받는다.

  - keyword argument를 option으로 추가입력.

```python
from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
```

</details>

<details>

<summary>HTTP Methods</summary>

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```

- route()의 default method는 GET

- route()의 argument로 GET, POST 사용

</details>

## 2021.02.07

### Static Files

<details>

<summary>Static Files</summary>

- static file 사용 시 패키지 내부에 static 폴더 생성하고 static file들을 위치시켜 사용한다.

```python
url_for('static', filename='style.css')
```

</details>

### Rendering Templates

<details>

<summary>Rendering Templates</summary>

- Flask는 Jinja2 Template을 자동으로 설정한다. (<https://jinja.palletsprojects.com/en/2.11.x/>)

- render_template()

  - template rendering시 사용하는 method

  - flask.render_template(template_name_or_list, **context)

    - tamplate_name_or_list: 사용하려는 템플릿 이름

    - context: template context에서 사용할 변수

  - <https://flask.palletsprojects.com/en/1.1.x/api/#flask.render_template>

  ```python
  from flask import render_template

  @app.route('/hello/')
  @app.route('/hello/<name>')
  def hello(name=None):
      return render_template('hello.html', name=name)
  ```

  - flask는 templates 폴더에서 hello.html을 찾는다.

  - hello.html template의 name 변수에 hello함수에서의 name 값 사용

- get_flashed_messages()

  - <https://flask.palletsprojects.com/en/1.1.x/api/#flask.get_flashed_messages>

  - template안에서 request, session, g object 접근하여 사용 가능

</details>