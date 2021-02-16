from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

'''
1. index()
- 모든 게시물을 보여주도록 한다.
- user 테이블과 JOIN을 걸어서 저자 정보를 출력하도록 한다.
'''
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

'''
2. login_required
- auth에서 생성한 decorator를 사용해서 login한 경우에만 접근 가능하도록 설정
'''
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    '''
    3. abort()
    - HTTP 상태코드를 반환하는 특별한 예외상황을 발생
    '''
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    '''
    4. check_author
    - 해당 변수를 통해서 작성자 validation check 실행 여부를 확인하도록 한다.
    '''
    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

'''
5. <int:id>
- id를 입력받는 매개변수 id.
- int:를 설정하지 않을 시 string으로 자동설정된다.
- url_for('blog.update', id=post['id'])
'''
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

'''
6. delete
- POST만 지원하고 index로 redirect
'''
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))