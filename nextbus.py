#!/usr/bin/python3

import sys
import itertools
import requests
import xml.etree.ElementTree as ET
from optparse import OptionParser

def nextbus_request(command, agency, route, stop):
    params = { 'command': command,
               'a': agency,
               'r': route,
               's': stop }
    r = requests.get('http://webservices.nextbus.com/service/publicXMLFeed', params=params)
    return r.text


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-a', '--agency',
            dest='agency',
            default='ttc',
            metavar='ID',
            help='choose the agency to get predictions for')
    parser.add_option('-r', '--route',
            dest='route',
            default='224',
            metavar='ID',
            help='choose the route to query')
    parser.add_option('-s', '--stop',
            dest='stop',
            default='5815',
            metavar='ID',
            help='choose the stop to query')

    (options, args) = parser.parse_args()

    xml = nextbus_request('predictions', options.agency, options.route, options.stop)
    tree = ET.fromstring(xml)

    error = tree.find('Error')
    if not error is None:
        print("Error: %s" % (error.text.strip()), file=sys.stderr)
        sys.exit(1)

    for prediction in tree.iter('predictions'):
        print(prediction.attrib['stopTitle'])

        for direction in prediction.iter('direction'):
            print("└─%s" % direction.attrib['title'])

            for prediction in itertools.islice(direction, None, 3):
                print("    %2s minutes" % prediction.attrib['minutes'])
