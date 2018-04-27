import os.path
from flask import Response, render_template
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Namespace, Literal, BNode
import config as conf
from pyldapi import PYLDAPI
import json
from pyldapi.renderer import Renderer
json.encoder.FLOAT_REPR = lambda f: ("%.2f" % f)


class OrganizationRenderer(Renderer):

    INSTANCE_CLASS = 'http://www.w3.org/ns/org#Organization'
    INSTANCE_URI_BASE = 'http://localhost:5000/widget/'

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

    def __init__(self, instance_id, data):
        """Creates an instance of a Widget from an external dta source, in this case a dummy JSON file
        """
        Renderer.__init__(self)

        self.instance_id = instance_id
        self.creation_date = None
        self.data = data
        # self.load_data(self.widget_id)

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
                        instance_id= self.instance_id, 
                        data= self.data
                    )
                )
            else:
                return Response(self.export_rdf(view, format), mimetype=format)
        elif view == 'dct':
            return self.export_rdf()

    def export_rdf(self, rdf_mime='text/turtle'):
        """
        Exports this instance in RDF, according to a given model from the list of supported models,
        in a given rdflib RDF format

        :param model_view: string of one of the views given in views_formats
        :param rdf_mime: string of one of formats given for this view in views_formats
        :return: RDF string
        """
        # things that are applicable to all model views; the graph and some namespaces
        g = Graph()
        GEO = Namespace('http://www.opengis.net/ont/geosparql#')
        g.bind('geo', GEO)

        # URI for this site
        this_site = URIRef(conf.URI_SITE_INSTANCE_BASE + self.widget_id)
        g.add((this_site, RDF.type, URIRef(self.name)))
        g.add((this_site, RDF.type, URIRef('http://www.w3.org/2002/07/owl#NamedIndividual')))
        g.add((this_site, RDFS.label, Literal('Site ' + self.widget_id, datatype=XSD.string)))
        g.add((this_site, RDFS.comment, Literal(self.description, datatype=XSD.string)))
        site_geometry = BNode()
        g.add((this_site, GEO.hasGeometry, site_geometry))
        g.add((site_geometry, RDF.type, GEO.Geometry))
        g.add((site_geometry, GEO.asWKT, Literal(self._generate_wkt(), datatype=GEO.wktLiteral)))

        return g.serialize(format=PYLDAPI.get_rdf_parser_for_mimetype(rdf_mime))


class ParameterError(ValueError):
    pass
