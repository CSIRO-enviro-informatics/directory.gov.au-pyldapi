from os import path

APP_DIR = path.dirname(path.dirname(path.realpath(__file__)))
TEMPLATES_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'view', 'templates')
STATIC_DIR = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'view', 'static')
LOGFILE = APP_DIR + '/flask.log'
DEBUG = True

PAGE_SIZE_DEFAULT = 100
PAGE_SIZE_MAX = 10000

# SPARQL endpoints
SPARQL_AUTH_USR = 'fuseki'
SPARQL_AUTH_PWD = 'problematic'
SPARQL_QUERY_URI = 'http://203.101.226.183/fuseki/orgs/query'
SPARQL_UPDATE_URI = ''
SPARQL_TIMEOUT = 5




