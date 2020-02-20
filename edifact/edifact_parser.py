# EDIFACT Message Parser


"""
    EDIFACT
    (Electronic Data Interchange for Administration, Commerce and Transport)

    Global set of rules defined by the UN for the inter-company electronic
    data exchange between two or more business partners via EDI.

    Problem:
        Taking an EDIFACT message text, write some code to parse
        out the all the LOC segments and populate an array with
        the 2nd and 3rd element of each segment.

        Note:  the ‘+’ is an element delimiter

    UNA segment (optional): here you can rename separators and special characters
    UNB segment: file header; forms the envelope with the UNZ, which contains general information
    UNG segment: group start; messages can be combined into message groups
    UNH segment: message header; this is where the actual message is located
    UNT segment: end of message
    UNE segment: group end
    UNZ segment: end of file

"""

import json


class EdifactParser:

    def __init__(self, filename):
        """
        initialise edifact parser class
        :param filename: full path to file containing message
        """
        self.msg = None  # raw edifact message
        self.segments = {}  # dict of segments
        self.read_msg(filename)  # read message from file

    def read_msg(self, filename):
        """
        read edifact message from file.
        store message in class property 'msg'
        :param filename: full path to file containing message
        """
        f = open(filename, 'r')
        self.msg = f.readlines()
        f.close()

    def filter_elems(self, seg_id, indexes, delimiter):
        """
        parse elements in indexes for a given segment identifier
        'seg_id' is 'segment identifier' (first element in segment)
        :param seg_id: identifier of the segments being queried, i.e 'LOC', 'DTM'
        :param indexes: element indexes for the matching segments to be returned
        :param delimiter: character separating the segment elements i.e '+'
        """
        trace_elems = {}
        filtered_elems = []
        for s, seg in enumerate(self.msg):
            elems = seg.split(delimiter)
            if elems[0] == seg_id:
                for i in indexes:
                    if i < len(elems):
                        filtered_elems.append(elems[i])
                        trace_elems.setdefault(seg, []).append(elems[i])
        return filtered_elems, trace_elems

    ######################################################################################

    # debugging. see above for solution

    def request_segments(self, seg_id, delimiter):
        """
        get list of segments matching an identifier
        :param seg_id: string for matching the first element
        :param delimiter: character separating the segment elements i.e '+'
        :return: list of matching segments
        """
        segs = []
        for seg in self.msg:
            elems = seg.split(delimiter)
            if elems[0] == seg_id:
                segs.append(seg)
        return segs

    def parse_all_segments(self, delimiter):
        """
        creating dictionary containing all segments and their respective elements
        dictionary keys are the segments, values is the list of elements
        :param delimiter: character separating the segment elements i.e '+'
        """
        for s, segment in enumerate(self.msg):
            elems = segment.split(delimiter)
            self.segments[segment] = elems

    @staticmethod
    def pprint(dictionary):
        """
        pretty print dictionary object
        :param dictionary: dictionary to print
        """
        print(json.dumps(
            dictionary,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        ))


# Program driver
if __name__ == '__main__':

    _filename = 'edifact/msg.txt'  # filename containing edifact message
    _seg_id = 'LOC'  # filtering segments by
    _delimiter = '+'  # elements separated by
    _indexes = [1, 2]  # get second and third elements from matching segments

    parser = EdifactParser(_filename)  # create parser object

    # debugging
    parser.parse_all_segments(_delimiter)  # parse all segments into dictionary with segments as keys and elements for values
    _segs = parser.request_segments(_seg_id, _delimiter)  # these are the segments we want to find elements in

    # solution
    _filtered_elems, _trace_elems = parser.filter_elems(_seg_id, _indexes, _delimiter)  # get filtered elements and trace their segments
    # parser.pprint(_trace_elems)  # pretty print which segments the elements came from

    print('\nresult: filtered elements at indexes {} from all {} segments: {}'.format(_indexes, _seg_id, _filtered_elems))
