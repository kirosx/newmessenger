from logging import basicConfig, getLogger, DEBUG

basicConfig(
    filename='logs.txt',
    format='%(levelname)s %(asctime)s %(message)s',
    level=DEBUG
)
log = getLogger('basic')


def logger_decorator(string):
    warning = {
        'info': log.info,
        'warning': log.warning,
        'debug': log.debug,
        'critical': log.critical

    }

    def real_decorator(func):
        def wrap(*args):
            func(*args)
            warning[string](f'{func.__name__} {args}')
        return wrap
    return real_decorator
