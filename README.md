# Zabbix Template Exporter

This tool connects to the Zabbix API.
It retrieves all templates and stores them in individual XML files allowing you to re-use these templates and make backups of them.

## Install
Install the requirements:
```bash
$ pip3 install -r requirements.txt
```

## Usage
You can provide your credentials on the commandline:
```bash
usage: export.py [-h] [--server ZABBIX_HOST] [--username ZABBIX_USER]
                 [--password ZABBIX_PASSWORD] [--format EXPORT_FORMAT]
                 [--type EXPORT_TYPE] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --server ZABBIX_HOST, -s ZABBIX_HOST
                        Zabbix URL
  --username ZABBIX_USER, -u ZABBIX_USER
                        Zabbix user to connect with the API
  --password ZABBIX_PASSWORD, -p ZABBIX_PASSWORD
                        Zabbix password for connecting to the API
  --format EXPORT_FORMAT, -f EXPORT_FORMAT
                        Export the templates as XML or JSON
  --type EXPORT_TYPE, -t EXPORT_TYPE
                        Export this type of entities
  --debug, -d           Enable debugging output
```

You can also configure your credentials globally and export these (e.g. in `.bashrc` or `.zshrc`) like this:

```bash
export ZABBIX_HOST=https://zabbix.example.com
export ZABBIX_USER=youruser
export ZABBIX_PASS=yourpass
```

Both `ZABBIX_USER` and `ZABBIX_PASS` can be provided as a string or a base64 string to prevent the passwords from being visible easily.
The exporter automatically detects the content and will act accordingly.


## License
The MIT License (MIT). Please see the [license file](https://github.com/syphernl/zabbix-template-exporter/blob/master/LICENSE) for more information.
