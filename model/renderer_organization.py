import os.path
from flask import Response, render_template, request
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Namespace, Literal, BNode
import config as conf
from pyldapi import PYLDAPI
import json
from pyldapi.renderer import Renderer
json.encoder.FLOAT_REPR = lambda f: ("%.2f" % f)


class OrganizationRenderer(Renderer):

    INSTANCE_CLASS = 'http://www.w3.org/ns/org#Organization'

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

    def __init__(self, organization_id, organisation):
        """Creates an instance of a Widget from an external dta source, in this case a dummy JSON file
        """
        Renderer.__init__(self)

        self.organization_id = organization_id
        self.creation_date = None
        self.organisation = organisation
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
                        'page_organisation.html',
                        organization_id= self.organization_id, 
                        organisation= self.organisation
                    )
                )
            else:
                return Response(self.export_rdf(format), mimetype=format)
        elif view == 'dct':
            return Response(self.export_rdf(format), mimetype=format)

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
        this_site = URIRef(self.site_url + self.organization_id)
        # g.add((this_site, RDF.type, URIRef(self.organisation.label)))
        g.add((this_site, RDF.type, URIRef('http://www.w3.org/2002/07/owl#NamedIndividual')))
        g.add((this_site, RDFS.label, Literal(self.organisation.get('label'), datatype=XSD.string)))
        g.add((this_site, RDFS.comment, Literal(self.organisation.get('description'), datatype=XSD.string)))
        site_geometry = BNode()
        g.add((this_site, GEO.hasGeometry, site_geometry))
        g.add((site_geometry, RDF.type, GEO.Geometry))
        # g.add((site_geometry, GEO.asWKT, Literal(self._generate_wkt(), datatype=GEO.wktLiteral)))
        g.add((site_geometry, GEO.asWKT, Literal('', datatype=GEO.wktLiteral)))
        return g.serialize(format=PYLDAPI.get_rdf_parser_for_mimetype(rdf_mime))

class ParameterError(ValueError):
    pass
