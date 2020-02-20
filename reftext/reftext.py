# XML (Extensible Markup Language) Parser

"""
    XML Parser
    Corresponding xml document 'doc.xml'
    Problem:
        Extract the RefText values for the following RefCodes: ‘MWB’, ‘TRV’ and ‘CAR’
"""

import xml.etree.ElementTree as Et


class XmlParser:

    def __init__(self, filename):
        """
        initialise xml parser
        :param filename: full path to xml document
        """
        self.dom = self.read_xml(filename)
        self.root = self.dom.getroot()
        self.tags_with_attrib = []
        self.filtered_tags = []
        self.extacted_vals = []
        self.traced_vals = {}

    @staticmethod
    def read_xml(filename):
        """
        read xml document using Element Tree module
        :param filename: full path to file containing message
        :return xml element tree object
        """
        return Et.parse(filename)

    def get_tags_with_attrib(self, element, attrib):
        """
        get all tags that have the specified attribute
        :param element: xml doc element to check
        :param attrib: attribute we are looking for
        """
        for child in element:
            if attrib in child.attrib:
                self.tags_with_attrib.append(child)
            self.get_tags_with_attrib(child, attrib)

    def filter_tags(self, attrib, attrib_values):
        """
        filter tags based on a particular attribute and list of possible values
        :param attrib: xml attribute name
        :param attrib_values: list of accepted attributed values
        """
        for tag in self.tags_with_attrib:
            if tag.attrib[attrib] in attrib_values:
                self.filtered_tags.append(tag)

    def extract_vals(self, tag, attrib):
        """
        extract the values from the tags within the filtered tags
        :param attrib: attribute name
        :param tag: inner tag from which the value is extracted
        """
        for element in self.filtered_tags:
            for child in element:
                if child.tag == tag:
                    self.extacted_vals.append(child.text)
                    self.traced_vals.setdefault(element.attrib[attrib], []).append(child.text)

    ######################################################################################

    # simple solution if path through dom is known

    def get_reftext(self, path, attrib, attrib_values, tag):
        """
        directly get values from RefText if dom structure is known
        :param path: path through dom to Reference tags
        :param attrib: outer tag filtered attribute name
        :param attrib_values: attribute values to filter tag by
        :param tag: return text from this tag
        """
        self.traced_vals = {}
        references = self.root.findall(path)
        for ref in references:
            if ref.attrib[attrib] in attrib_values:
                reftext = ref.findall(tag)
                for reft in reftext:
                    self.traced_vals.setdefault(ref.attrib[attrib], []).append(reft.text)

    ######################################################################################

    # debugging. see above for solution

    def print_tags_and_attribs(self, ele):
        """
        print all element tags and their attributes
        :param ele: display info for element
        """
        for el in ele:
            print(el, ' ==> tag:', el.tag, ', attrib:', el.attrib)
            self.print_tags_and_attribs(el)


# Program driver
if __name__ == '__main__':

    _filename = 'doc.xml'  # xml document path
    _attrib = 'RefCode'  # search for tags that have this attribute
    _attrib_values = ['MWB', 'TRV', 'CAR']  # filter tags based on _attrib that matching one of the following
    _tag = 'RefText'  # get the value from this tag from within the filtered tags

    parser = XmlParser(_filename)  # create new xml parser object
    parser.get_tags_with_attrib(parser.root, _attrib)  # get all tags which have a specified attrib i.e all tags with attribute 'RefCode'
    parser.filter_tags(_attrib, _attrib_values)  # filter tags for tags that have 'RefCode' matching one of the given
    parser.extract_vals(_tag, _attrib)  # extract the values from the 'RefText' tags if is inside the filtered tags

    # solution
    print('corresponding values: ', parser.traced_vals)
    print('extracted values are: ', parser.extacted_vals)

    # simple solution if dom structure is known
    _path = 'DeclarationList/DeclarationHeader/Reference'
    parser.get_reftext(_path, _attrib, _attrib_values, _tag)
    print('corresponding values: ', parser.traced_vals)
