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

</deatils>

### Application Setup

- Flask application은 Flask class의 인스턴스로 설정과 URL등이 모두 클래스에 등록되어있다.

- Flask 인스턴스를 글로벌하게 만드는 것은 프로젝트 규모가 커져가면서 문제를 야기할 수 있기 때문에 함수를 통해서 인스턴스를 생성할 것이다.

  - application factory

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