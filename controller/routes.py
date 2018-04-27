from flask import Blueprint, request, render_template
from flask_paginate import Pagination, get_page_parameter
from pyldapi.renderer_register_master import RegisterMasterRenderer
from pyldapi.renderer_register import RegisterRenderer
from pyldapi import decorator
from model.renderer_organization import OrganizationRenderer

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
    """A demo Register of 'Widgets'

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # render response according to view and format parameters
    format = args.get('format')
    description = args.get('description')
    # Use a package of Flask-paginate to manage pagination
    # Total number of records is an import param for pagination, and there is not a fixed way to query it,
    # Expose these page params configuration using flask-paginate may a good choice
    # document url: https://pythonhosted.org/Flask-paginate/
    # github url: https://github.com/lixxu/flask-paginate
    print('print params:', get_page_parameter())
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    pagination = Pagination(page=page, total=21,  record_name='Organisations')
    print('page: ', page, 'per_page', pagination.per_page)
    result = sparql.organisation_query(pagination.page, pagination.per_page)
    print(result.get('results').get('bindings'))
    
    
    # contained_item_class='http://www.w3.org/ns/org#Organization',
    # description='This register contains instances of the org:Organization class.'

    a = RegisterRenderer(result.get('results').get('bindings'), pagination, 'page_register.html', description=description)
    return a.render(format)


@routes.route('/org/<path:organization_id>')
@decorator.instance('/org/<path:organization_id>', OrganizationRenderer)
def organization(**args):
    """A demo 'Widgets' object renderer

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    organization_id = args.get('organization_id')
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    result = sparql.organisatoin_detail(organization_id)
    
    data = result.get('results').get('bindings')[0]
    print(data)
    return OrganizationRenderer(organization_id, data).render(view, format)

@routes.route('/about')
def about(**args):
    return render_template('page_about.html')
