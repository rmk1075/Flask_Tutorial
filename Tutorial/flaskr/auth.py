import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

'''
1. Blueprint()
- auth: 객체 이름
- __name__: 해당 객체가 선언된 위치
- url_prefix: 해당 blueprint 객체와 관련된 URL의 prefix를 설정
'''
bp = Blueprint('auth', __name__, url_prefix='/auth')


'''
2. @bp.route()
- /auth/register 요청에 대한 view function로 register() 함수를 연계한다
'''
@bp.route('/register', methods=('GET', 'POST'))
def register():
    '''
    3. request.method는 POST이다.
    '''
    if request.method == 'POST':
        '''
        4. request.form
        - dict 타입으로 화면에서 입력한 값의 key, value와 매핑되어있다.
        - 이 화면에서는 사용자의 username, password와 매핑됨.
        '''
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        '''
        5. validation
        - username과 password의 값 존재유무를 validation
        '''
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            '''
            6. db.execute().fetchone()
            - username이 이미 등록되어 있는지 쿼리를 통해서 확인
            - '?' placeholder에 입력으로 받은 username을 대입한다.
            - fetchone(): 쿼리의 결과를 한 row 또는 결과가 없는 경우 None을 반환한다.
            - fetchall(): 쿼리 결과 리스트를 반환한다.
            '''
            error = 'User {} is already registered.'.format(username)

        if error is None:
            '''
            7. generate_password_hash(), db.commit()
            - password를 hash로 암호화하여서 저장하게 한다.
            - db에 commit, 변경내용을 저장한다.
            '''
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()

            '''
            8. login 페이지로 redirect
            - url_for(): 이름을 기반으로 login view URL을 생성한다.
            - redirect(): 해당 URL로의 redirect response 생성
            '''
            return redirect(url_for('auth.login'))

        '''
        9. flash()
        - flash(): template을 렌더링할 때 회수되어지는 메시지를 저장한다.
        '''
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            '''
            10. check_password_hash
            - hash로 암호화되어서 등록된 password에 대해서 매핑을 통해 비교한다.
            '''
            error = 'Incorrect password.'

        if error is None:
            '''
            11. session
            - request로 인한 data를 저장하는 dict 타입 객체
            - session에 user_id 등록
            '''
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

'''
12. before_app_request
- view function이 실행되기 전에 실행하는 함수를 등록한다.
- URL request에 대한 함수 실행 전에 실행
- session에 user_id가 등록되어 있는지 확인한다.
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

'''
13. session clear하여서 로그인 정보 삭제
'''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    '''
    14. functools.wraps()
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
