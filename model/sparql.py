import requests
import json
import config as conf


def query(sparql_query, format_mimetype='application/sparql-results+json'):
    """ Make a SPARQL query"""
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    data = {'query': sparql_query}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': format_mimetype
    }
    try:
        r = requests.post(conf.SPARQL_QUERY_URI, auth=auth, data=data, headers=headers, timeout=1)
        # print(r.text)
        return json.loads(r.content.decode('utf-8'))
    except Exception as e:
        raise e


def query_turtle(sparql_query):
    """ Make a SPARQL query with turtle format response"""
    data = {'query': sparql_query, 'format': 'text/turtle'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    r = requests.post(conf.SPARQL_QUERY_URI, data=data, auth=auth, headers=headers, timeout=1)
    try:
        return r.content
    except Exception as e:
        raise


def insert(g, named_graph_uri=None):
    """ Securely insert a named graph into the DB"""
    if named_graph_uri is not None:
        data = {'update': 'INSERT DATA { GRAPH <' + named_graph_uri + '> { ' + g.serialize(format='nt').decode('utf-8') + ' } }'}
    else:  # insert into default graph
        data = {'update': 'INSERT DATA { ' + g.serialize(format='nt') + ' }'}
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    headers = {'Accept': 'text/turtle'}
    try:
        r = requests.post(conf.SPARQL_UPDATE_URI, headers=headers, data=data, auth=auth, timeout=1)
        if r.status_code != 200 and r.status_code != 201:
            raise Exception('The INSERT was not successful. The SPARQL _database\' error message is: ' + r.content)
        return True
    except requests.ConnectionError as e:
        print(str(e))
        raise Exception()


def update(sparql_update_query, format_mimetype='application/sparql-results+json'):
    """ Make a SPARQL update"""
    auth = (conf.SPARQL_AUTH_USR, conf.SPARQL_AUTH_PWD)
    data = {'update': sparql_update_query}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': format_mimetype
    }
    try:
        r = requests.post(conf.SPARQL_UPDATE_URI, auth=auth, data=data, headers=headers, timeout=1)
        return r.text
    except Exception as e:
        raise e

def organisation_query(start, limit):
    orgs = '''
        PREFIX org: <http://www.w3.org/ns/org#>
        PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
       SELECT ?org ?label
       WHERE {
           ?org a org:Organization.
           ?org rdfs:label ?label.
       }
       ''' + 'OFFSET ' + str(start) + 'LIMIT ' + str(limit)
    return query(orgs)
def organisatoin_detail(org):
    org = '<'+org+'>'
    detailAnOrg ='PREFIX org: <http://www.w3.org/ns/org#> \
       PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
       SELECT  ?label ?create ?description ?link \
       WHERE { \
           %s a org:Organization. \
            OPTIONAL {  %s rdfs:label ?label } \
            OPTIONAL {  %s <http://purl.org/dc/terms/created> ?create }\
            OPTIONAL {  %s <http://purl.org/dc/terms/description> ?description } \
            OPTIONAL {  %s  <http://www.w3.org/2002/07/owl#seeAlso> ?link } \
       } \
    ' % (org, org,org,org,org)
    # print(detailAnOrg)
    return query(detailAnOrg)
if __name__ == '__main__':
    organisations = organisation_query(0, 10)
    # print(organisations)
    # print(organisations.get('results').get('bindings')[0].get('org').get('value'))
    print(organisatoin_detail(organisations.get('results').get('bindings')[3].get('org').get('value')))
    #
    # test_query = "PREFIX org: <http://www.w3.org/ns/org#> \
    #    PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#> \
    #    SELECT  ?label ?create ?description ?link \
    #    WHERE { \
    #        %s a org:Organization. \
    #         OPTIONAL {  %s rdfs:label ?label } \
    #         OPTIONAL {  %s <http://purl.org/dc/terms/created> ?create }\
    #         OPTIONAL {  %s <http://purl.org/dc/terms/description> ?description } \
    #         OPTIONAL {  %s  <http://www.w3.org/2002/07/owl#seeAlso> ?link } \
    #    } \
    # " % ('<http://test.linked.data.gov.au/dataset/auorg/directoryRole/D-02130>','<http://test.linked.data.gov.au/dataset/auorg/directoryRole/D-02130>','<http://test.linked.data.gov.au/dataset/auorg/directoryRole/D-02130>','<http://test.linked.data.gov.au/dataset/auorg/directoryRole/D-02130>','<http://test.linked.data.gov.au/dataset/auorg/directoryRole/D-02130>')
    # print(test_query)
    # print(query(test_query))

