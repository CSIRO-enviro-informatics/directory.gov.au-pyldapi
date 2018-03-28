from flask import Blueprint, request
from pyldapi.renderer_register_master import RegisterMasterRenderer
from pyldapi.renderer_register import RegisterRenderer
from pyldapi import decorator
from model.renderer_widget import WidgetRenderer

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


@routes.route('/wiget/')
@decorator.register(
    '/wiget/',
    RegisterRenderer,
    contained_item_class=['http://example.com/ex#Widget'],
    description='This register contains instances of a dummy Widget class.'
)
def widgets(**args):
    """A demo Register of 'Widgets'

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    description = args.get('description')
    return RegisterRenderer(request, 'http://example.org/def/widgets#Widget', 'http://localhost:5000/widget/', description=description).render(view, format)


@routes.route('/widget/<string:widget_id>')
@decorator.instance('/widget/<string:widget_id>', WidgetRenderer)
def widget(**args):
    """A demo 'Widgets' object renderer

    :param args: supplied by decorator
    :return: a Flask HTTP Response
    """
    widget_id = args.get('widget_id')
    # render response according to view and format parameters
    view = args.get('view')
    format = args.get('format')
    return WidgetRenderer(widget_id).render(view, format)
