"""Module for loading a user config.
See conf_template.py for more info.
"""

import os

import six

try:
    # noinspection PyPackageRequirements
    import conf
except ImportError:  # pragma: no cover
    conf = None


def get(attr, default):
    result = os.getenv('HTD_' + attr.upper())
    if result is None:
        result = getattr(conf, attr, None)
    if result is None:
        result = default
    return result


docfiles_dir = get('docfiles_dir', 'hostthedocs/static/docfiles')
docfiles_link_root = get('docfiles_link_root', 'static/docfiles')

copyright = get('copyright', 'Host The Docs')

title = get('title', 'Software documentation')

header = get('header', "<h2>Software documentation</h2>")

host = get('host', '0.0.0.0')
port = int(get('port', 5000))
debug = bool(get('debug', True))
readonly = get('readonly', False)
disable_delete = get('disable_delete', False)
max_content_mb = float(get('max_content_mb', 8))

renderables = dict((k, v) for (k, v) in globals().items() if isinstance(v, six.string_types))


def serve_gevent(app):
    from gevent.wsgi import WSGIServer

    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()


def serve_flask(app):
    app.run(host, port, debug)


def calc_serve(serve_from_conf, gevent_module, debug_from_conf, wsgi_server_from_conf):
    if serve_from_conf is not None:
        return serve_from_conf

    if debug_from_conf:
        default_wsgi = 'flask'
    elif gevent_module is not None:
        default_wsgi = 'gevent'
    else:
        default_wsgi = 'flask'

    wsgi_server = wsgi_server_from_conf or default_wsgi
    servefunc = {
        'gevent': serve_gevent,
        'flask': serve_flask}[wsgi_server]
    return servefunc


def _calc_serve():
    try:
        import gevent
    except ImportError:
        gevent = None
    return calc_serve(get('serve', None), gevent, debug, get('wsgi_server', None))

serve = _calc_serve()
