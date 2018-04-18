from flask import Blueprint, request, render_template
from pyldapi.renderer_register_master import RegisterMasterRenderer
from pyldapi.renderer_register import RegisterRenderer
from pyldapi import decorator
from model.renderer_organization import OrganizationRenderer
import model.sparql as sparql

routes = Blueprint('controller', __name__)


@routes.route('/')
@decorator.register('/', RegisterMasterRenderer)
def index(**args):
    """The master Register of Registers and also the home page of this API instance

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    return RegisterMasterRenderer(request, 'page_index.html', decorator.register_tree).render(view, format)


@routes.route('/board/')
@decorator.register(
    '/board/',
    RegisterRenderer,
    contained_item_class='http://test.linked.data.gov.au/def/auorg#Board',
    description='This register contains instances of the org:Organization class.'
)
def boards(**args):
    """A Register of Organisations

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    r = RegisterRenderer(
        request,
        'http://test.linked.data.gov.au/def/auorg#Board',
        'http://localhost:5000/board/',
        description=args.get('description'))

    # translate pagination vars to query
    limit = r.per_page
    offset = (r.page - 1) * r.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a <http://test.linked.data.gov.au/def/auorg#Board> ;
               rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    r.register = []
    orgs = sparql.query(q)['results']['bindings']
    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        r.register.append((o, l))

    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')

    return r.render(view, format)


@routes.route('/org/')
@decorator.register(
    '/org/',
    RegisterRenderer,
    contained_item_class='http://www.w3.org/ns/org#Organization',
    description='This register contains instances of the org:Organization class.'
)
def organizations(**args):
    """A Register of org:Organizations

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    r = RegisterRenderer(
        request,
        'http://www.w3.org/ns/org#Organization',
        'http://localhost:5000/org/',
        description=args.get('description'))

    # translate pagination vars to query
    limit = r.per_page
    offset = (r.page - 1) * r.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a <http://www.w3.org/ns/org#Organization> ;
               rdfs:label ?label .
          MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectorySubStructure> }}
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    r.register = []
    orgs = sparql.query(q)['results']['bindings']
    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        r.register.append((o, l))

    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')

    return r.render(view, format)


@routes.route('/person/')
@decorator.register(
    '/person/',
    RegisterRenderer,
    contained_item_class='http://xmlns.com/foaf/0.1/Person',
    description='This register contains people.'
)
def persons(**args):
    """A Register of People'

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    r = RegisterRenderer(
        request,
        'http://xmlns.com/foaf/0.1/Person',
        'http://localhost:5000/person/',
        description=args.get('description'))

    # translate pagination vars to query
    limit = r.per_page
    offset = (r.page - 1) * r.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a <http://xmlns.com/foaf/0.1/Person> ;
               rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    r.register = []
    orgs = sparql.query(q)['results']['bindings']
    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        r.register.append((o, l))

    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')

    return r.render(view, format)


@routes.route('/portfolio/')
@decorator.register(
    '/portfolio/',
    RegisterRenderer,
    contained_item_class='http://test.linked.data.gov.au/def/auorg#Portfolio',
    description='This register contains Portfolios.'
)
def portfolios(**args):
    """A Register of Portfolios'

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    r = RegisterRenderer(
        request,
        'http://test.linked.data.gov.au/def/auorg#Portfolio',
        'http://localhost:5000/portfolio/',
        description=args.get('description'))

    # translate pagination vars to query
    limit = r.per_page
    offset = (r.page - 1) * r.per_page

    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a <http://test.linked.data.gov.au/def/auorg#Portfolio> ;
               rdfs:label ?label .
        }}
        ORDER BY ?label
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    r.register = []
    orgs = sparql.query(q)['results']['bindings']
    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        r.register.append((o, l))

    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')

    return r.render(view, format)


# @routes.route('/org/<string:organization_id>')
# @decorator.instance('/org/<string:organization_id>', OrganizationRenderer)
# def organization(**args):
#     """A demo 'Widgets' object renderer
#
#     :param args: supplied by decorator
#     :return: a Flask HTTP Response
#     """
#     organization_id = args.get('organization_id')
#     # render response according to view and format parameters
#     view = args.get('view')
#     format = args.get('format')
#     return OrganizationRenderer(organization_id).render(view, format)


@routes.route('/about')
def about(**args):
    return render_template('page_about.html')
