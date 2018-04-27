import os.path
from abc import ABCMeta
import jinja2
from flask import Response, render_template, request
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Namespace, Literal
import math
from .pyldapi import PYLDAPI
from .renderer import Renderer


class RegisterRenderer(Renderer):
    __metaclass__ = ABCMeta

    def __init__(self, instances, pagination,  template,  description=None):
        Renderer.__init__(self)

        self.base_url=request.base_url
        self.register_uri = self.base_url
        self.description = description
        self.pagination = pagination
        self.template = template
        self.page = pagination.page if pagination.page is not None else 1
        self.per_page = pagination.per_page if pagination.per_page is not None else 10
        self.last_page = math.ceil(pagination.total/pagination.per_page) +1
        self.g = None
        self.instances = instances


    @staticmethod
    def views_formats(description=None):
        return {
            'default': 'reg',
            'alternates': {
                'mimetypes':
                    ['text/html', 'text/turtle', 'application/rdf+xml', 'application/rdf+json', 'application/json'],
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
            },
            'description':
                description
        }

    def render(self, format):
        # is an RDF format requested?
        if format in PYLDAPI.get_rdf_mimetypes_list():
            return Response(
                self.render_rdf(format),
                status=200,
                mimetype=format
            )
        elif format == 'text/html':
            # html = self.render_html(
            #     os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dummy_files', self.template),
            #     context
            # )
            # return Response(html, headers=self.headers)
            return render_template(self.template,  
                base_url=self.base_url,
                instances=self.instances,
                pagination=self.pagination)

    def render_html(self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(path or './')
        ).get_template(filename).render(context)

    def render_rdf(self, format):
        g = Graph()

        REG = Namespace('http://purl.org/linked-data/registry#')
        g.bind('reg', REG)

        LDP = Namespace('http://www.w3.org/ns/ldp#')
        g.bind('ldp', LDP)

        XHV = Namespace('https://www.w3.org/1999/xhtml/vocab#')
        g.bind('xhv', XHV)

        register_uri = URIRef(self.register_uri)
        g.add((register_uri, RDF.type, REG.Register))
        g.add((register_uri, RDFS.label, Literal('Register', datatype=XSD.string)))

        page_uri_str = self.register_uri
        if self.per_page is not None:
            page_uri_str += '?per_page=' + str(self.per_page)
        else:
            page_uri_str += '?per_page=100'
        page_uri_str_no_page_no = page_uri_str + '&page='
        if self.page is not None:
            page_uri_str += '&page=' + str(self.page)
        else:
            page_uri_str += '&page=1'
        page_uri = URIRef(page_uri_str)

        # pagination
        # this page
        g.add((page_uri, RDF.type, LDP.Page))
        g.add((page_uri, LDP.pageOf, register_uri))

        # links to other pages
        g.add((page_uri, XHV.first, URIRef(page_uri_str_no_page_no + '1')))
        g.add((page_uri, XHV.last, URIRef(page_uri_str_no_page_no + str(self.last_page))))

        if self.page != 1:
            g.add((page_uri, XHV.prev, URIRef(page_uri_str_no_page_no + str(self.page - 1))))

        if self.page != self.last_page:
            g.add((page_uri, XHV.next, URIRef(page_uri_str_no_page_no + str(self.page + 1))))

        # add all the items
        for item in self.instances:
            if isinstance(item, tuple):  # if it's a tuple, add in the label
                item_uri = URIRef(item[0])
                g.add((item_uri, RDF.type, URIRef(self.base_url)))
                g.add((item_uri, RDFS.label, Literal(item[1], datatype=XSD.string)))
                g.add((item_uri, REG.register, page_uri))
            else:  # just URIs
                item_uri = URIRef(item)
                g.add((item_uri, RDF.type, URIRef(self.base_url)))
                g.add((item_uri, REG.register, page_uri))

        # serialize the RDF in whichever format was selected by the user, after converting from mimtype
        return g.serialize(format=PYLDAPI.get_rdf_parser_for_mimetype(format))
