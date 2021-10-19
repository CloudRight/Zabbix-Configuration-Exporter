# Zabbix Configuration Exporter  [![Latest Release](https://img.shields.io/github/release/CloudRight/Zabbix-Configuration-Exporter.svg)](https://github.com/CloudRight/Zabbix-Configuration-Exporter/releases/latest)

This tool connects to the Zabbix API and retrieves configuration and stores this in individual files, allowing you to re-use these templates and make backups of them (e.g. by adding them to version control).

It is capable of exporting the following:

* Templates
* Mediatypes
* Hosts
* Host Groups
* Maps
* Images

Tested with Zabbix 5.4.x



## Install
Install the requirements:

```bash
$ pip3 install -r requirements.txt
```

## Usage
You can provide your credentials on the commandline:

```bash
usage: export.py [-h] [--server ZABBIX_HOST] [--token ZABBIX_API_TOKEN] [--format {xml,json,yaml}] [--type {templates,mediatypes,hosts,hostgroups,maps,images}] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --server ZABBIX_HOST, -s ZABBIX_HOST
                        Zabbix URL
  --token ZABBIX_API_TOKEN
                        Zabbix API token
  --format {xml,json,yaml}, -f {xml,json,yaml}
                        Export the templates as XML or JSON
  --type {templates,mediatypes,hosts,hostgroups,maps,images}, -t {templates,mediatypes,hosts,hostgroups,maps,images}
                        Export this type of entities
  --debug, -d           Enable debugging output


```

You can also configure your credentials globally and export these (e.g. in `.bashrc` or `.zshrc`) like this:

```bash
export ZABBIX_HOST=https://zabbix.example.com
export ZABBIX_API_TOKEN=your-token
```

## Limitations

* Exporting auto-discovered hosts results in an empty file, because the Zabbix API does not provide this information.

## License
The MIT License (MIT). Please see the [license file](./LICENSE) for more information.
