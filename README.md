# directory.gov.au Linked Data API

This repository is for the Linked Data API version of <http://directory.gov.au>. It generates [RDF](https://www.w3.org/2001/sw/wiki/RDF) versions of items in directory.gov.au and serves them at persistent URI endpoints.

This API is an implementation of [pyLDAPI](https://pypi.org/project/pyldapi/), a Python Linked Data API tool. This particular instance uses directory.gov.au content converted to RDF by the [directory.gov.au Linked Data generator](https://github.com/AGLDWG/directory.gov.au-ld-generator) tool from the [XML export](https://data.gov.au/dataset/directory-gov-au-export) of directory.gov.au content. The RDF data is stored using the [Jena](http://jena.apache.org/) native triplestore and made accessible at a [SPARQL endpoint](http://www.w3.org/TR/2013/REC-sparql11-service-description-20130321) via JEna's [Fuseki](https://jena.apache.org/documentation/fuseki2/) frontend.


## License
This repository is licensed under Creative Commons 4.0 International. See the [LICENSE deed](LICENSE) in this repository for details.


## Contacts
Lead Developer:  
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water  
<nicholas.car@csiro.au>  
<http://orcid.org/0000-0002-8742-7730>
