import pryvate.server
from pryvate.server import app

BASE_DIR = './eggs/'

PRIVATE_EGGS = {}

DB_PATH = '.pryvate.db'

PYPI = 'https://pypi.python.org{}'

pryvate.server.before_request()

pryvate.server.run(host=None,debug=False)