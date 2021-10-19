#!/usr/bin/env python3

# The MIT License (MIT)
#
# Copyright (c) 2018-2021 Frank Klaassen
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
import sys
import logging
import re

"""
Handle arguments
"""


def set_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server",
        "-s",
        dest="zabbix_host",
        help="Zabbix URL",
        default=os.environ.get("ZABBIX_HOST", None),
    )
    parser.add_argument(
        "--token",
        dest="zabbix_api_token",
        help="Zabbix API token",
        default=os.environ.get("ZABBIX_API_TOKEN", None),
    )

    # Optional arguments
    parser.add_argument(
        "--format",
        "-f",
        dest="export_format",
        help="Format to use to store the configuration as.",
        choices=["xml", "json", "yaml"],
        default="yaml",
    )
    parser.add_argument(
        "--type",
        "-t",
        dest="export_type",
        help="Export this type of entities.",
        choices=["templates", "mediatypes", "hosts", "hostgroups", "maps", "images"],
        default="templates",
    )
    parser.add_argument(
        "--debug",
        "-d",
        dest="debug",
        help="Enable debugging output",
        action="store_true",
    )

    args = parser.parse_args()

    if not args.zabbix_host or not args.zabbix_api_token:
        exit(parser.print_usage())

    return args


"""
Export templates
"""


def export_templates(zapi):
    templates = zapi.template.get(output=["name", "id"])

    for t in templates:
        template_id = int(t["templateid"])
        name = normalize(t["name"])
        print("Exporting template %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format,
            prettyprint=True,
            options={"templates": [template_id]},
        )
        write_export(name, config, args.export_format)


"""
Export mediatypes
"""


def export_mediaTypes(zapi):
    mediatypes = zapi.mediatype.get(output=["mediatypeid", "name"])

    for t in mediatypes:
        mediatype_id = int(t["mediatypeid"])
        name = "MediaType_" + normalize(t["name"])
        print("Exporting media type %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format,
            prettyprint=True,
            options={"mediaTypes": [mediatype_id]},
        )
        write_export(name, config, args.export_format)


"""
Export hosts
"""


def export_hosts(zapi):
    hosts = zapi.host.get(output=["hostid", "name"])

    for t in hosts:
        host_id = int(t["hostid"])
        name = "Host_" + re.sub(r"[^a-zA-Z0-9\-\_\.]+", "_", t["name"])
        print("Exporting host %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format, prettyprint=True, options={"hosts": [host_id]}
        )
        write_export(name, config, args.export_format)


"""
Export host groups
"""


def export_hosts_groups(zapi):
    host_groups = zapi.hostgroup.get(output=["groupid", "name"])

    for t in host_groups:
        hostgroup_id = int(t["groupid"])
        name = "HostGroup_" + re.sub(r"[^a-zA-Z0-9\-\_\.]+", "_", t["name"])
        print("Exporting hostgroup %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format,
            prettyprint=True,
            options={"groups": [hostgroup_id]},
        )
        write_export(name, config, args.export_format)


"""
Export maps
"""


def export_maps(zapi):
    maps = zapi.map.get(output=["sysmapid", "name"])

    for t in maps:
        map_id = int(t["sysmapid"])
        name = "Map_" + normalize(t["name"])
        print("Exporting map %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format,
            prettyprint=True,
            options={"maps": [map_id]},
        )
        write_export(name, config, args.export_format)


"""
Export images
"""


def export_images(zapi):
    images = zapi.image.get(output=["imageid", "name"])

    for t in images:
        image_id = int(t["imageid"])
        name = "Image_" + normalize(t["name"])
        print("Exporting image %s..." % name)

        config = zapi.configuration.export(
            format=args.export_format,
            prettyprint=True,
            options={"images": [image_id]},
        )
        write_export(name, config, args.export_format)


"""
Write the output to a file
"""


def write_export(name, config, export_format="yaml"):
    if config is not None:
        print("Writing %s.%s" % (name, export_format))
        with open("%s.%s" % (name, export_format), "w") as f:
            f.write(config)


"""
Normalize the template name to generate a proper filename
"""


def normalize(input):
    return re.sub(r"[^a-zA-Z0-9\-\_]+", "_", input)


"""
Main function
"""


def exporter(args):
    try:
        zapi = ZabbixAPI(server=args.zabbix_host)
        zapi.login(api_token=args.zabbix_api_token)
        print("Connected to Zabbix API Version %s" % zapi.api_version())

    except Exception as e:
        print("Failed to connect with the Zabbix API. Please check your credentials.")
        print(str(e))
        exit(1)

    if args.debug is True:
        stream = logging.StreamHandler(sys.stdout)
        stream.setLevel(logging.DEBUG)
        log = logging.getLogger("pyzabbix")
        log.addHandler(stream)
        log.setLevel(logging.DEBUG)

    if args.export_type == "templates":
        export_templates(zapi)
    elif args.export_type == "mediatypes":
        export_mediaTypes(zapi)
    elif args.export_type == "hosts":
        export_hosts(zapi)
    elif args.export_type == "hostgroups":
        export_hosts_groups(zapi)
    elif args.export_type == "maps":
        export_maps(zapi)
    elif args.export_type == "images":
        export_images(zapi)


if __name__ == "__main__":
    args = set_arguments()
    exporter(args)
