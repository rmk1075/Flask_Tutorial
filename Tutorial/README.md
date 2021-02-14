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