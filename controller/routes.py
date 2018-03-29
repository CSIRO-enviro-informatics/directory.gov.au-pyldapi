from flask import Blueprint, request, render_template
from pyldapi.renderer_register_master import RegisterMasterRenderer
from pyldapi.renderer_register import RegisterRenderer
from pyldapi import decorator
from model.renderer_organization import OrganizationRenderer

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


@routes.route('/org/')
@decorator.register(
    '/org/',
    RegisterRenderer,
    contained_item_class='http://www.w3.org/ns/org#Organization',
    description='This register contains instances of the org:Organization class.'
)
def organizations(**args):
    """A demo Register of 'Widgets'

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    description = args.get('description')
    return RegisterRenderer(request, 'http://www.w3.org/ns/org#Organization', 'http://localhost:5000/widget/', description=description).render(view, format)


@routes.route('/org/<string:organization_id>')
@decorator.instance('/org/<string:organization_id>', OrganizationRenderer)
def organization(**args):
    """A demo 'Widgets' object renderer

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    organization_id = args.get('organization_id')
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    return OrganizationRenderer(organization_id).render(view, format)


@routes.route('/about')
def about(**args):
    return render_template('page_about.html')
