from flask import Blueprint, request, render_template
from flask_paginate import Pagination, get_page_parameter
from pyldapi.renderer_register_master import RegisterMasterRenderer
from pyldapi.renderer_register import RegisterRenderer
from pyldapi import decorator
from model.renderer_organization import OrganizationRenderer
import model.sparql as sparql

from model import sparql

routes = Blueprint('controller', __name__)

@routes.route('/')
@decorator.register('/', RegisterMasterRenderer)
def index(**args):
    """The master Register of Registers and also the home page of this API instance

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # render response according to view and format parameters
    # alternates view is handled by the pyldapi, no view param required
    format = args.get('format')
    return RegisterMasterRenderer( decorator.register_tree, 'page_index.html',).render(format)


@routes.route('/org/')
@decorator.register(
    '/org/',
    RegisterRenderer,
    description='This register contains instances of the org:Organization class.'
)
def organizations(**args):
    """A Register of org:Organizations
    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # Use a package of Flask-paginate to manage pagination
    # Total number of records is an important param for pagination
    # document url: https://pythonhosted.org/Flask-paginate/
    # github url: https://github.com/lixxu/flask-paginate
    per_page = request.args.get('per_page', type=int, default=20)
    page = request.args.get('page', type=int, default=1)
    total_organisation = sparql.total_organisation()

    pagination = Pagination(page=page, total=total_organisation, per_page=per_page, record_name='Organisations')

    # translate pagination vars to query
    limit = pagination.per_page
    offset = (pagination.page -1)*pagination.per_page
    
    # get list of org URIs and labels from the triplestore
    q = '''
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX org: <http://www.w3.org/ns/org#>
        SELECT ?uri ?label
        WHERE {{
          ?uri a org:Organization ;
               rdfs:label ?label.
          MINUS {{ ?uri a <http://test.linked.data.gov.au/def/auorg#DirectorySubStructure> }}
        }}
        LIMIT {}
        OFFSET {}
    '''.format(limit, offset)
    register = []
    orgs = sparql.query(q)['results']['bindings']

    for org in orgs:
        o = str(org['uri']['value'])
        l = str(org['label']['value'])
        register.append((o, l))

    format = args.get('format')
    r = RegisterRenderer(
        register,
        pagination,
        'page_register.html',
        'http://www.w3.org/ns/org#Organization',
        description=args.get('description'))

    # render response according to format parameter
    return r.render(format)


@routes.route('/org/<path:organization_id>')
@decorator.instance('/org/<path:organization_id>', OrganizationRenderer)
def organization(**args):
    """A demo 'Widgets' object renderer
    """
    view = args.get('view')
    format = args.get('format')
    organization_id = args.get('organization_id')
    # print(organization_id)
    result = sparql.organisatoin_detail(organization_id)
    
    
    if result.get('results').get('bindings'):
        data = result.get('results').get('bindings')[0]
    else:
        data = {}
    organisation = {}
    organisation['label'] = data.get('label').get('value') if data.get('label') else ''
    organisation['create'] = data.get('create').get('value')  if data.get('create') else ''
    organisation['description'] = data.get('description').get('value')  if data.get('description') else ''
    organisation['link'] = data.get('link').get('value')  if data.get('link') else ''
    # print('organisation', organisation)
    return OrganizationRenderer(organization_id, organisation).render(view, format)

# @routes.route('/board/')
# @decorator.register(
#     '/board/',
#     RegisterRenderer,
#     contained_item_class='http://test.linked.data.gov.au/def/auorg#Board',
#     description='This register contains instances of the org:Organization class.'
# )

# def boards(**args):
#     """A Register of Organisations

#     :param args: supplied by decorator
#     :return: a Flask HTTP Response
#     """
#     r = RegisterRenderer(
#         request,
#         'http://test.linked.data.gov.au/def/auorg#Board',
#         'http://localhost:5000/board/',
#         description=args.get('description'))

#     # translate pagination vars to query
#     limit = r.per_page
#     offset = (r.page - 1) * r.per_page

#     # get list of org URIs and labels from the triplestore
#     q = '''
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#         PREFIX org: <http://www.w3.org/ns/org#>
#         SELECT ?uri ?label
#         WHERE {{
#           ?uri a <http://test.linked.data.gov.au/def/auorg#Board> ;
#                rdfs:label ?label .
#         }}
#         ORDER BY ?label
#         LIMIT {}
#         OFFSET {}
#     '''.format(limit, offset)
#     r.register = []
#     orgs = sparql.query(q)['results']['bindings']
#     for org in orgs:
#         o = str(org['uri']['value'])
#         l = str(org['label']['value'])
#         r.register.append((o, l))

#     # render response according to view and format parameters
#     view = args.get('view')
#     format = args.get('format')

#     return r.render(view, format)


# @routes.route('/person/')
# @decorator.register(
#     '/person/',
#     RegisterRenderer,
#     contained_item_class='http://xmlns.com/foaf/0.1/Person',
#     description='This register contains people.'
# )
# def persons(**args):
#     """A Register of People'

#     :param args: supplied by decorator
#     :return: a Flask HTTP Response
#     """
#     format = args.get('format')
#     description = args.get('description')
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     pagination = Pagination(page=page, total=21,  record_name='Organisations')

#     # translate pagination vars to query
#     limit = pagination.per_page
#     offset = (pagination.page -1)*pagination.per_page

#     # get list of org URIs and labels from the triplestore
#     q = '''
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#         PREFIX org: <http://www.w3.org/ns/org#>
#         SELECT ?uri ?label
#         WHERE {{
#           ?uri a <http://xmlns.com/foaf/0.1/Person> ;
#                rdfs:label ?label .
#         }}
#         ORDER BY ?label
#         LIMIT {}
#         OFFSET {}
#     '''.format(limit, offset)
#     register = []
#     orgs = sparql.query(q)['results']['bindings']
#     for org in orgs:
#         o = str(org['uri']['value'])
#         l = str(org['label']['value'])
#         register.append((o, l))
#     r = RegisterRenderer(
#         register,
#         pagination,
#         'page_register.html',
#         'http://xmlns.com/foaf/0.1/Person',
#         description=description)
#     return r.render(format)



# @routes.route('/portfolio/')
# @decorator.register(
#     '/portfolio/',
#     RegisterRenderer,
#     contained_item_class='http://test.linked.data.gov.au/def/auorg#Portfolio',
#     description='This register contains Portfolios.'
# )
# def portfolios(**args):
#     """A Register of Portfolios'

#     :param args: supplied by decorator
#     :return: a Flask HTTP Response
#     """
#     r = RegisterRenderer(
#         request,
#         'http://test.linked.data.gov.au/def/auorg#Portfolio',
#         'http://localhost:5000/portfolio/',
#         description=args.get('description'))

#     # translate pagination vars to query
#     limit = r.per_page
#     offset = (r.page - 1) * r.per_page

#     # get list of org URIs and labels from the triplestore
#     q = '''
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#         PREFIX org: <http://www.w3.org/ns/org#>
#         SELECT ?uri ?label
#         WHERE {{
#           ?uri a <http://test.linked.data.gov.au/def/auorg#Portfolio> ;
#                rdfs:label ?label .
#         }}
#         ORDER BY ?label
#         LIMIT {}
#         OFFSET {}
#     '''.format(limit, offset)
#     r.register = []
#     orgs = sparql.query(q)['results']['bindings']
#     for org in orgs:
#         o = str(org['uri']['value'])
#         l = str(org['label']['value'])
#         r.register.append((o, l))

#     # render response according to view and format parameters
#     view = args.get('view')
#     format = args.get('format')

#     return r.render(view, format)

@routes.route('/about')
def about(**args):
    return render_template('page_about.html')