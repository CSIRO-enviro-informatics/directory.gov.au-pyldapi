import os.path
from abc import ABCMeta
from flask import render_template, Response, request
import jinja2
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Namespace, Literal
from .pyldapi import PYLDAPI
from .renderer import Renderer


class RegisterMasterRenderer(Renderer):
    __metaclass__ = ABCMeta

    def __init__(self, register_tree, template):
        Renderer.__init__(self)
        self.register_uri = request.base_url
        self.uri = 'http://purl.org/linked-data/registry#Register'
        self.template = template
        self.g = None
        self.register_tree = register_tree
        # self.paging_params()
    def render(self, mimetype):
        """This method must be implemented by all classes that inherit from Renderer

        :param view: a model view available for this class instance
        :param mimetype: a mimetype string, e.g. text/html
        :return: a Flask Response object
        """
        # alternates view is handled by the pyldapi
        if mimetype == 'text/html':
            return render_template(self.template, register_tree=self.register_tree)
        else:
            self._make_reg_graph()
            rdflib_format = PYLDAPI.get_rdf_parser_for_mimetype(mimetype)
            return Response(
                self.g.serialize(format=rdflib_format),
                status=200,
                mimetype=mimetype
            )
            
    @staticmethod
    def views_formats(description=None):
        """
        return this register's supported views and mimetypes for each view
        """
        return {
            'default': 'reg',
            'alternates': {
                'mimetypes': [
                    'text/html', 'text/turtle', 'application/rdf+xml', 'application/rdf+json', 'application/json'],
                'default_mimetype': 'text/html',
                'namespace': 'http://www.w3.org/ns/ldp#Alternates',
                'description': 'The view listing all other views of this class of object'
            },
            'reg': {
                'mimetypes': ['text/html', 'text/turtle', 'application/rdf+xml', 'application/rdf+json'],
                'default_mimetype': 'text/html',
                'namespace': 'http://purl.org/linked-data/registry#',
                'description':
                    'The Registry Ontology. Core ontology for linked data registry services. Based on ISO19135 but '
                    'heavily modified to suit Linked Data representations and applications',
                'containedItemClass': 'http://purl.org/linked-data/registry#Register'
            },
            'description':
                'This is the Master Register containing all the registers within this Linked Data API.'
        }
    def _make_reg_graph(self):
        self.g = Graph()
        # make the static part of the graph
        REG = Namespace('http://purl.org/linked-data/registry#')
        self.g.bind('reg', REG)

        LDP = Namespace('http://www.w3.org/ns/ldp#')
        self.g.bind('ldp', LDP)

        XHV = Namespace('https://www.w3.org/1999/xhtml/vocab#')
        self.g.bind('xhv', XHV)
        print('self.register_uri', self.register_uri)
        register_uri = URIRef(self.register_uri)
        self.g.add((register_uri, RDF.type, REG.Register))
        self.g.add((register_uri, RDFS.label, Literal('Register', datatype=XSD.string)))

        # add all the items
        for register in self.register_tree:
            if '#' in register.get('contained_item_class'):
                label = register.get('contained_item_class').split('#')[1]
            else:
                label = register.get('contained_item_class').split('/')[-1]

            item_uri = URIRef(self.register_uri + register.get('uri')[1:])
            print('item_uri', item_uri)
            self.g.add((item_uri, RDF.type, URIRef('http://purl.org/linked-data/registry#Register')))
            self.g.add((item_uri, RDFS.label, Literal('Register of ' + label + 's', datatype=XSD.string)))
            self.g.add((item_uri, RDFS.comment, Literal(register.get('description'), datatype=XSD.string)))
            self.g.add((item_uri, REG.register, URIRef(item_uri)))
            self.g.add((item_uri, REG.containedItemClass, URIRef(register.get('contained_item_class'))))