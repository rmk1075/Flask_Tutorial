import os

from flask import Flask

# application factory function
def create_app(test_config=None):
    '''
    1. Flask instance 생성한다.
    - __name__: 현재 파이썬 모듈의 이름. 위치 설정에서 유용하게 쓰인다.
    - instance_relative_config=True: 설정파일에 상대경로를 사용할 수 있도록 한다.
    '''
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    '''
    2. app의 기본 설정
    - SECRET_KEY: Flak 및 extension의 데이터를 안전하게 유지하는데 사용된다.
    - DATABASE: SQLite 파일이 저장될 위치를 설정. app.instance_path (Flask의 인스턴스 폴더 경로) 아리에 저장된다.
    '''
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        '''
        3. config.py의 값으로 설정 재정의
        - config.py 파일이 있는 경우 해당 파일의 값으로 설정한다.
        - 실제 개발 인스턴스 설정과 테스트 설정을 독립적으로 설정하여 사용할 수 있다. - config.py & test_config
        '''
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        '''
        4. app.instance_path 디렉토리를 생성한다.
        '''
        os.makedirs(app.instance_path)
    except OSError:
        pass

    '''
    5. URL/hello 요청에 대한 연결 생성
    - 'Hello, World!'를 반환
    '''
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    return app