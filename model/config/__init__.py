from os.path import dirname, realpath, join, abspath

APP_DIR = dirname(dirname(realpath(__file__)))
TEMPLATES_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'templates')
STATIC_DIR = join(dirname(dirname(abspath(__file__))), 'view', 'static')
LOGFILE = APP_DIR + '/flask.log'
DEBUG = True

SPARQL_AUTH_USR = 'fuseki'
SPARQL_AUTH_PWD = 'problematic'
SPARQL_QUERY_URI = 'http://203.101.226.183/fuseki/orgs/query'
