import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

'''
1. app fixture
- factory 호출 후 test config와 test database 설정
'''
@pytest.fixture
def app():
    '''
    2. tempfile.mkstemp()
    - temp file 생성, 열기
    - data path 덮어쓰기 - instance 대신 임시 경로 사용
    - test 종료 후 임시 파일 삭제됨
    '''
    db_fd, db_path = tempfile.mkstemp()

    '''
    3. TESTING
    - Flask에게 application이 test 모드로 실행됨을 알린다.
    '''
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


'''
4. app.test_cliend()
- 서버 실행없이 request를 생성하도록 client 사용
'''
@pytest.fixture
def client(app):
    return app.test_client()

'''
5. app.test_cli_runner()
- app에 등록된 click command를 호출할 수 있도록 한다.
'''
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)