#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2018-2020 Frank Klaassen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pyzabbix import ZabbixAPI
import argparse
import os
import base64
import sys
import logging
from xml.dom import minidom
import simplejson


def is_base64(sb):
    try:
        if isinstance(sb, str):
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False


def set_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server',
                        '-s',
                        dest='zabbix_host',
                        help='Zabbix URL',
                        default=os.environ.get('ZABBIX_HOST', None),
                        )
    parser.add_argument('--username', '-u',
                        dest='zabbix_user',
                        help='Zabbix user to connect with the API',
                        default=os.environ.get('ZABBIX_USER', None),
                        )
    parser.add_argument('--password', '-p',
                        dest='zabbix_password',
                        help='Zabbix password for connecting to the API',
                        default=os.environ.get('ZABBIX_PASS', None),
                        )

    # Optional arguments
    parser.add_argument('--format', '-f',
                        dest='export_format',
                        help='Export the templates as XML or JSON',
                        default='xml',
                        )
    parser.add_argument('--type', '-t',
                        dest='export_type',
                        help='Export this type of entities',
                        default='templates',
                        )
    parser.add_argument('--debug', '-d',
                        dest='debug',
                        help='Enable debugging output',
                        action='store_true'
                        )

    args = parser.parse_args()

    if not args.zabbix_host or not args.zabbix_user or not args.zabbix_password:
        exit(parser.print_usage())

    if is_base64(args.zabbix_user):
        args.zabbix_user = base64.b64decode(args.zabbix_user).strip().decode('utf-8')

    if is_base64(args.zabbix_password):
        args.zabbix_password = base64.b64decode(args.zabbix_password).strip().decode('utf-8')

    return args


def export_templates(args):
    try:
        zapi = ZabbixAPI(server=args.zabbix_host)
        zapi.login(user=args.zabbix_user, password=args.zabbix_password)
        print("Connected to Zabbix API Version %s" % zapi.api_version())

    except Exception as e:
        print('Failed to connect with the Zabbix API. Please check your credentials.')
        print(str(e))
        exit(1)

    if args.debug is True:
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger('pyzabbix')
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)

    # Export Templates (Triggers, items etc)
    if args.export_type == 'templates':
        templates = zapi.template.get(
            output=['name', 'id']
        )

        for t in templates:
            template_id = t['templateid']
            name = normalize(t['name'])
            print('Exporting template %s...' % name)

            config = zapi.configuration.export(
                format=args.export_format,
                options={
                    'templates': [template_id]
                }
            )
            write_export(name, config, args.export_format)

    # Export Media Types
    elif args.export_type == 'mediatypes':
        mediatypes = zapi.mediatype.get(
            output=['mediatypeid', 'name']
        )

        for t in mediatypes:
            mediatype_id = t['mediatypeid']
            name = 'Media_' + normalize(t['name'])
            print('Exporting media type %s...' % name)

            config = zapi.configuration.export(
                format=args.export_format,
                options={
                    'mediaTypes': [mediatype_id]
                }
            )
            write_export(name, config, args.export_format)

    # Export ValueMaps
    elif args.export_type == 'valuemaps':
        valuemaps = zapi.valuemap.get(
            output=['valuemapid', 'name']
        )
        print(valuemaps)

        for t in valuemaps:
            valuemap_id = t['valuemapid']
            name = 'Valuemap_' + normalize(t['name'])
            print('Exporting valuemap %s...' % name)

            config = zapi.configuration.export(
                format=args.export_format,
                options={
                    'valueMaps': [valuemap_id]
                }
            )
            write_export(name, config, args.export_format)


def write_export(name, config, export_format='xml'):
    if config is not None:
        if export_format == 'xml':
            xmlstr = minidom.parseString(config).toprettyxml(indent="   ")
            print('Writing %s.xml' % name)
            with open("%s.xml" % name, "w") as f:
                f.write(xmlstr)
        elif export_format == 'json':
            print('Writing %s.json' % name)
            with open("%s.json" % name, "w") as f:
                f.write(simplejson.dumps(simplejson.loads(config), indent=4, sort_keys=True))


def normalize(input):
    input = input.replace(' ', '_')
    input = input.replace('/', '_')
    input = input.replace(':', '_')
    return input


if __name__ == "__main__":
    args = set_arguments()
    export_templates(args)
