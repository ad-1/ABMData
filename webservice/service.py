
"""
    webservice that accepts payload.xml

    Requirements:
    The webservice should respond with a status code which is
    based on parsing the contents of the XML payload

        a.	If the XML document specified in payload is passed
            then return a status of ‘0’ – which means
            the document was structured correctly.

        b.	If the Declararation’s Command <> ‘DEFAULT’
            then return ‘-1’ – which means invalid command specified.

        c.	If the SiteID <> ‘DUB’ then return ‘-2’ – invalid Site specified.
"""

from flask import Flask, request
from lxml import etree

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    data = request.get_data()
    response = get_response(data, xsd_path='payload.xsd')
    headers = {
        'Content-Type': 'application/xml',
        'Accept': '*/*',
        'Content-Length': utf8len(response.value[0])
    }
    return response.value[0], response.value[1], headers


def utf8len(s):
    content_length = len(s.encode('utf-8'))
    print('Content-Length:', content_length)
    return content_length


def get_response(data, xsd_path):
    """
    get appropriate http response
    :param xsd_path: path to xsd file
    :param data: post data
    :return: http response
    """
    valid, dom = validate_xml(data)

    if not valid:
        return Response.INVALID_XML

    if not validate_xsd(dom, xsd_path):
        return Response.INVALID_XSD

    root = dom.getroot()

    if not validate_declaration_command(root):
        return Response.INVALID_DECLARATION_CMD

    if not validate_site(root):
        return Response.INVALID_SITEID

    return Response.VALID_PAYLOAD


def validate_xml(data):
    """
    validate that the request contains valid xml
    :param data: xml string
    :return: http status code
    """
    try:
        dom = etree.ElementTree(etree.fromstring(data))
        return True, dom
    except Exception as e:
        print(e)
        return False, None


def validate_xsd(dom, xsd_path):
    """
    validate xml with vsa
    :param xsd_path:
    :param dom: xml dom
    :param xsd: xsd file path
    :return: whether payload is valid
    """
    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema.validate(dom)


def validate_declaration_command(root):
    """
    validate payload declaration command
    :param root: dom root object
    :return: True if command is 'DEFAULT'
    """
    declaration = root.find('DeclarationList/Declaration')
    cmd = declaration.attrib['Command']
    if cmd == 'DEFAULT':
        return True
    return False


def validate_site(root):
    """
    validate the site is 'DUB'
    :param root: document root
    :return: true if site id is valid
    """
    site_elem = root.find('DeclarationList/Declaration/DeclarationHeader/SiteID')
    site = site_elem.text
    if site == 'DUB':
        return True
    return False


if __name__ == '__main__':
    with app.app_context():
        app.run(port=5000, debug=True)
