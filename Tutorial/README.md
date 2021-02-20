# Tutorial

## 2021.02.13

### Project Layer

<details>

<summary>Project Layer</summary >

- Tutorial 프로젝트 디렉토리 내부 구조

  - flaskr/: 어플리케이션 소스와 파일을 보관할 파이썬 패키지

  - tests/: 테스트 모듈들을 보관할 디렉토리

  - venv/: 프로젝트를 위한 파이썬 가상환경

    - 이 프로젝트의 경우 ../venv/의 가상환경 사용한다.

</details>

### Application Setup

<details>

<summary>Application Setup</summary>

- Flask application은 Flask class의 인스턴스로 설정과 URL등이 모두 클래스에 등록되어있다.

- Flask 인스턴스를 글로벌하게 만드는 것은 프로젝트 규모가 커져가면서 문제를 야기할 수 있기 때문에 함수를 통해서 인스턴스를 생성할 것이다.

  - application factory

</details>

<details>

<summary>The Application Factory</summary>

- flaskr/__init__.py

  1) application factory를 포함한다.

  2) flaskr 디렉토리가 패키지임을 파이썬에게 알려준다.

  - create_app(): application factory function 및 application 기본 설정

</details>

<details>

<summary>Run The Application</summary>

- Flask 패키지의 최상위 디렉토리에서 application을 실행하도록 한다.

- For Linux and Mac:

```shell
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

</details>

### Define and Access the Database

<details>

<summary>Define and Access the Database</summary>

- 이 프로젝트에서는 SQLite DB를 사용한다.

- 파이썬은 SQLite를 지원하는 모듈 sqlite3를 지원한다.

- SQLite

  - python built-in module

  - 별도의 database server설정이 필요없어서 편하다.

  - 동시접속에서 성능 문제 있을 수 있지만, 작은 프로젝트에서는 문제 없다.

</details>

<details>

<summary>Connect to the Database</summary>

- database connection 생성

  - request에 의해서 connection 생성 후 response 반환 전에 close

- flaskr/db.py

  1) get_db(): g 객체에 접근해서 db 연결설정한다.

  2) close_db(): g 객체에 db 연결 존재하는 경우 종료한다.

</details>

<details>

<summary>Create the Tables</summary>

- SQLite에서 데이터는 table과 columns에 저장된다.

- Flaskr에서 사용자 정보는 user, 게시물은 post 테이블에 저장한다.

- flaskr/schema.sql

  - 테이블 생성

- flaskr/db.py

  1) init_db(): db 설정 초기화한다. db 연결 생성 및 테이블 생성.

  2) init_db_command(): init-db 명령어 설정.

</details>

<details>

<summary>Register with the Application</summary>

- close_db(), init_db_command() 함수는 application 인스턴스에 등록되어야 한다.

- flaskr/db.py

  1) init_db(): close_db, init_db_command 함수 등록

- flaskr/__init__.py

  1) create_app() 함수 하단에 db.init_app() 호출 추가

</details>

<details>

<summary>Initialize the Database File</summary>

- init-db 명령어가 app에 등록되어서 flask run과 같이 사용가능

```shell
$ flask init-db
Initialized the database.
```

- flaskr/instance dir 내부에 flask.sqlite 생성

</details>

## 2021.02.14

### Blueprints and Views

<details>

<summary>Blueprints and Views</summary>

- view function: application으로 온 요청에 대한 응답을 위한 코드

- request URL과 매칭하기 위해서 Flask는 pattern을 사용한다.

</details>

<details>

<summary>Create a Blueprint</summary>

- blueprint: 뷰와 관련된 코드들을 관리하는 방법

  - 뷰와 코드들을 application에 직접 등록하는 것이 아니라 blueprint에 등록하고 해당 blueprint가 factory function에서 app에 등록된다.

  - Flaskr's blueprint

    1) authentication function

    2) blog post function

- flaskr/auth.py

  1) Blueprint 객체 생성

- flaskr/__init.py__

  1) register_blueprint(): blueprint 객체 등록 - auth.bp

</details>

<details>

<summary>The First View: Register</summary>

- /auth/register에 접근 시 register 뷰 반환

- flaskr/auth.py

  1) register(): /auth/register URL 접근시에 사용자의 username, password를 입력받아 유효성 검사 후 등록한다.

</details>

<details>

<summary>Login</summary>

- flaskr/auth.py

  1) login(): user 정보 확인하여서 로그인 하는 함수. 로그인 후 session에 user_id 등록.

  2) load_logged_in_user(): app request에 대한 함수 실행전에 session을 확인하도록 하는 함수.

  3) logout(): session 정보 삭제하여서 로그아웃 처리.

</details>

<details>

<summary>Require Authentication in Other Views</summary>

- flaskr/auth.py

  1) login_require(): blog post 시에 사용자의 로그인 유무를 확인하는 함수.

</details>

<details>

<summary>Endpoints and URLs</summary>

- endpoint: view와 연결된 이름, URL로 view와 연결되는 이름.

</details>

## 2021.02.15

### Templates

<details>

<summary>Templates</summary>

- template file들은 flaskr 패키지 내부에 templates 디렉터리에 저장된다.

- template

  - statis data와 dynamic data를 위한 placeholder 등을 포함

- Jinja template

  - Flask는 Jinja template library  사용

  - Flask에서 Jinja template은 autoescape로 설정되어서 안전하다.

  - {{ .. }}: output to the final document

  - {% .. %}: control flow (if, for)

</details>

<details>

<summary>The Base Layout</summary>

- app의 각 화면은 각각의 HTML 구조 템플릿을 짜지않고, basic layout을 기반으로 확장하고 오버라이딩해서 사용한다.

- flaskr/templates/base.html

</details>

<details>

<summary>Register</summary>

- flaskr/templates/auth/register.html

</details>

<details>

<summary>Log In</summary>

- flaskr/templates/auth/login.html

</details>

<details>

<summary>Register A User</summary>

- <http://127.0.0.1:5000/auth/register> 과 <http://127.0.0.1:5000/auth/login> 접속

- form 입력하지 않고 register, login 버튼 클릭 시, 에러메시지 출력

  - flash()로 생성한 에러메시지 반환

</details>

## 2021.02.16

### Static Files

<details>

<summary>Static Files</summary>

- Flask는 flaskr/static 디렉토리 아래의 상대주소를 통해서 자동으로 static view들을 사용한다.

- base.html

```python
{{ url_for('static', filename='style.css') }}
```

- flaskr/static/style.css

</details>

### Blog Blueprint

<details>

<summary>Blog Blueprint</summary>

- blog

  - 모든 게시물 조회

  - 로그인한 사용자의 게시물 등록

  - 게시물 저자의 게시물 편집, 삭제

</details>

<details>

<summary>The Blueprint</summary>

- flaskr/blog.py

  1) Blueprint() 객체 생성

- flaskr/__init__.py

  1) blog blueprint, url rule 등록

</details>

<details>

<summary>Index</summary>

- 모든 게시물을 최신순으로 조회하는 화면

- flaskr/blog.py

  - index(): 게시물과 저자의 정보를 출력하는 화면

- flaskr/templates/blog/index.html

</details>

<details>

<summary>Create</summary>

- create view는 register view와 동일하게 동작한다.

- flaskr/blog.py

  1) create: 로그인한 사용자에 대해서 새로운 게시물 등록할 수 있도록 하는 함수

- flaskr/templates/blog/create.html

</details>

<details>

<summary>Update</summary>

- update와 delete는 게시물을 조회하여 사용자와 작성자 일치 여부의 확인이 필요하다.

- flaskr/blog.py

  1) get_post(): 게시물을 조회하여 존재여부, 작성자와 사용자 일치 여부를 확인하여 결과를 반환한다.

  2) update(): 게시물의 id를 입력받아서 해당 게시물을 update한다.

- flaskr/templates/blog/update.html

</details>

<details>

<summary>Delete</summary>

- delete view는 template 따로 존재하지 않는다.

- delete 버튼은 update 화면에 존재하고, 클릭 시 '/<id>/delete' URL로 접근.

- flaskr/blog.py

  1) delete(): 게시물 삭제 후 index 화면으로 이동

</details>

## 2021.02.17

### Make the Project Installable

<details>

<summary>Make the Project Installable</summary>

- project 배포가능하도록 설정.

- 다른 환경에서 해당 프로젝트를 설치하여서 동일하게 동작하도록 설정한다.

</details>

<details>

<summary>Describe thr Project</summary>

- setup.py

  1) 프로젝트, 파일 설명

- MANIFEST.in

  1) static files, templates, sql 등등 프로젝트 파일들을 설명한 파일

</details>

<details>

<summary>Install the Project</summary>

```shell
pip install -e
```

- pip가 setup.py 파일을 찾아서 해당 프로젝트를 editable 모드로 설치한다.

- pip list 명령어로 확인가능

- Tutorial directory가 아니어도 flask run 으로 실행가능

</details>

### Test Coverage

<details>

<summary>Test Coverage</summary>

- application unit code 작성

- pytest, coverage 설치

```shell
pip install pytest coverage
```

</details>

<details>

<summary>Setup and Fixtures</summary>ß

- test 코드들은 tests 디렉토리 아래에 위치한다.

  - tests 디렉토리는 package 디렉토리 내부가 아닌 동일 디렉토리에 위치한다.

- tests/conftest.py

  - fixtures: setup function

- 파이썬 모듈 내부의 모든 테스트, 테스트 함수들은 'test_'로 시작한다.

- tests/data.sql

  - test에서 사용할 데이터들을 삽입하는 sql

</details>

<details>

<summary>Factory</summary>

- tests/test_factory.py

</details>

<details>

<summary>Database</summary>

- tests/test_db.py

</details>

<details>

<summary>Authentication</summary>

- tests/conftest.py

- tests/test_auth.py

</details>

<details>

<summary>Blog</summary>

- tests/test_blog.py

</details>

<details>

<summary>Running the Tests</summary>

- setup.cfg

</details>

## 2021.02.18

### Deploy to Production

<details>

<summary>Build and Install</summary>

- wheel format - Python distribution

- dist 디렉토리 안에 whl파일 생성

```shell
$ pip install wheel
$ python setup.py bdist_wheel
$ pip install flaskr-1.0.0-py3-none-any.whl
# {project name}-{version}-{python tag} -{abi tag}-{platform tag}

# 새로운 환경의 경우 init 실행
$ export FLASK_APP=flaskr
$ flask init-db
```

- Tutorial_deploy 디렉토리에 배포

</details>

<details>

<summary>Configure the Secret Key</summary>

- secret key 생성

```shell
$ python -c 'import os; print(os.urandom(16))'
```

- venv/var/flaskr-instance/config.py 파일 설정

```python
SECRET_KEY = {생성된 KEY}
```

</details>

<details>

<summary>Run with a Production Server</summary>

- Waitress: production WSGI server

```shell
$ pip install waitress
$ waitress-serve --call 'flaskr:create_app'
```

</details>

### Keep Developing

<details>

<summary>Keep Developing!</summary>

- developing ideas

  - A detail view to show a single post. Click a post’s title to go to its page.

  - Like / unlike a post.

  - Comments.

  - Tags. Clicking a tag shows all the posts with that tag.

  - A search box that filters the index page by name.

  - Paged display. Only show 5 posts per page.

  - Upload an image to go along with a post.

  - Format posts using Markdown.

  - An RSS feed of new posts.

</details>
