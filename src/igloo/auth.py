import functools

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from igloo.security import check_password, hash_password


def user(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        request.user = None
    else:
        request.user = request.db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(request, **kwargs):
        if request.user is None:
            return HTTPFound(request.route_url('login'))

        return view(request, **kwargs)

    return wrapped_view


@view_config(route_name='hello')
def hello(request):
    return Response('Hello, World!')


@view_config(
    renderer='auth/login.jinja2',
    request_method=('GET', 'POST'),
    route_name='auth-login',
)
def login(request):
    if request.session.get('user_id'):
        return HTTPFound(request.route_url('index'))

    if request.method == 'POST':
        username = request.params['username']
        password = request.params['password']
        error = None
        user = request.db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            request.session.invalidate()
            request.session['user_id'] = user['id']

            return HTTPFound(request.route_url('index'))

        request.session.flash(error)

    return {}


@view_config(
    request_method=('GET'),
    route_name='auth-logout',
)
def logout(request):
    request.session.invalidate()

    return HTTPFound(request.route_url('index'))


@view_config(
    renderer='auth/register.jinja2',
    request_method=('GET', 'POST'),
    route_name='auth-register',
)
def register(request):
    if request.method == 'POST':
        username = request.params['username']
        password = request.params['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif request.db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            request.registry.db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, hash_password(password))
            )
            request.registry.db.commit()

            return HTTPFound(request.route_url('auth-login'))

        request.session.flash(error)

    return {}
