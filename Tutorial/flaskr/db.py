import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    '''
    1. g object
    - 각 request에 대한 unique object
    - 요청동안 접근되는 다양한 데이터를 저장하는데 사용된다.
    - 동일한 요청에 대해서 get_db()가 호출되는 경우 db 연결을 재생성하지 않고 재사용한다.
    '''
    if 'db' not in g:
        '''
        2. current_app
        - 해당 request에서 다루는 Flask application를 가리키는 object
        - application factory를 사용하는 경우, 더이상 application obejct를 직접생성하지 않고 get_db()를 호출해서 사용한다.

        3. sqlite3.connect()
        - database configuration key가 가리키는 database와의 connection을 생성한다.
        '''
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        '''
        4. sqlite3.Row
        - dict타입 처럼 동작하는 row를 반환하도록 한다.
        - column의 이름으로 접근을 허용한다.
        '''
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    '''
    - db연결이 존재 여부 확인 후 close()
    '''
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    '''
    5. open_resource()
    - flaskr 패키지에 대한 상대주소를 통해서 파일 열기
    '''
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

'''
6. click.command()
- command line command init-db를 정의한다.
'''
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    '''
    7. app.teardown_appcontext()
    - response 후 정리시에 close_db() 함수를 호출하도록 설정
    '''
    app.teardown_appcontext(close_db)

    '''
    8. app.cli.add_command(): flask 명령으로 호출할 수 있는 새로운 cli 명령어 등록
    '''
    app.cli.add_command(init_db_command)