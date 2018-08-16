#!/usr/bin/env python2
"""
Zabbix Template Exporter
2018 Frank Klaassen <frank@cloudright.nl>
"""

from pyzabbix import ZabbixAPI
from xml.dom import minidom
import argparse
import os
import base64


def is_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
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
    args = parser.parse_args()

    if not args.zabbix_host or not args.zabbix_user or not args.zabbix_password:
        exit(parser.print_usage())

    if is_base64(args.zabbix_user):
        args.zabbix_user = base64.b64decode(args.zabbix_user).strip()

    if is_base64(args.zabbix_password):
        args.zabbix_password = base64.b64decode(args.zabbix_password).strip()

    return args


def export_templates(url, user, password):
    try:
        zapi = ZabbixAPI(url=url, user=user, password=password)
    except Exception, e:
        print('Failed to connect with the Zabbix API. Please check your credentials.')
        print(str(e))
        exit(1)

    templates = zapi.template.get(
        output=['name', 'id']
    )

    for t in templates:
        template_id = t['templateid']
        name = t['name'].replace(' ', '_')

        config = zapi.configuration.export(
            format='xml',
            options={
                'templates': [template_id]
            }
        )

        print('Exporting %s...' % name)
        xmlstr = minidom.parseString(config).toprettyxml(indent="   ")
        with open("%s.xml" % name, "w") as f:
            f.write(xmlstr)


if __name__ == "__main__":
    args = set_arguments()
    export_templates(args.zabbix_host, args.zabbix_user, args.zabbix_password)
