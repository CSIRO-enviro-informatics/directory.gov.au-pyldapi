import os.path
from flask import Response
import jinja2
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Literal
import json
from .pyldapi import PYLDAPI
from .renderer import Renderer
json.encoder.FLOAT_REPR = lambda f: ("%.2f" % f)

class WidgetRenderer(Renderer):

    INSTANCE_CLASS = 'http://example.org/def/widgets#Widget'

    @staticmethod
    def views_formats(description=None):
        return {
            'default': 'widgont',
            'alternates': {
                'mimetypes': [
                    'text/html',
                    'text/turtle',
                    'application/rdf+xml',
                    'application/rdf+json',
                    'application/json'
                ],
                'default_mimetype': 'text/html',
                'namespace': 'http://www.w3.org/ns/ldp#Alternates',
                'description': 'The view listing all other views of this class of object'
            },
            'dct': {
                'mimetypes': [
                    'text/turtle',
                    'application/rdf+xml',
                    'application/rdf+json',
                    'application/json'
                ],
                'default_mimetype': 'text/turtle',
                'namespace': 'http://purl.org/dc/terms/',
                'description': 'A simple Dublin Core Terms view, RDF formats only'
            },
            'widgont': {
                'mimetypes': ['text/html', 'text/turtle', 'application/rdf+xml', 'application/rdf+json'],
                'default_mimetype': 'text/html',
                'namespace': 'http://pid.geoscience.gov.au/def/ont/vanilla/pdm#',
                'description': 'A dummy Widget Ontology view'
            },
            'description': 'Renderer for Widget instances'
        }

    def __init__(self, widget_id, widget):
        """Creates an instance of a Widget from an external dta source, in this case a dummy JSON file
        """
        Renderer.__init__(self)

        self.widget_id = widget_id
        self.creation_date = None
        # widget is a dict of widget {name: '', create: '', description: ''}
        self.widget = widget
        self.site_url = request.base_url

    def render(self, view, format):
        """The required function used to determine how to create a rendering for each enabled view and format

        :param view: he selected view to render
        :param format: the selected format to render
        :return:
        """
        # each view and format handled
        if view == 'widgont':  # a fake 'widgont' (Widget Ontology) view
            if format == 'text/html':
                 return Response(
                    render_template(
                        'page_widget.html',
                        widget_id= self.widget_id, 
                        widget= self.widget
                    )
                )
            else:
                return Response(self.export_rdf(format), mimetype=format)
        elif view == 'dct':
            return Response(self.export_rdf(format), mimetype=format)

    def render_rdf(self, format='text/turtle'):
        """
        Exports this instance in RDF, according to a given model from the list of supported models,
        in a given rdflib RDF format

        :param view: string of one of the views given in views_formats
        :param format: string of one of formats given for this view in views_formats
        :return: RDF string
        """
        # no need to handle other views as there are none and no need to handle a default case (else) as the PYLDAPI
        # modules does all that for you
        if view == 'widgont':
            g = Graph()
            this_widget = URIRef(self.base_url)
            g.add((this_widget, RDF.type, URIRef(self.INSTANCE_CLASS)))
            g.add((this_widget, RDFS.label, Literal(self.widget.get('name'), datatype=XSD.string)))
            g.add((this_widget, RDFS.comment, Literal(self.widget.get('description'), datatype=XSD.string)))

            return g.serialize(format=PYLDAPI.get_rdf_parser_for_mimetype(format))
