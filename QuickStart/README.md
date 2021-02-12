# Quick Start

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

## 2021.02.08

### Accessing Request Data

<details>

<summary>Accessing Request Data</summary>

- request 객체 - 전역객체

</details>

<details>

<summary>Context Locals</summary>

</details>

<details>

<summary>Request Objects</summary>

```python
from flask import request

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
```

- method 속성으로 request method 접근 가능

- form 속성으로 사용해서 data 사용

- key가 존재하지 않는 data 접근 시 key error -> HTTP 400 (Bad Request) 발생

```python
searchword = request.args.get('key', '')
```

- args 속성을 통해서 url parameter에 접근 가능

</details>

<details>

<summary>File Uploads</summary>

- files attribute를 통해서 file data 접근 가능

- upload된 각 파일들은 그 dictionary안에 저장되어 있다.

- save() method를 이용해서 서버 시스템에 저장가능

  - save(file_path)

```python
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
```

- filenames attribute를 통해서 file 이름 접근

```python
from flask import request
from werkzeug import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
```

</details>

<details>

<summary>Cookies</summary>

- cookies attribute를 통해서 cookies 접근

- set_cookie(): response 객체의 cookie를 설정

- read cookies

```python
from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.
```

- write cookies

```python
from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
```

</details>

## 2021.02.10

### Redirects and Errors

<details>

<summary>Redirects and Errors</summary>

- redirect(): 다른 엔드포인트로 redirect

- abort(): 에러코드와 함께 요청을 중단

```python
from flask import abort, redirect, url_for

# root url로 접근시 /login으로 redirect
@app.route('/')
def index():
    return redirect(url_for('login'))

# /login 접근시 에러코드 401로 요청중단
@app.route('/login')
def login():
    abort(401)
    # this_is_never_executed()
```

- errorhandler(): errorhandler 데코레이터를 사용하여 에러페이지 변경

```python
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
    # render_template 뒤의 404는 페이지의 상태코드가 404가 되어야한다는 것을 flask에 말해준다. 기본적으로 200으로 설정되어있다. (200, OK)
```

</details>

### About Responses

<details>

<summary>About Responses</summary>

- view function의 return value는 자동으로 response 객체로 변환된다.

- return value가 string인 경우 200 OK 상태코드와 test/html mimtype


```python
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp
```

</details>

<details>

<summary>APIs with JSON</summary>

- response 포맷으로 JSON 형식을 사용

```python
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }
```

</details>

### Session

<details>

<summary>Session</summary>

- Session 객체

  - Session 사용을 위해서는 비밀키 사용 필요

  - 비밀키를 모르면 cookie를 조회만 가능. 변경은 불가능.

```python
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
```

</details>

## 2021.02.11

### Message Flashing

<details>

<summary>Message Flashing</summary>

- flashing system은 request의 끝과 그 바로 다음 request에 접근할 떄 메시지를 기록할 수 있도록 한다.

- flash(): 메세지를 flash

- get_flashed_messages(): 메세지를 가져오기 위해서 템플릿에서 사용할 수 있는 메소드

- <https://flask-docs-kr.readthedocs.io/ko/latest/patterns/flashing.html#message-flashing-pattern>

</details>

### Logging

<details>

<summary>Logging</summary>

- logger를 사용해서 로그 출력

```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')
```

</details>

### Hooking in WSGI Middleware

<details>

<summary>Hooking in WSGI Middleware</summary>

```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
```

</details>