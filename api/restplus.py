from flask_restx import Api
from rq import Queue
from worker import conn, timeout
from sqlalchemy.orm.exc import NoResultFound
from config import settings

api = Api(version='1.0', title='Sputnik Pricing Engine',
          description='Method for projecting returns for fixed income.')
q = Queue(connection=conn, default_timeout=timeout)

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    return {'message': 'A database result was required but none was found.'}, 404
