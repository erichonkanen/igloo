from pyramid.httpexceptions import HTTPForbidden, HTTPFound, HTTPNotFound
from pyramid.view import view_config

from igloo.auth import login_required


def get_post(request, id, check_author=True):
    post = request.db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        HTTPNotFound("Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != request.session['user_id']:
        HTTPForbidden()

    return post


@view_config(
    renderer='blog/index.jinja2',
    request_method=('GET'),
    route_name='index',
)
def index(request):
    posts = request.db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return {'posts': posts}


@view_config(
    renderer='blog/create.jinja2',
    request_method=('GET', 'POST'),
    route_name='blog-create',
)
@login_required
def create(request):
    if request.method == 'POST':
        title = request.params['title']
        body = request.params['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            request.session.flash(error)
        else:
            request.db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, request.session['user_id'])
            )
            request.db.commit()

            return HTTPFound(request.route_url('index'))

    return {}


@view_config(
    request_method=('POST'),
    route_name='blog-delete',
)
@login_required
def delete(request):
    id = request.matchdict['id']
    get_post(request, id)
    request.db.execute('DELETE FROM post WHERE id = ?', (id,))
    request.db.commit()

    return HTTPFound(request.route_url('index'))


@view_config(
    renderer='blog/update.jinja2',
    request_method=('GET', 'POST'),
    route_name='blog-update',
)
@login_required
def update(request):
    id = request.matchdict['id']
    post = get_post(request, id)

    if request.method == 'POST':
        title = request.params['title']
        body = request.params['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            request.session.flash(error)
        else:
            request.db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            request.db.commit()

            return HTTPFound(request.route_url('index'))

    return {'post': post}
